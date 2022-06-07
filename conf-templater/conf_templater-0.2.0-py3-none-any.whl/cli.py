from typing import Any, Optional

from .console import parse_console_arguments
from .template import render_config_template

__all__ = [
    'template_config',
]


def template_config(
    package: Optional[str] = None,
    subpath: Optional[str] = None,
    **render_options: Any,
) -> None:
    args = parse_console_arguments(package=package, subpath=subpath)
    render_config_template(
        package if package is not None else args['package'],
        subpath if subpath is not None else args['subpath'],
        args['template_name'],
        args['output_filepath'],
        args['config_options'],
        **render_options,
    )
