import logging
from contextlib import ExitStack
from copy import copy, deepcopy
from typing import Optional, Dict, List, Type, Tuple, Callable

from aiohttp import web
from heaobject.root import DesktopObjectDict
from yarl import URL
from heaserver.service import runner
from heaserver.service import wstl
from heaserver.service.db.database import DatabaseManager
from heaserver.service.db.mongo import MongoManager
from heaserver.service.db.mockmongo import MockMongoManager
from heaserver.service.docker import get_exposed_port, get_bridge_ip, DockerContainerConfig, \
    wait_for_status_code
from contextlib import contextmanager, closing
from typing import Generator
from abc import ABC


def start_microservice_container(container_config: DockerContainerConfig, stack: ExitStack,
                                 registry_url: Optional[str] = None) -> Tuple[str, str]:
    """
    Starts a Docker container with the provided HEA microservice image and configuration (container_spec argument),
    Mongo database container, and exit stack for cleaning up resources. If the docker_image object has a check_path,
    the function will wait until the microservice returns a 200 status code from a GET call to the path before
    returning a two-tuple with the container's external and bridge URLs. This function wraps DockerImage's start()
    method.

    The following environment variables are set in the container and will overwrite any pre-existing values that were
    set using the image's env_vars property:
        MONGO_HEA_DATABASE is set to the value of the hea_database argument.
        HEASERVER_REGISTRY_URL is set to the value of the registry_url argument.

    Any other environment variables set using the image's env_vars property are retained.

    :param container_config: the Docker image to start (required).
    :param stack: the ExitStack (required).
    :param registry_url: optional base URL for the heaserver-registry microservice.
    :return: a two-duple containing the container's external URL string and the bridge URL string.
    """
    logger = logging.getLogger(__name__)
    logger.debug('Starting docker container %s', container_config.image)
    container_config_ = _with_hea_env_vars(container_config, registry_url)

    microservice = container_config_.start(stack)

    external_url = f'http://{microservice.get_container_host_ip()}:{get_exposed_port(microservice, container_config_.port)}'
    logger.debug('External URL of docker image %s is %s', container_config_.image, external_url)

    if container_config_.check_path is not None:
        wait_for_status_code(str(URL(external_url).with_path(container_config_.check_path)), 200)

    bridge_url = f'http://{get_bridge_ip(microservice)}:{container_config_.port}'
    logger.debug('Internal URL of docker image %s is %s', container_config_.image, bridge_url)

    return external_url, bridge_url


class RegistryContainerConfig(DockerContainerConfig, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RealRegistryContainerConfig(RegistryContainerConfig):
    def __init__(self, image: str):
        super().__init__(image=image, port=8080, check_path='/components', db_manager_cls=MongoManager)


class MockRegistryContainerConfig(RegistryContainerConfig):
    def __init__(self, image: str):
        super().__init__(image=image, port=8080, check_path='/components', db_manager_cls=MockMongoManager)


@contextmanager
def app_context(db_manager_cls: Type[DatabaseManager],
                desktop_objects: Dict[str, List[DesktopObjectDict]],
                other_microservice_images: Optional[List[DockerContainerConfig]] = None,
                other_db_manager_cls: Optional[List[Type[DatabaseManager]]] = None,
                registry_docker_image: Optional[RegistryContainerConfig] = None,
                content: Dict[str, Dict[str, bytes]] = None,
                wstl_builder_factory: Optional[Callable[[], wstl.RuntimeWeSTLDocumentBuilder]] = None) -> Generator[web.Application, None, None]:
    """
    Starts the test environment. The test environment consists of: a "bridge" database that is accessible from the
    internal docker network; an "external" database that is accessible from outside the network; a "bridge" registry
    service that is accessible from the internal docker network; an "external" registry service that is accessible from
    outside the network; the service being tested, which is run from outside of docker; and any service dependencies,
    which are run as docker containers. The provided context manager will clean up any resources upon exit.

    :param db_manager_cls: the database manager class for the microservice being tested (required).
    :param desktop_objects: HEA desktop objects to load into the database (required), as a map of collection -> list of
    desktop object dicts.
    :param other_microservice_images: the docker images of any service dependencies.
    :param other_db_manager_cls: a list of database manager classes from the heaserver.server.db package, if any
    supporting microservices need database connectivity. If omitted or None, heaserver.service.db.mongo.MongoManager is
    used.
    :param registry_docker_image: an HEA registry service docker image.
    :param content: any content to load into the database.
    :param wstl_builder_factory: a zero-argument callable that will return a RuntimeWeSTLDocumentBuilder. Optional if
    this service has no actions. Typically, you will use the heaserver.service.wstl.get_builder_factory function to
    get a factory object.
    :param testing: whether this function was called by a test case in a HEAAioHTTPTestCase object. Default is False.
    :returns: a callable for creating the aiohttp Application.
    """

    def _bridge_dbs_to_start() -> set[type[DatabaseManager]]:
        bridge_db_manager_cls = set()
        if other_db_manager_cls:
            bridge_db_manager_cls.update(other_db_manager_cls)
        if registry_docker_image is not None and registry_docker_image.db_manager_cls is not None:
            bridge_db_manager_cls.add(registry_docker_image.db_manager_cls)
        return bridge_db_manager_cls

    with ExitStack() as context_manager, closing(db_manager_cls()) as external_db_, db_manager_cls.environment(), db_manager_cls.context():
        bridge_dbs = [context_manager.enter_context(closing(bridge_db_cls())) for bridge_db_cls in
                      _bridge_dbs_to_start()]
        bridge_desktop_objects, external_desktop_objects = deepcopy(desktop_objects), deepcopy(desktop_objects)
        external_db_.start_database(context_manager)
        if registry_docker_image is not None:
            assert registry_docker_image.db_manager_cls is not None
            if db_manager_cls != registry_docker_image.db_manager_cls:
                external_registry_db_ = context_manager.enter_context(closing(registry_docker_image.db_manager_cls()))
                external_registry_db_.start_database(context_manager)
            else:
                external_registry_db_ = external_db_
        for bridge_db in bridge_dbs:
            bridge_db.start_database(context_manager)
        if registry_docker_image is not None:
            bridge_config_ = _add_db_config(registry_docker_image, bridge_dbs)
            _, bridge_registry_url = start_microservice_container(bridge_config_, context_manager)
            external_config_ = _add_db_config(registry_docker_image, [external_registry_db_])
            external_registry_url, _ = start_microservice_container(external_config_, context_manager)
        else:
            external_registry_url = None
            bridge_registry_url = None
        if other_microservice_images:
            _start_other_docker_containers(bridge_desktop_objects, external_desktop_objects,
                                           other_microservice_images, bridge_registry_url, bridge_dbs, context_manager)
        config_file = _generate_config_file(external_db_, external_registry_url)
        if registry_docker_image is not None and type(external_db_) != registry_docker_image.db_manager_cls:
            external_db_.insert_all({k: v for k, v in external_desktop_objects.items() if k in (external_db_.get_relevant_collections() or [])}, content)
            external_registry_db_.insert_desktop_objects({k: v for k, v in external_desktop_objects.items() if k == 'components'})
        else:
            external_db_.insert_all({k: v for k, v in external_desktop_objects.items() if k in (external_db_.get_relevant_collections() or [])}, content)
        for bridge_db in bridge_dbs:
            bridge_db.insert_all({k: v for k, v in bridge_desktop_objects.items() if k in (bridge_db.get_relevant_collections() or [])}, content)
        yield runner.get_application(db=external_db_, wstl_builder_factory=wstl_builder_factory,
                                     config=runner.init(config_string=config_file))


def _add_db_config(docker_container_config: DockerContainerConfig, dbs: list[DatabaseManager]) -> DockerContainerConfig:
    """
    Returns a copy of the docker_container_config with additional environment variables needed for connecting to the
    database.

    :param docker_container_config: a DockerContainerConfig (required).
    :param dbs: the available database containers.
    :return: a newly created DockerContainerConfig.
    """
    db_manager = _get_db_manager(dbs, docker_container_config.db_manager_cls)
    if db_manager is not None:
        env_vars = db_manager.get_microservice_env_vars()
    else:
        env_vars = None
    return docker_container_config.with_env_vars(env_vars)


def _get_db_manager(dbs: list[DatabaseManager], db_manager_cls_: Optional[type[DatabaseManager]]) -> Optional[DatabaseManager]:
    """
    Returns the database manager with the given type.

    :param dbs: the available database managers.
    :param db_manager_cls_: the type of interest.
    :return: a database manager, or None if no database manager with the given type is available.
    """
    if db_manager_cls_ is not None:
        return next((b for b in dbs if isinstance(b, db_manager_cls_)), None)
    else:
        return None


def _start_other_docker_containers(bridge_desktop_objects: Dict[str, List[DesktopObjectDict]],
                                   external_desktop_objects: Dict[str, List[DesktopObjectDict]],
                                   other_docker_images: Optional[List[DockerContainerConfig]],
                                   registry_url: Optional[str],
                                   bridge_dbs: list[DatabaseManager],
                                   stack: ExitStack):
    """
    Starts the provided microservice containers.

    :param bridge_desktop_objects: data to go into the database that is internal to the docker network, as a map of
    collection -> list of desktop object dicts.
    :param external_desktop_objects: data to go into the database that is outside of the docker network, as a map of
    collection -> list of desktop object dicts.
    :param other_docker_images: a list of docker images to start.
    :param registry_url: the URL of the registry microservice.
    :param stack: the ExitStack.
    """
    for img in other_docker_images or []:
        db_manager = _get_db_manager(bridge_dbs, img.db_manager_cls)
        if db_manager is not None:
            env_vars = db_manager.get_microservice_env_vars()
            img_ = img.with_env_vars(env_vars)
        else:
            img_ = img
        external_url, bridge_url = start_microservice_container(img_, stack, registry_url)
        bridge_desktop_objects.setdefault('components', []).append(
            {'type': 'heaobject.registry.Component', 'base_url': bridge_url, 'name': bridge_url,
             "owner": "system|none", 'resources': [r.to_dict() for r in img_.resources or []]})
        external_desktop_objects.setdefault('components', []).append(
            {'type': 'heaobject.registry.Component', 'base_url': external_url, 'name': external_url,
             "owner": "system|none", 'resources': [r.to_dict() for r in img_.resources or []]})


def _generate_config_file(db_manager: DatabaseManager, registry_url: Optional[str]) -> str:
    """
    Generates a HEA microservice configuration file.

    :param db_manager: a DatabaseManager instance (required).
    :param registry_url: the URL of the registry service.
    :returns: the configuration file string.
    """
    if db_manager is not None:
        if registry_url is None:
            config_file = db_manager.get_config_file_section()
        else:
            config_file = f"""
    [DEFAULT]
    Registry={registry_url}

    {db_manager.get_config_file_section()}
                    """
    else:
        if registry_url is None:
            config_file = ''
        else:
            config_file = f"""
        [DEFAULT]
        Registry={registry_url}
                        """
    return config_file


def _with_hea_env_vars(container_config: DockerContainerConfig,
                       registry_url: Optional[str]) -> DockerContainerConfig:
    """
    Copies the provided container_spec, adding the environment variables corresponding to the provided arguments.

    :param container_config: the image and configuration (required).
    :param db_manager: a TestDatabaseFactory instance (required).
    :param registry_url: the URL of the registry service, which populates the HEASERVER_REGISTRY_URL environment
    variable.
    :return: the copy of the provided container_spec.
    """
    env_vars: Dict[str, str] = {}
    if registry_url is not None:
        env_vars['HEASERVER_REGISTRY_URL'] = registry_url
    return container_config.with_env_vars(env_vars)
