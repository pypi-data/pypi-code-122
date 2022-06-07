import inspect
import logging
import os
import sys
from types import ModuleType
from typing import Any, Callable, Dict, NamedTuple, Optional, Union

import flask
from inference_schema.schema_util import is_schema_decorated

from exceptions import AzmlinfsrvError, AzmlAssertionError
from input_parsers import InputParserBase, JsonStringInput, ObjectInput, RawRequestInput
from utils import timeout, Timer


# XXX: Since we didn't configure the root logger, getLogger(__name__) would not write to the right handlers. Here we'll
# reuse the logger that is configured in aml_logger.py, which is the logger named "root". Note that this is not the
# actual root logger (prior to Python 3.9)
logger = logging.getLogger("root")


class UserScriptError(AzmlinfsrvError):
    pass


class UserScriptException(UserScriptError):
    """User script threw an exception."""

    def __init__(self, ex: Exception, message: Optional[str] = None):
        self.user_ex = ex

        message = message or "Caught an unhandled exception from the user script"
        super().__init__(message)


class UserScriptImportException(UserScriptException):
    def __init__(self, ex: Exception):
        super().__init__(ex, "Failed to import user script because it raised an unhandled exception")


class UserScriptTimeout(UserScriptError):
    def __init__(self, timeout_ms: int, elapsed_ms: int):
        super().__init__(f"Script failed to finish execution within the allocated time: {timeout_ms}ms")
        self.timeout_ms = timeout_ms
        self.elapsed_ms = elapsed_ms


class TimedResult(NamedTuple):
    elapsed_ms: int
    input: Dict[str, Any]
    output: Any


class _DummyModule:  # pragma: no cover
    def init(self):
        raise AzmlAssertionError("User script was not loaded before init() is called.")

    def run(self, data):
        raise AzmlAssertionError("User script was not loaded before run() is called.")


class UserScript:
    input_parser: InputParserBase
    _run: Callable

    def __init__(self, entry_script: Optional[str] = None):
        self.entry_script = entry_script
        self.user_module: Union[_DummyModule, ModuleType] = _DummyModule()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.entry_script})"

    def load_script(self, app_root: str) -> None:
        if self.entry_script:
            import importlib.util as imp

            script_location = os.path.join(app_root, self.entry_script.replace("/", os.sep))
            try:
                main_module_spec = imp.spec_from_file_location("entry_module", script_location)
                user_module = imp.module_from_spec(main_module_spec)
                main_module_spec.loader.exec_module(user_module)
            except BaseException as ex:
                raise UserScriptImportException(ex) from ex
        else:
            try:
                import main as user_module
            except BaseException as ex:
                raise UserScriptImportException(ex) from ex

        # For some reason, the SDK generates a proxy script (known as the driver module) to call the customer's actual
        # script. If we detect such script, try to extract the user script from it.
        maybe_user_module = getattr(user_module, "driver_module", None)
        if isinstance(maybe_user_module, ModuleType):
            self.user_module = maybe_user_module
        else:
            self.user_module = user_module

        logger.info(f"Found user script at {self.user_module.__file__}")

        # Ensure the user script has a init() and a run().
        if not hasattr(self.user_module, "init"):
            raise UserScriptError(
                f"User script at {self.user_module.__file__} does not have a init() function defined."
            )
        if not hasattr(self.user_module, "run"):
            raise UserScriptError(
                f"User script at {self.user_module.__file__} does not have a run() function defined."
            )

        self._analyze_run()

    def invoke_init(self) -> None:
        logger.info("Invoking user's init function")
        try:
            self.user_module.init()
        except BaseException as ex:
            raise UserScriptException(ex) from ex

        logger.info("Users's init has completed successfully")

    def invoke_run(self, request: flask.Request, *, timeout_ms: int) -> TimedResult:
        run_parameters = self.input_parser(request)

        # Invoke the user's code with a timeout and a timer.
        timer = None
        try:
            with timeout(timeout_ms), Timer() as timer:
                run_output = self._run(**run_parameters, request_headers=dict(request.headers))
        except TimeoutError:
            # timer may be unset if timeout() threw TimeoutError before Timer() is called. Should probably not happen
            # but not impossible.
            elapsed_ms = timer.elapsed_ms if timer else 0
            raise UserScriptTimeout(timeout_ms, elapsed_ms) from None
        except Exception as ex:
            raise UserScriptException(ex) from ex

        return TimedResult(elapsed_ms=timer.elapsed_ms, input=run_parameters, output=run_output)

    def _analyze_run(self) -> None:
        # Import this module after we've patched azureml.contrib.services in _patch_azureml_contrib_services()
        from azureml.contrib.services import aml_request

        # Inspect the user's run() function. Make sure it is declared in the right way.
        run_params = list(inspect.signature(self.user_module.run).parameters.values())
        if any(param.kind not in [param.KEYWORD_ONLY, param.POSITIONAL_OR_KEYWORD] for param in run_params):
            raise UserScriptError("run() cannot accept positional-only arguments, *args, or **kwargs.")

        # Create a thin wrapper for user's run that always accepts the request_headers parameter.
        param_names = [run_param.name for run_param in run_params]
        try:
            param_names.remove("request_headers")
            self._run = self.user_module.run
        except ValueError:
            self._run = lambda request_headers, **kwargs: self.user_module.run(**kwargs)

        # Decide the input parser we need for user's run() function.
        if aml_request._rawHttpRequested and is_schema_decorated(self.user_module.run):
            raise UserScriptError("run() cannot be decorated with both @rawhttp and @input_schema")
        elif aml_request._rawHttpRequested:
            if len(param_names) != 1:
                raise UserScriptError(
                    'run() is decorated with @rawhttp. It needs to accept an argument that is not "request_headers".'
                )

            self.input_parser = RawRequestInput(param_names[0])
            logger.info("run() is decorated with @rawhttp. Server will invoke it with the flask request object.")
        elif is_schema_decorated(self.user_module.run):
            if len(param_names) == 0:
                raise UserScriptError("run() is decorated with @input_schema but doesn't take any inputs.")

            self.input_parser = ObjectInput(param_names)
            logger.info(
                "run() is decorated with @input_schema. Server will invoke it with the following arguments: "
                f"{', '.join(param_name for param_name in param_names)}."
            )
        else:
            if len(param_names) != 1:
                raise UserScriptError(
                    'run() is not decorated. It needs to accept an argument that is not "request_headers".'
                )

            self.input_parser = JsonStringInput(param_names[0])
            logger.info("run() is not decorated. Server will invoke it with the input in JSON string.")

    def get_run_function(self) -> callable:
        return self.user_module.run


def _patch_azureml_contrib_services():
    # TODO: Move this to __init__.py once we have one.

    # override the azureml.contrib.services package with local one, meanwhile keep the other stuff under azureml.*
    # untouched note this must be done prior to importing the package in app logic
    import azureml.contrib.services.aml_request
    import azureml_contrib_services.aml_request

    # works for 'import azureml.contrib.services.aml_request'
    sys.modules["azureml.contrib.services"].aml_request = sys.modules["azureml_contrib_services"].aml_request
    # works for 'from azureml.contrib.services.aml_request import *'
    sys.modules["azureml.contrib.services.aml_request"] = sys.modules["azureml_contrib_services.aml_request"]

    import azureml.contrib.services.aml_response
    import azureml_contrib_services.aml_response

    # works for 'import azureml.contrib.services.aml_response'
    sys.modules["azureml.contrib.services"].aml_response = sys.modules["azureml_contrib_services"].aml_response
    # works for 'from azureml.contrib.services.aml_response import *'
    sys.modules["azureml.contrib.services.aml_response"] = sys.modules["azureml_contrib_services.aml_response"]


_patch_azureml_contrib_services()
