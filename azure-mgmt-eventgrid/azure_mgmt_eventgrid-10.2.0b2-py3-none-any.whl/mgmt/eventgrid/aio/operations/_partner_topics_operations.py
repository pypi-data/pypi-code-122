# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, AsyncIterable, Callable, Dict, Optional, TypeVar, Union

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.polling import AsyncLROPoller, AsyncNoPolling, AsyncPollingMethod
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.mgmt.core.exceptions import ARMErrorFormat
from azure.mgmt.core.polling.async_arm_polling import AsyncARMPolling

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._partner_topics_operations import build_activate_request, build_create_or_update_request, build_deactivate_request, build_delete_request_initial, build_get_request, build_list_by_resource_group_request, build_list_by_subscription_request, build_update_request
T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class PartnerTopicsOperations:
    """PartnerTopicsOperations async operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure.mgmt.eventgrid.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = _models

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    @distributed_trace_async
    async def get(
        self,
        resource_group_name: str,
        partner_topic_name: str,
        **kwargs: Any
    ) -> "_models.PartnerTopic":
        """Get a partner topic.

        Get properties of a partner topic.

        :param resource_group_name: The name of the resource group within the user's subscription.
        :type resource_group_name: str
        :param partner_topic_name: Name of the partner topic.
        :type partner_topic_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PartnerTopic, or the result of cls(response)
        :rtype: ~azure.mgmt.eventgrid.models.PartnerTopic
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.PartnerTopic"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str

        
        request = build_get_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            partner_topic_name=partner_topic_name,
            api_version=api_version,
            template_url=self.get.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('PartnerTopic', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics/{partnerTopicName}"}  # type: ignore


    @distributed_trace_async
    async def create_or_update(
        self,
        resource_group_name: str,
        partner_topic_name: str,
        partner_topic_info: "_models.PartnerTopic",
        **kwargs: Any
    ) -> "_models.PartnerTopic":
        """Create a partner topic.

        Asynchronously creates a new partner topic with the specified parameters.

        :param resource_group_name: The name of the resource group within the user's subscription.
        :type resource_group_name: str
        :param partner_topic_name: Name of the partner topic.
        :type partner_topic_name: str
        :param partner_topic_info: Partner Topic information.
        :type partner_topic_info: ~azure.mgmt.eventgrid.models.PartnerTopic
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PartnerTopic, or the result of cls(response)
        :rtype: ~azure.mgmt.eventgrid.models.PartnerTopic
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.PartnerTopic"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(partner_topic_info, 'PartnerTopic')

        request = build_create_or_update_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            partner_topic_name=partner_topic_name,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.create_or_update.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if response.status_code == 200:
            deserialized = self._deserialize('PartnerTopic', pipeline_response)

        if response.status_code == 201:
            deserialized = self._deserialize('PartnerTopic', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_or_update.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics/{partnerTopicName}"}  # type: ignore


    async def _delete_initial(  # pylint: disable=inconsistent-return-statements
        self,
        resource_group_name: str,
        partner_topic_name: str,
        **kwargs: Any
    ) -> None:
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str

        
        request = build_delete_request_initial(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            partner_topic_name=partner_topic_name,
            api_version=api_version,
            template_url=self._delete_initial.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 202, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})

    _delete_initial.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics/{partnerTopicName}"}  # type: ignore


    @distributed_trace_async
    async def begin_delete(  # pylint: disable=inconsistent-return-statements
        self,
        resource_group_name: str,
        partner_topic_name: str,
        **kwargs: Any
    ) -> AsyncLROPoller[None]:
        """Delete a partner topic.

        Delete existing partner topic.

        :param resource_group_name: The name of the resource group within the user's subscription.
        :type resource_group_name: str
        :param partner_topic_name: Name of the partner topic.
        :type partner_topic_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :keyword str continuation_token: A continuation token to restart a poller from a saved state.
        :keyword polling: By default, your polling method will be AsyncARMPolling. Pass in False for
         this operation to not poll, or pass in your own initialized polling object for a personal
         polling strategy.
        :paramtype polling: bool or ~azure.core.polling.AsyncPollingMethod
        :keyword int polling_interval: Default waiting time between two polls for LRO operations if no
         Retry-After header is present.
        :return: An instance of AsyncLROPoller that returns either None or the result of cls(response)
        :rtype: ~azure.core.polling.AsyncLROPoller[None]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str
        polling = kwargs.pop('polling', True)  # type: Union[bool, AsyncPollingMethod]
        cls = kwargs.pop('cls', None)  # type: ClsType[None]
        lro_delay = kwargs.pop(
            'polling_interval',
            self._config.polling_interval
        )
        cont_token = kwargs.pop('continuation_token', None)  # type: Optional[str]
        if cont_token is None:
            raw_result = await self._delete_initial(
                resource_group_name=resource_group_name,
                partner_topic_name=partner_topic_name,
                api_version=api_version,
                cls=lambda x,y,z: x,
                **kwargs
            )
        kwargs.pop('error_map', None)

        def get_long_running_output(pipeline_response):
            if cls:
                return cls(pipeline_response, None, {})


        if polling is True: polling_method = AsyncARMPolling(lro_delay, **kwargs)
        elif polling is False: polling_method = AsyncNoPolling()
        else: polling_method = polling
        if cont_token:
            return AsyncLROPoller.from_continuation_token(
                polling_method=polling_method,
                continuation_token=cont_token,
                client=self._client,
                deserialization_callback=get_long_running_output
            )
        return AsyncLROPoller(self._client, raw_result, get_long_running_output, polling_method)

    begin_delete.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics/{partnerTopicName}"}  # type: ignore

    @distributed_trace_async
    async def update(
        self,
        resource_group_name: str,
        partner_topic_name: str,
        partner_topic_update_parameters: "_models.PartnerTopicUpdateParameters",
        **kwargs: Any
    ) -> Optional["_models.PartnerTopic"]:
        """Update a partner topic.

        Asynchronously updates a partner topic with the specified parameters.

        :param resource_group_name: The name of the resource group within the user's subscription.
        :type resource_group_name: str
        :param partner_topic_name: Name of the partner topic.
        :type partner_topic_name: str
        :param partner_topic_update_parameters: PartnerTopic update information.
        :type partner_topic_update_parameters:
         ~azure.mgmt.eventgrid.models.PartnerTopicUpdateParameters
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PartnerTopic, or the result of cls(response)
        :rtype: ~azure.mgmt.eventgrid.models.PartnerTopic or None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType[Optional["_models.PartnerTopic"]]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str
        content_type = kwargs.pop('content_type', "application/json")  # type: Optional[str]

        _json = self._serialize.body(partner_topic_update_parameters, 'PartnerTopicUpdateParameters')

        request = build_update_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            partner_topic_name=partner_topic_name,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.update.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = None
        if response.status_code == 201:
            deserialized = self._deserialize('PartnerTopic', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    update.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics/{partnerTopicName}"}  # type: ignore


    @distributed_trace
    def list_by_subscription(
        self,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.PartnerTopicsListResult"]:
        """List partner topics under an Azure subscription.

        List all the partner topics under an Azure subscription.

        :param filter: The query used to filter the search results using OData syntax. Filtering is
         permitted on the 'name' property only and with limited number of OData operations. These
         operations are: the 'contains' function as well as the following logical operations: not, and,
         or, eq (for equal), and ne (for not equal). No arithmetic operations are supported. The
         following is a valid filter example: $filter=contains(namE, 'PATTERN') and name ne 'PATTERN-1'.
         The following is not a valid filter example: $filter=location eq 'westus'. Default value is
         None.
        :type filter: str
        :param top: The number of results to return per page for the list operation. Valid range for
         top parameter is 1 to 100. If not specified, the default number of results to be returned is 20
         items per page. Default value is None.
        :type top: int
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either PartnerTopicsListResult or the result of
         cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.eventgrid.models.PartnerTopicsListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.PartnerTopicsListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_by_subscription_request(
                    subscription_id=self._config.subscription_id,
                    api_version=api_version,
                    filter=filter,
                    top=top,
                    template_url=self.list_by_subscription.metadata['url'],
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                
                request = build_list_by_subscription_request(
                    subscription_id=self._config.subscription_id,
                    api_version=api_version,
                    filter=filter,
                    top=top,
                    template_url=next_link,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("PartnerTopicsListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list_by_subscription.metadata = {'url': "/subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/partnerTopics"}  # type: ignore

    @distributed_trace
    def list_by_resource_group(
        self,
        resource_group_name: str,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.PartnerTopicsListResult"]:
        """List partner topics under a resource group.

        List all the partner topics under a resource group.

        :param resource_group_name: The name of the resource group within the user's subscription.
        :type resource_group_name: str
        :param filter: The query used to filter the search results using OData syntax. Filtering is
         permitted on the 'name' property only and with limited number of OData operations. These
         operations are: the 'contains' function as well as the following logical operations: not, and,
         or, eq (for equal), and ne (for not equal). No arithmetic operations are supported. The
         following is a valid filter example: $filter=contains(namE, 'PATTERN') and name ne 'PATTERN-1'.
         The following is not a valid filter example: $filter=location eq 'westus'. Default value is
         None.
        :type filter: str
        :param top: The number of results to return per page for the list operation. Valid range for
         top parameter is 1 to 100. If not specified, the default number of results to be returned is 20
         items per page. Default value is None.
        :type top: int
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either PartnerTopicsListResult or the result of
         cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.eventgrid.models.PartnerTopicsListResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str

        cls = kwargs.pop('cls', None)  # type: ClsType["_models.PartnerTopicsListResult"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_by_resource_group_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    api_version=api_version,
                    filter=filter,
                    top=top,
                    template_url=self.list_by_resource_group.metadata['url'],
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)

            else:
                
                request = build_list_by_resource_group_request(
                    subscription_id=self._config.subscription_id,
                    resource_group_name=resource_group_name,
                    api_version=api_version,
                    filter=filter,
                    top=top,
                    template_url=next_link,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("PartnerTopicsListResult", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list_by_resource_group.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics"}  # type: ignore

    @distributed_trace_async
    async def activate(
        self,
        resource_group_name: str,
        partner_topic_name: str,
        **kwargs: Any
    ) -> "_models.PartnerTopic":
        """Activate a partner topic.

        Activate a newly created partner topic.

        :param resource_group_name: The name of the resource group within the user's subscription.
        :type resource_group_name: str
        :param partner_topic_name: Name of the partner topic.
        :type partner_topic_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PartnerTopic, or the result of cls(response)
        :rtype: ~azure.mgmt.eventgrid.models.PartnerTopic
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.PartnerTopic"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str

        
        request = build_activate_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            partner_topic_name=partner_topic_name,
            api_version=api_version,
            template_url=self.activate.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('PartnerTopic', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    activate.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics/{partnerTopicName}/activate"}  # type: ignore


    @distributed_trace_async
    async def deactivate(
        self,
        resource_group_name: str,
        partner_topic_name: str,
        **kwargs: Any
    ) -> "_models.PartnerTopic":
        """Deactivate a partner topic.

        Deactivate specific partner topic.

        :param resource_group_name: The name of the resource group within the user's subscription.
        :type resource_group_name: str
        :param partner_topic_name: Name of the partner topic.
        :type partner_topic_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: PartnerTopic, or the result of cls(response)
        :rtype: ~azure.mgmt.eventgrid.models.PartnerTopic
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["_models.PartnerTopic"]
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError
        }
        error_map.update(kwargs.pop('error_map', {}))

        api_version = kwargs.pop('api_version', "2021-10-15-preview")  # type: str

        
        request = build_deactivate_request(
            subscription_id=self._config.subscription_id,
            resource_group_name=resource_group_name,
            partner_topic_name=partner_topic_name,
            api_version=api_version,
            template_url=self.deactivate.metadata['url'],
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)

        pipeline_response = await self._client._pipeline.run(  # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('PartnerTopic', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    deactivate.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/partnerTopics/{partnerTopicName}/deactivate"}  # type: ignore

