import json
import logging
import os
import sys
import tempfile
import traceback

from aml_logger import AMLLogger
from appinsights_client import AppInsightsClient
from flask import Flask
from print_hook import PrintHook

from user_script import UserScript, UserScriptError


AML_APP_ROOT = os.environ.get("AML_APP_ROOT", "/var/azureml-app")
AML_SERVER_ROOT = os.environ.get("AML_SERVER_ROOT", os.path.dirname(os.path.realpath(__file__)))
AML_ENTRY_SCRIPT = os.environ.get("AZUREML_ENTRY_SCRIPT")
AML_SOURCE_DIR = os.environ.get("AZUREML_SOURCE_DIRECTORY")

# Amount of time we wait before exiting the application when errors occur for exception log sending
WAIT_EXCEPTION_UPLOAD_IN_SECONDS = 30
SCORING_TIMEOUT_ENV_VARIABLE = "SCORING_TIMEOUT_MS"

sys.path.append(AML_APP_ROOT)

if AML_SOURCE_DIR:
    source_dir = os.path.join(AML_APP_ROOT, AML_SOURCE_DIR)
    sys.path.append(source_dir)


class AMLInferenceApp(Flask):
    appinsights_client: AppInsightsClient
    logger: AMLLogger

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_script = UserScript(AML_ENTRY_SCRIPT)
        self.gen_swagger: bool = False
        self.swagger2 = False
        self.swagger3 = False
        self.swagger2_spec_path = os.path.join(AML_APP_ROOT, "swagger2.json")
        self.swagger3_spec_path = os.path.join(AML_APP_ROOT, "swagger3.json")
        self.scoring_timeout_in_ms = 3600 * 1000

        self._stdout_hook = None
        self._stderr_hook = None

    def _init_logger(self):
        try:
            print("Initializing logger")
            self.logger = AMLLogger()

            logging.getLogger("gunicorn.access").addFilter(lambda record: "GET / HTTP/1." not in record.getMessage())
        except:
            print("logger initialization failed: {0}".format(traceback.format_exc()))
            sys.exit(3)

    def _gen_swagger_json(self, swagger_version, get_input_schema, get_output_schema):
        service_name = os.getenv("SERVICE_NAME", "ML service")
        service_path_prefix = os.getenv("SERVICE_PATH_PREFIX", "")
        service_version = os.getenv("SERVICE_VERSION", "1.0")

        if swagger_version == "3":
            template_file = "swagger3_template.json"
        else:
            template_file = "swagger2_template.json"

        with open(os.path.join(AML_SERVER_ROOT, template_file), "r") as f:
            swagger_spec_str = f.read()

        if service_path_prefix and not service_path_prefix.startswith("/"):
            service_path_prefix = "/{}".format(service_path_prefix)
        service_path_prefix = service_path_prefix.rstrip("/")

        swagger_spec_str = (
            swagger_spec_str.replace("$SERVICE_NAME$", service_name)
            .replace("$SERVICE_VERSION$", service_version)
            .replace("$PATH_PREFIX$", service_path_prefix)
        )

        swagger_spec_json = json.loads(swagger_spec_str)

        run_function = self.user_script.get_run_function()
        input_schema = get_input_schema(run_function)
        output_schema = get_output_schema(run_function)

        if swagger_version == "3":
            swagger_spec_json["components"]["schemas"]["ServiceInput"] = input_schema
            swagger_spec_json["components"]["schemas"]["ServiceOutput"] = output_schema
        else:
            swagger_spec_json["definitions"]["ServiceInput"] = input_schema
            swagger_spec_json["definitions"]["ServiceOutput"] = output_schema

        # Write the swagger json to a temporary file for futher reference.
        # Write to a file in AML_APP_ROOT can fail, if AML_APP_ROOT is read-only.
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as swagger_file:
            print(f"Generating swagger file for version {swagger_version}: {swagger_file.name}")

            if swagger_version == "3":
                self.swagger3_spec_path = swagger_file.name
            else:
                self.swagger2_spec_path = swagger_file.name
            json.dump(swagger_spec_json, swagger_file, indent=4)

        return swagger_spec_json

    def _get_swagger(self, swagger_version):
        try:
            from inference_schema.schema_util import (
                get_input_schema,
                get_output_schema,
                is_schema_decorated,
                get_supported_versions,
            )

            gen_swagger = False
            run_function = self.user_script.get_run_function()
            if is_schema_decorated(run_function):
                gen_swagger = True

            self.gen_swagger = gen_swagger
            # If request swagger version not supported, this will remain None
            if gen_swagger and any(item.startswith(swagger_version) for item in get_supported_versions(run_function)):
                return self._gen_swagger_json(
                    swagger_version=swagger_version,
                    get_input_schema=get_input_schema,
                    get_output_schema=get_output_schema,
                )

        except:
            self.logger.error(
                "Encountered exception while generating swagger file: {0}".format(traceback.format_exc())
            )

        if swagger_version == "3":
            swagger_load_path = self.swagger3_spec_path
        else:
            swagger_load_path = self.swagger2_spec_path

        if os.path.exists(swagger_load_path):
            print(f"Found swagger file for version {swagger_version}: {swagger_load_path}")
            with open(swagger_load_path, "r") as file:
                data = json.load(file)
                print("Swagger file loaded.")
                return data

        return None

    # AML App Insights Wrapper
    def _init_appinsights(self):
        try:
            self.logger.info("Starting up app insights client")
            self.appinsights_client = AppInsightsClient()
            self._stdout_hook = PrintHook(PrintHook.stdout_fd)
            self._stderr_hook = PrintHook(PrintHook.stderr_fd)
        except:
            self.logger.error(
                "Encountered exception while initializing App Insights/Logger {0}".format(traceback.format_exc())
            )
            sys.exit(3)

    def send_exception_to_app_insights(self, request_id="NoRequestId", client_request_id=""):
        if self.appinsights_client is not None:
            self.appinsights_client.send_exception_log(sys.exc_info(), request_id, client_request_id)

    # The default prefix of zeros acts as default request id
    def start_hooks(self, prefix="00000000-0000-0000-0000-000000000000"):
        try:
            if self._stdout_hook is not None:
                self._stdout_hook.start_hook(prefix)
            if self._stderr_hook is not None:
                self._stderr_hook.start_hook(prefix)
        except:
            pass

    def stop_hooks(self):
        try:
            if self._stdout_hook is not None:
                self._stdout_hook.stop_hook()
            if self._stderr_hook is not None:
                self._stderr_hook.stop_hook()
        except:
            pass

    def setup(self):
        # initiliaze logger and app insights
        self._init_logger()
        self._init_appinsights()

        # start the hooks to listen to init print events
        try:
            self.logger.info("Starting up app insight hooks")
            self.start_hooks()
        except:
            self.logger.error("Starting up app insight hooks failed")
            if self.appinsights_client is not None:
                self.appinsights_client.send_exception_log(sys.exc_info())
                self.appinsights_client.wait_for_upload()
            sys.exit(3)

        try:
            self.user_script.load_script(AML_APP_ROOT)
        except UserScriptError:
            # If main is not found, this indicates score script is not in expected location
            if "No module named 'main'" in traceback.format_exc():
                self.logger.error("No score script found. Expected score script main.py.")
                self.logger.error(f"Expected script to be found in PYTHONPATH: {sys.path}")
                if os.path.isdir(AML_APP_ROOT):
                    self.logger.error(f"Current contents of AML_APP_ROOT: {os.listdir(AML_APP_ROOT)}")
                else:
                    self.logger.error(f"The directory {AML_APP_ROOT} not an accessible directory in the container.")

            self.logger.error(traceback.format_exc())
            sys.exit(3)

        try:
            self.user_script.invoke_init()
        except UserScriptError:
            self.logger.error("User's init function failed")
            self.logger.error("Encountered Exception {0}".format(traceback.format_exc()))
            self.appinsights_client.send_exception_log(sys.exc_info())
            self.appinsights_client.wait_for_upload()

            sys.exit(3)

        self.stop_hooks()

        # init debug middlewares deprecated
        if "AML_DBG_MODEL_INFO" in os.environ or "AML_DBG_RESOURCE_INFO" in os.environ:
            self.logger.warning(
                "The debuggability features have been removed. If you have a use case for them please reach out to us."
            )

        # set has_swagger value
        self.swagger3 = self._get_swagger(swagger_version="3")
        self.swagger2 = self._get_swagger(swagger_version="2")

        if SCORING_TIMEOUT_ENV_VARIABLE in os.environ.keys() and self.is_int(os.environ[SCORING_TIMEOUT_ENV_VARIABLE]):
            self.scoring_timeout_in_ms = int(os.environ[SCORING_TIMEOUT_ENV_VARIABLE])
            self.logger.info("Scoring timeout is found from os.environ: {} ms".format(self.scoring_timeout_in_ms))
        else:
            self.logger.info(
                "Scoring timeout setting is not found. Use default timeout: {} ms".format(self.scoring_timeout_in_ms)
            )

    @staticmethod
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False
