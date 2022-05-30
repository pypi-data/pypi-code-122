"""Provide non-CDN-dependent Swagger & Redoc pages to FastAPI"""
from pathlib import Path
from typing import Any, Optional, TYPE_CHECKING
from fastapi import FastAPI, Request
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

if TYPE_CHECKING:
    from fastapi import Response  # pragma: no cover

_STATIC_PATH = Path(__file__).parent / "static"


def FastAPIOffline(
    docs_url: Optional[str] = "/docs",
    redoc_url: Optional[str] = "/redoc",
    *args: Any,
    **kwargs: Any,
) -> FastAPI:
    """Return a FastAPI obj that doesn't rely on CDN for the documentation page"""
    # Disable the normal doc & redoc pages
    kwargs["docs_url"] = None
    kwargs["redoc_url"] = None

    # Grab the user specified favicon url (if present)
    favicon_url = kwargs.pop("favicon_url", None)

    # Create the FastAPI object
    app = FastAPI(*args, **kwargs)

    # This mostly just keeps mypy happy
    assert isinstance(app.openapi_url, str)
    assert isinstance(app.swagger_ui_oauth2_redirect_url, str)

    openapi_url = app.openapi_url
    swagger_ui_oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url

    # Set up static file mount
    app.mount(
        "/static-offline-docs",
        StaticFiles(directory=_STATIC_PATH.as_posix()),
        name="static-offline-docs",
    )

    if docs_url is not None:
        # Define the doc and redoc pages, pointing at the right files
        @app.get(docs_url, include_in_schema=False)
        async def custom_swagger_ui_html(request: Request) -> "Response":
            root = request.scope.get("root_path")

            if favicon_url is None:
                favicon = f"{root}/static-offline-docs/favicon.png"
            else:
                favicon = favicon_url

            return get_swagger_ui_html(
                openapi_url=f"{root}{openapi_url}",
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
                swagger_js_url=f"{root}/static-offline-docs/swagger-ui-bundle.js",
                swagger_css_url=f"{root}/static-offline-docs/swagger-ui.css",
                swagger_favicon_url=favicon,
            )

        @app.get(swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect() -> "Response":
            return get_swagger_ui_oauth2_redirect_html()

    if redoc_url is not None:

        @app.get(redoc_url, include_in_schema=False)
        async def redoc_html(request: Request) -> "Response":
            root = request.scope.get("root_path")

            if favicon_url is None:
                favicon = f"{root}/static-offline-docs/favicon.png"
            else:
                favicon = favicon_url

            return get_redoc_html(
                openapi_url=f"{root}{openapi_url}",
                title=app.title + " - ReDoc",
                redoc_js_url=f"{root}/static-offline-docs/redoc.standalone.js",
                with_google_fonts=False,
                redoc_favicon_url=favicon,
            )

    # Return the FastAPI object
    return app
