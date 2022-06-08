import click
import logging
import re
from imagination import container

from dnastack.cli.utils import command, echo_result, echo_dict_in_table
from dnastack.common.events import Event
from dnastack.common.logger import get_logger
from dnastack.configuration.models import ServiceEndpoint
from dnastack.context.manager import ContextManager
from dnastack.http.authenticators.abstract import AuthState, AuthStateStatus


@click.group("contexts")
def context_command_group():
    pass


@command(context_command_group)
def use(hostname: str, no_auth: bool = False):
    """
    Import a configuration from host's service registry (if available) or the corresponding public configuration from
    cloud storage. If "--no-auth" is not defined, it will automatically initiate all authentication.

    This will also switch the default context to the given hostname.
    """
    ContextCommandHandler().use(hostname, no_auth=no_auth)


class ContextCommandHandler:
    _re_http_scheme = re.compile(r'^https?://')

    __emoji_map = {
        'add': '+',
        'update': '●',
        'keep': 'o',
        'remove': 'x',
    }

    __output_color_map = {
        'add': 'green',
        'update': 'magenta',
        'keep': 'yellow',
        'remove': 'red',
    }

    _status_color_map = {
        AuthStateStatus.READY: 'green',
        AuthStateStatus.UNINITIALIZED: 'magenta',
        AuthStateStatus.REFRESH_REQUIRED: 'yellow',
        AuthStateStatus.REAUTH_REQUIRED: 'red',
    }

    def __init__(self):
        self._logger = get_logger(type(self).__name__, logging.DEBUG)
        self._context_manager: ContextManager = container.get(ContextManager)
        self._context_manager.events.on('context-sync', self.__handle_sync_event)
        self._context_manager.events.on('auth-begin', self._handle_auth_begin)
        self._context_manager.events.on('auth-end', self._handle_auth_end)

    def use(self, hostname: str, no_auth: bool = False):
        self._context_manager.use(hostname, no_auth)
        echo_result('Context', 'green', 'use', hostname)

    def __handle_sync_event(self, event: Event):
        action: str = event.details['action']
        endpoint: ServiceEndpoint = event.details['endpoint']

        echo_result(
            'Endpoint',
            self.__output_color_map[action],
            action,
            f'{endpoint.id} ({endpoint.type.group}:{endpoint.type.artifact}:{endpoint.type.version}) at {endpoint.url}',
            self.__emoji_map[action]
        )

    def _handle_auth_begin(self, event: Event):
        session_id = event.details['session_id']
        state: AuthState = event.details['state']

        if state.status != AuthStateStatus.READY:
            echo_result('Session',
                        'yellow',
                        'initializing',
                        f'Session {session_id}',
                        ' ')

    def _handle_auth_end(self, event: Event):
        session_id = event.details['session_id']
        state: AuthState = event.details['state']
        echo_result('Session',
                    self._status_color_map[state.status],
                    state.status,
                    f'Session {session_id}',
                    '●' if state.status == AuthStateStatus.READY else 'x')

        echo_dict_in_table(state.auth_info, left_padding_size=18)