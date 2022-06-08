from json import JSONDecodeError

import re
import requests
from imagination.decorator import service
from typing import Optional, Callable
from urllib.parse import urljoin, urlparse

from dnastack.auth.manager import AuthManager
from dnastack.client.service_registry.client import ServiceRegistry
from dnastack.client.service_registry.factory import ClientFactory
from dnastack.client.service_registry.manager import ServiceRegistryManager
from dnastack.common.events import EventSource, EventRelay
from dnastack.common.logger import get_logger
from dnastack.configuration.manager import ConfigurationManager
from dnastack.configuration.models import ServiceEndpoint, Context, Configuration


@service.registered()
class ContextManager:
    _re_http_scheme = re.compile(r'^https?://')
    _logger = get_logger('ContextManager')

    def __init__(self, config_manager: ConfigurationManager):
        self._config_manager = config_manager
        self.__events = EventSource(['context-sync', 'auth-begin', 'auth-disabled', 'auth-end'])

    @property
    def events(self):
        return self.__events

    def use(self, hostname: str, no_auth: Optional[bool] = False) -> Optional[ClientFactory]:
        base_url = hostname if self._re_http_scheme.search(hostname) else f'https://{hostname}'
        context_name = urlparse(base_url).netloc

        config = self._config_manager.load()
        context = config.contexts.get(context_name)

        # noinspection PyUnusedLocal
        factory: Optional[ClientFactory] = None

        if context:
            if context.auto_sync:
                factory = self._use_registry(config,
                                             context_name,
                                             lambda srm, sr: srm.synchronize_endpoints(sr.endpoint.id))
            else:
                self._logger.debug(f'C/{context_name}: Auto-sync disabled')
                factory = None
        else:
            config.contexts[context_name] = Context(auto_sync=True)

            factory = self._use_registry(config,
                                         context_name,
                                         lambda srm, sr: srm.add_registry_and_import_endpoints(sr.endpoint.id,
                                                                                               sr.endpoint.url))

        # Set the current context.
        config.current_context = context_name

        # Save it to the configuration file.
        self._config_manager.save(config)

        if no_auth:
            self.events.dispatch('auth-disabled', dict())
        else:
            auth_manager = AuthManager(config)

            # Set up an event relay.
            self.events.relay_from(auth_manager.events, 'auth-begin')
            self.events.relay_from(auth_manager.events, 'auth-end')

            auth_manager.initiate_authentications()

        return factory

    def _use_registry(self,
                      config: Configuration,
                      context_name: str,
                      sync_operation: Callable[[ServiceRegistryManager, ServiceRegistry], None]) -> ClientFactory:
        registry = self.registry(context_name)
        if not registry:
            # TODO #182289347 Look up for a public sync config (Cloud Storage or GitHub public repo)
            #  in case that the registry.
            raise NotImplementedError('Public sync configuration')

        # Instantiate the manager.
        reg_manager = ServiceRegistryManager(config, context_name)

        # The name of the context is the same as the ID of the service registry.
        reg_manager.events.on('endpoint-sync', lambda e: self.events.dispatch('context-sync', e))

        # Trigger sync operation
        sync_operation(reg_manager, registry)

        return ClientFactory.use(registry.endpoint)



    @classmethod
    def registry(cls, hostname: str) -> Optional[ServiceRegistry]:
        # Scan the service for the list of service info.
        base_url = hostname if cls._re_http_scheme.search(hostname) else f'https://{hostname}'
        context_name = urlparse(base_url).netloc

        target_registry_url: Optional[str] = None

        # Base-registry-URL-to-listing-URL map
        potential_registry_base_paths = [
            # This is for a service which implements the service registry at root.
            '/',

            # This is for a collection service.
            '/service-registry/',

            # This is for an explorer service, e.g., viral.ai.
            '/api/service-registry/',
        ]

        for api_path in potential_registry_base_paths:
            registry_url = urljoin(base_url, api_path)
            listing_url = urljoin(registry_url, 'services')

            try:
                response = requests.get(listing_url, headers={'Accept': 'application/json'})
            except requests.exceptions.ConnectionError:
                continue

            if response.ok:
                try:
                    ids = sorted([entry['id'] for entry in response.json()])
                    cls._logger.debug(f'CHECK: IDS => {", ".join(ids)}')
                except JSONDecodeError:
                    # Look for the next one.
                    continue

                target_registry_url = registry_url

                break
            # end: if

        if target_registry_url:
            return ServiceRegistry.make(ServiceEndpoint(id=context_name, url=target_registry_url))
        else:
            return None
