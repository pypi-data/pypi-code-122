"""
Utility functions and classes for working with docker images and containers.
"""
from contextlib import ExitStack

from testcontainers.core.waiting_utils import wait_container_is_ready
import requests
from testcontainers.core.container import DockerContainer
from typing import Dict, List
from copy import deepcopy, copy
from typing import Optional
from heaobject.registry import Resource
from heaserver.service.db.database import DatabaseManager
from enum import Enum


class DockerImages(Enum):
    """
    Images to use for SwaggerUI, tests, and other situations in which we want HEA to start Docker containers
    automatically.
    """
    MONGODB = 'percona/percona-server-mongodb:4.4.9'


class DockerVolumeMapping:
    """
    Docker volume mapping. This class is immutable.
    """

    def __init__(self, host: str, container: str, mode: str = 'ro'):
        """
        Creates a volume mapping.

        :param host: the path of the directory on the host to map (required).
        :param container: the path to mount the volume in the container (required).
        :param mode: access level in the container as Unix rwx-style permissions (defaults to 'ro').
        """
        if mode is None:
            self.__mode: str = 'ro'
        else:
            self.__mode = str(mode)
        self.__container = str(container)
        self.__host = str(host)

    @property
    def host(self) -> str:
        return self.__host

    @property
    def container(self) -> str:
        return self.__container

    @property
    def mode(self) -> str:
        return self.__mode


class DockerContainerConfig:
    """
    Docker image and configuration for starting a container. This class is immutable.
    """

    def __init__(self, image: str, port: int, check_path: Optional[str] = None,
                 resources: Optional[List[Resource]] = None,
                 volumes: Optional[List[DockerVolumeMapping]] = None,
                 env_vars: Optional[Dict[str, str]] = None,
                 db_manager_cls: Optional[type[DatabaseManager]] = None):
        """
        Constructor.

        :param image: the image tag (required).
        :param port: the exposed port (required).
        :param check_path: the URL path to check if the microservice is running.
        :param resources: a list of heaobject.registry.Resource dicts indicating what content types this image is designed for.
        :param volumes: a list of volume mappings.
        :param env_vars: a dict containing environment variable names mapped to string values.
        """
        if image is None:
            raise ValueError('image cannot be None')
        if port is None:
            raise ValueError('port cannot be None')
        if any(not isinstance(volume, DockerVolumeMapping) for volume in volumes or []):
            raise TypeError(f'volumes must contain only {DockerVolumeMapping} objects')
        if any(not isinstance(k, str) and isinstance(v, str) for k, v in (env_vars or {}).items()):
            raise TypeError('env_vars must be a str->str dict')
        if any(not isinstance(r, Resource) for r in resources or []):
            raise TypeError(f'resources must contain only {Resource} objects')
        self.__image = str(image)
        self.__port = int(port)
        self.__check_path = str(check_path)
        self.__resources = [deepcopy(e) for e in resources or []]
        self.__volumes = list(volumes) if volumes else []
        self.__env_vars = dict(env_vars) if env_vars is not None else {}
        self.__db_manager_cls = db_manager_cls  # immutable

    @property
    def image(self) -> str:
        """
        The image tag (read-only).
        """
        return self.__image

    @property
    def port(self) -> int:
        """
        The exposed port (read-only).
        """
        return self.__port

    @property
    def check_path(self) -> Optional[str]:
        """
        The URL path to check for whether the microservice is running (read-only).
        """
        return self.__check_path

    @property
    def resources(self) -> Optional[List[Resource]]:
        """
        A list of heaobject.registry.Resource dicts indicating what content types this image is designed for (read-only).
        """
        return deepcopy(self.__resources)

    @property
    def volumes(self) -> List[DockerVolumeMapping]:
        """
        A list of VolumeMapping instances indicating what volumes to map (read-only, never None).
        """
        return copy(self.__volumes)

    @property
    def env_vars(self) -> Dict[str, str]:
        """
        A dict of environment variable names to string values.
        """
        return copy(self.__env_vars)

    @property
    def db_manager_cls(self) -> Optional[type[DatabaseManager]]:
        return self.__db_manager_cls  # immutable

    def start(self, stack: ExitStack) -> DockerContainer:
        """
        Start a container using this image, port number, and volume mappings, connecting to the provided MongoDB
        container for database access, and using the provided HEA Server Registry instance.

        :param stack: the ExitStack to use (required).
        :return: itself, but started.
        """
        container = DockerContainer(self.image)
        for env, val in self.env_vars.items():
            container.with_env(env, val)
        for volume in self.volumes:
            container.with_volume_mapping(volume.host, volume.container, volume.mode)
        container.with_exposed_ports(self.port)
        microservice = stack.enter_context(container)
        return microservice

    def with_env_vars(self, env_vars: Optional[Dict[str, str]]) -> 'DockerContainerConfig':
        """
        Returns a new DockerContainerConfig with the same values as this one, plus any environment variables in the
        env_vars argument.

        :param env_vars: any environment variables.
        :return:
        """
        new_env_vars = self.env_vars
        if env_vars is not None:
            new_env_vars.update(env_vars)
        return DockerContainerConfig(self.image, self.port, self.check_path, self.resources, self.volumes,
                                     new_env_vars, self.db_manager_cls)


@wait_container_is_ready()
def get_exposed_port(container: DockerContainer, port: int) -> int:
    """
    Returns the actual port that the docker container is listening to. It tries getting the port repeatedly until the
    container has sufficiently started to assign the port number.

    :param container: the docker container (required).
    :param port: the port to which the container's application is listening internally.
    :return: the exposed port.
    """
    return container.get_exposed_port(port)


@wait_container_is_ready()
def wait_for_status_code(url, status: int):
    """
    Makes a HTTP GET call to the provided URL repeatedly until the returned status code is equal to the provided code.

    :param url: the URL to call.
    :param status: the status code to check for.
    """
    actual_status = requests.get(url).status_code
    if actual_status != status:
        raise ValueError(f'Expected status {status} and actual status {actual_status}')


@wait_container_is_ready()
def get_bridge_ip(container: DockerContainer) -> str:
    """
    Returns the IP address of the container on the default bridge network.
    :param container: a docker container.
    :return: an IP address.
    """
    return container.get_docker_client().bridge_ip(container.get_wrapped_container().id)


