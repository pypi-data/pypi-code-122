#
# MIT License
#
# Copyright (c) 2022 KuFlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.#


import logging
from uuid import UUID

from frozendict import frozendict
import kuflow_rest_client
from kuflow_rest_client.api import task_api
from kuflow_rest_client.model.delete_element_command import DeleteElementCommand
from kuflow_rest_client.model.delete_element_value_document_command import (
    DeleteElementValueDocumentCommand,
)
from kuflow_rest_client.model.principal_type import PrincipalType
from kuflow_rest_client.model.log import Log
from kuflow_rest_client.model.log_level import LogLevel
from kuflow_rest_client.model.save_element_value_document_command import (
    SaveElementValueDocumentCommand,
)
from robot.api.deco import keyword

from robot.utils import (is_list_like, is_number, is_string, type_name, is_dict_like)
from kuflow_rest_client.model.task_element_value_or_array_value import TaskElementValueOrArrayValue

from kuflow_rest_client.model.task_element_value_principal_item import TaskElementValuePrincipalItem
from kuflow_rest_client.model.task_element_value_principal import TaskElementValuePrincipal
from kuflow_rest_client.model.task_element_value_string import TaskElementValueString
from kuflow_rest_client.model.task_element_value_number import TaskElementValueNumber
from kuflow_rest_client.model.task_element_value_type import TaskElementValueType
from kuflow_rest_client.model.task_element_value_object import TaskElementValueObject
from kuflow_rest_client.model.task_element_value_document_item import TaskElementValueDocumentItem
from kuflow_rest_client.model.task_element_value_document import TaskElementValueDocument


class Keywords:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._client_configuration = None

    @keyword(tags=("settings",))
    def set_client_authentication(self, endpoint, identifier, token):
        """Configure the client authentication in order to execute keywords against Rest API.

        Before using any other KuFlow Keyword, this one must be called.

        Example:
        | Set Client Authentication | %{KUFLOW_API_ENDPOINT} | %{KUFLOW_APPLICATION_IDENTIFIER} | %{KUFLOW_APPLICATION_TOKEN}
        =>
        | Set Client Authentication | https://api.kuflow.com/v1.0 | identifier | token
        """
        self._client_configuration = kuflow_rest_client.Configuration(
            host=endpoint,
            username=identifier,
            password=token,
        )

    @keyword()
    def append_log_message(self, task_id: UUID, message: str, level=LogLevel.INFO):
        """Add a log entry to the task

        If the number of log entries is reached, the oldest log entry is removed.
        The level of log can be INFO, WARN or ERROR.

        Example:
        | Append Log Message | ${TASK_ID} | ${MESSAGE}
        | Append Log Message | ${TASK_ID} | ${MESSAGE} | level=${LEVEL}
        =>
        | Append Log Message | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My info message
        | Append Log Message | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | My warning message | level=WARN
        """

        body = Log(
            message=message,
            level=level,
        )

        self._do_append_log_request(task_id, body)

    @keyword()
    def save_element_document(self, task_id: UUID, code: str, path: str, id: UUID = None):
        """Save a element of type document

        Allow to save an element document uploading the content.

        If it is a multiple element, and the documentId does not exist or is empty, the document will be added to
        the element.
        If the element already exists (the Id referenced in the body corresponds to an existing one), it updates it.

        Example:
        | Save Element Document | ${TASK_ID} | ${CODE} | ${PATH}
        =>
        | Save Element Document | ${TASK_ID} | ELEMENT_KEY | hello.jpg
        | Save Element Document | ${TASK_ID} | ELEMENT_KEY | hello.jpg | a05f197f-a50a-46d5-bdec-29a0c020f0d7
        """

        if id is not None:
            command = SaveElementValueDocumentCommand(
                code=code,
                id=id
            )
        else:
            command = SaveElementValueDocumentCommand(
                code=code
            )

        body = dict(
            json=command,
            file=open(path, "rb"),
        )

        self._do_save_element_document_request(task_id, body)

    @keyword()
    def save_element(self, task_id: UUID, code: str, *value, valid=True):
        """Save a element

        Allow to save an element i.e., a field, a decision, a form, a principal or document.

        If values already exist for the provided element code, it replaces them with the new ones,
        otherwise it creates them.
        The values of the previous elements that no longer exist will be deleted.
        To remove an element, use the appropriate API method.

        Type of arguments in keywords and KuFlow elements:
            - String:
                By default, plain argument in keywords are of type String.

            - Number:
                You can use the built-in keywords 'Convert To Integer', 'Convert To Number' or others
                to pass a numeric type element.

        Object Elements (aka Forms Elements in KuFlow):
            You must pass an argument of type dictionary. You can use the built-in keyword
            Create Dictionary or others as utilities.

        Principal Elements:
            The keyword 'Convert To Element Value Principal Item' will allow you to create a Principal
            object that you can use as an argument.

        Document Elements:
            To save a document you need to pass a document reference using the 'id' attribute.
            To upload a new file, please use the 'Save Element Document' keyword.
            The keyword 'Convert To Element Value Document Item' will allow you to create a Principal
            object that you can use as an argument. The identifier of the documents follows the following
            format: ku:task/{taskId}/element-value/{elementValueId}

        Multivalues elements:
            For those elements that have been defined as multiple, you can pass a variable list
            of arguments to the keyword.

        Valid flag for elements:
            When saving an element, it is possible to specify if its value is valid or not,
            which allows it to be shown in the KuFlow UI as a validated element or not. To do this
            you must use the Valid=Boolean parameter. Note that in RobotFramework format the default
            type of parameters is String, so you must write Valid=${False}. By default, all items
            are valid when saved. Similarly, for multi-evaluated elements, the value of the "valid"
            parameter applies to all values.

        Example:
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE}
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE} | ${VALID}
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE_1} | ${VALUE_2} | ${VALUE_3}
        | Save Element | ${TASK_ID} | ${CODE} | ${VALUE_1} | ${VALUE_2} | ${VALUE_3} | ${VALID}
        =>
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | Value
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | Value | ${False}
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | Value 1 | Value 2 | Value 3 | ${False}
        |
        | ${result} = Convert To Integer    123
        | Save Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY | ${result}
        |
        | ${result_one} = Convert To Integer | 123
        | ${result_two} = Convert To Number |  123.123
        | Save Element | ${TASK_ID} | FIELD | ${result_one} | ${result_two}
        |
        | ${result} = Convert To Element Value Principal Item    7dd16e94-2dac-4fca-931e-c2505baa695c
        | Save Element | ${TASK_ID} | FIELD | ${result}
        |
        | &{result_one} = Create Dictionary | one_key=My Example Value One | two_key=2
        | &{result_two} = Create Dictionary | a_key=My Example Value A | b_key=B
        | Save Element | ${TASK_ID} | FIELD | ${result_one} | ${result_two}
        |
        | ${result} = Convert To Element Value Document Item    ku:task/acdca56f-b8aa-46c8-9055-8ee52810a4a9/element-value/a05f197f-a50a-46d5-bdec-29a0c020f0d7
        | Save Element | ${TASK_ID} | FIELD | ${result}
        """
        if not is_list_like(value):
            raise TypeError("Expected argument to be a list or list-like, "
                            "got %s instead." % (type_name(value)))

        target = []
        for v in value:
            element = None

            if is_string(v):
                element = frozendict(self._convert_to_element_value_string(v, valid=valid))
            elif is_number(v):
                element = frozendict(self._convert_to_element_value_number(v, valid=valid))
            elif isinstance(v, TaskElementValuePrincipalItem):
                element = frozendict(self._convert_to_element_value_principal(v, valid=valid))
            elif isinstance(v, TaskElementValueDocumentItem):
                element = frozendict(self._convert_to_element_value_document(v, valid=valid))
            elif is_dict_like(v):
                element = frozendict(self._convert_to_element_value_object(v, valid=valid))
            else:
                element = frozendict(self._convert_to_element_value_string(v, valid=valid))

            target.append(element)

        body = TaskElementValueOrArrayValue(
            code=code,
            value=target,
        )

        self._do_save_element_request(task_id, body)

    @keyword()
    def delete_element_document(self, task_id: UUID, id: UUID):
        """Delete an element document value

        Allow to delete a specific document from an element of document type using its Id.

        Note: If it is a multiple item, it will only delete the specified document. If it is a single element,
        in addition to the document, it will also delete the element.

        Example:
        | Delete Element Document | ${TASK_ID} | ${ID}
        =>
        | Delete Element Document | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ac951e9f-c194-445b-9eec-4a800b25fb56
        """

        body = DeleteElementValueDocumentCommand(
            documentId=id,
        )

        self._do_delete_element_document(task_id, body)

    @keyword()
    def delete_element(self, task_id: UUID, code: str):
        """Delete an element by code

        Allow to delete task element by specifying the item definition code.

        Remove all values of the selected element.

        Example:
        | Delete Element | ${TASK_ID} | ${CODE}
        =>
        | Delete Element | d9729dc3-10ee-4ed9-91ca-c10e6a6d13ec | ELEMENT_KEY
        """

        body = DeleteElementCommand(
            code=code,
        )

        self._do_delete_element(task_id, body)

    @keyword()
    def convert_to_element_value_principal_item(self, id: UUID):
        """Convert to element value principal item

        Given an Id of a Principal user, create an item that represents a reference to the Principal. Then can be used
        as a value in the kewyord 'Save Element'.

        Example:
        | Convert To Element Value Principal Item  | ${PRINCIPAL_ID}
        =>
        | Convert To Element Value Principal Item  | 7dd16e94-2dac-4fca-931e-c2505baa695c
        """
        return TaskElementValuePrincipalItem(id=id, type=PrincipalType.USER)

    @keyword()
    def convert_to_element_value_document_item(self, uri: str):
        """Convert to element value principal item

        Given an Id of a Document or the Reference of a Document, create an item that represents a reference to the
        Document elementand can be used. Then can be used as a value in the kewyord 'Save Element'.

        Example:
        | Convert To Element Value Document Item  | ${ID}
        | Convert To Element Value Document Item  | ${ID} | ${DOCUMENT_URI}
        =>
        | Convert To Element Value Document Item  | ku:task/acdca56f-b8aa-46c8-9055-8ee52810a4a9/element-value/a05f197f-a50a-46d5-bdec-29a0c020f0d7
        """
        return TaskElementValueDocumentItem(
            uri=uri,
        )

    def _convert_to_element_value_string(self, value, valid=True):
        return TaskElementValueString(value=value, type=TaskElementValueType.STRING, valid=valid)

    def _convert_to_element_value_number(self, value, valid=True):
        return TaskElementValueNumber(value=value, type=TaskElementValueType.NUMBER, valid=valid)

    def _convert_to_element_value_object(self, value, valid=True):
        fdict = frozendict(value)
        return TaskElementValueObject(value=fdict, type=TaskElementValueType.OBJECT, valid=valid)

    def _convert_to_element_value_principal(self, value, valid=True):
        return TaskElementValuePrincipal(value=value, type=TaskElementValueType.PRINCIPAL, valid=valid)

    def _convert_to_element_value_document(self, value, valid=True):
        return TaskElementValueDocument(value=value, type=TaskElementValueType.DOCUMENT, valid=valid)

    def _do_save_element_document_request(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                api_instance.actions_save_element_value_document(
                    path_params=path_params,
                    body=body,
                )
            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling KuFlow->TaskApi->actions_save_element_document: %s\n"
                    % e
                )
                raise e

    def _do_append_log_request(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                api_instance.actions_append_log(
                    path_params=path_params,
                    body=body,
                )

            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling KuFlow->TaskApi->actions_append_log: %s\n"
                    % e
                )
                raise e

    def _do_save_element_request(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                api_instance.actions_save_element(
                    path_params=path_params,
                    body=body,
                )

            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling TaskApi->actions_save_element: %s\n" % e
                )
                raise e

    def _do_delete_element_document(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                api_instance.actions_delete_value_document(
                    path_params=path_params,
                    body=body,
                )

            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling KuFlow->TaskApi->actions_delete_document: %s\n"
                    % e
                )
                raise e

    def _do_delete_element(self, task_id, body):
        with kuflow_rest_client.ApiClient(self._client_configuration) as api_client:
            api_instance = task_api.TaskApi(api_client)

            path_params = {
                "id": task_id,
            }

            try:
                api_instance.actions_delete_element(
                    path_params=path_params,
                    body=body,
                )

            except kuflow_rest_client.ApiException as e:
                self.logger.error(
                    "Exception when calling KuFlow->TaskApi->actions_delete_element: %s\n"
                    % e
                )
                raise e
