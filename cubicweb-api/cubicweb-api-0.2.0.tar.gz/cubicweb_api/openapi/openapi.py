from os import path
from pyramid.config import Configurator
from cubicweb_api.constants import API_ROUTE_PREFIX
from cubicweb_api.httperrors import get_http_error, get_http_500_error
from pyramid_openapi3 import (
    RequestValidationError,
    ResponseValidationError,
    openapi_validation_error,
)
from typing import Union
from pyramid.request import Request
from pyramid.response import Response
import logging

log = logging.getLogger(__name__)


def register_openapi_routes(config: Configurator):
    config.include("pyramid_openapi3")
    # TODO block access if anonymous access is disabled and user is not connected
    config.pyramid_openapi3_spec(
        f"{path.dirname(__file__)}/openapi.yaml",
        route=f"{API_ROUTE_PREFIX}openapi.yaml",
    )
    config.pyramid_openapi3_add_explorer(route=f"{API_ROUTE_PREFIX}openapi")
    config.registry.settings["pyramid_openapi3.enable_endpoint_validation"] = True
    config.registry.settings["pyramid_openapi3.enable_request_validation"] = True
    # Do not validate responses as it could slow down the server
    config.registry.settings["pyramid_openapi3.enable_response_validation"] = False
    config.add_exception_view(
        view=custom_openapi_validation_error, context=RequestValidationError
    )
    config.add_exception_view(
        view=custom_openapi_validation_error, context=ResponseValidationError
    )


def custom_openapi_validation_error(
    context: Union[RequestValidationError, ResponseValidationError], request: Request
) -> Response:
    """Overrides default pyramid_openapi3 errors to match the API format."""
    error_response = openapi_validation_error(context, request)

    status = error_response.status_code
    body = error_response.json_body
    if status == 500:
        return get_http_500_error()
    if status == 400:
        return get_http_error(
            error_response.status_code,
            "OpenApiValidationError",
            "Your request could not be validated against the openapi specification.",
            body,
        )

    return get_http_error(error_response.status_code, "OpenAPI Error", "", body)
