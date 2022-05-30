# coding: utf-8

"""
    validateapi

    The validation APIs help you validate data. Check if an E-mail address is real. Check if a domain is real. Check up on an IP address, and even where it is located. All this and much more is available in the validation API.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from cloudmersive_validate_api_client.api_client import ApiClient


class IPAddressApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def i_p_address_geolocate_street_address(self, value, **kwargs):  # noqa: E501
        """Geolocate an IP address to a street address  # noqa: E501

        Identify an IP address's street address.  Useful for security and UX applications.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_geolocate_street_address(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to geolocate, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: GeolocateStreetAddressResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.i_p_address_geolocate_street_address_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.i_p_address_geolocate_street_address_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def i_p_address_geolocate_street_address_with_http_info(self, value, **kwargs):  # noqa: E501
        """Geolocate an IP address to a street address  # noqa: E501

        Identify an IP address's street address.  Useful for security and UX applications.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_geolocate_street_address_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to geolocate, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: GeolocateStreetAddressResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method i_p_address_geolocate_street_address" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `i_p_address_geolocate_street_address`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/validate/ip/geolocate/street-address', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GeolocateStreetAddressResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def i_p_address_ip_intelligence(self, value, **kwargs):  # noqa: E501
        """Get intelligence on an IP address  # noqa: E501

        Identify key intelligence about an IP address, including if it is a known threat IP, known bot, Tor exit node, as well as the location of the IP address.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_ip_intelligence(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to process, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: IPIntelligenceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.i_p_address_ip_intelligence_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.i_p_address_ip_intelligence_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def i_p_address_ip_intelligence_with_http_info(self, value, **kwargs):  # noqa: E501
        """Get intelligence on an IP address  # noqa: E501

        Identify key intelligence about an IP address, including if it is a known threat IP, known bot, Tor exit node, as well as the location of the IP address.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_ip_intelligence_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to process, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: IPIntelligenceResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method i_p_address_ip_intelligence" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `i_p_address_ip_intelligence`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/validate/ip/intelligence', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='IPIntelligenceResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def i_p_address_is_bot(self, value, **kwargs):  # noqa: E501
        """Check if IP address is a Bot client  # noqa: E501

        Check if the input IP address is a Bot, robot, or otherwise a non-user entity.  Leverages real-time signals to check against known high-probability bots..  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_is_bot(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: BotCheckResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.i_p_address_is_bot_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.i_p_address_is_bot_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def i_p_address_is_bot_with_http_info(self, value, **kwargs):  # noqa: E501
        """Check if IP address is a Bot client  # noqa: E501

        Check if the input IP address is a Bot, robot, or otherwise a non-user entity.  Leverages real-time signals to check against known high-probability bots..  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_is_bot_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: BotCheckResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method i_p_address_is_bot" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `i_p_address_is_bot`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/validate/ip/is-bot', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BotCheckResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def i_p_address_is_threat(self, value, **kwargs):  # noqa: E501
        """Check if IP address is a known threat  # noqa: E501

        Check if the input IP address is a known threat IP address.  Checks against known bad IPs, botnets, compromised servers, and other lists of threats.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_is_threat(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: IPThreatResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.i_p_address_is_threat_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.i_p_address_is_threat_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def i_p_address_is_threat_with_http_info(self, value, **kwargs):  # noqa: E501
        """Check if IP address is a known threat  # noqa: E501

        Check if the input IP address is a known threat IP address.  Checks against known bad IPs, botnets, compromised servers, and other lists of threats.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_is_threat_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: IPThreatResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method i_p_address_is_threat" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `i_p_address_is_threat`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/validate/ip/is-threat', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='IPThreatResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def i_p_address_is_tor_node(self, value, **kwargs):  # noqa: E501
        """Check if IP address is a Tor node server  # noqa: E501

        Check if the input IP address is a Tor exit node server.  Tor servers are a type of privacy-preserving technology that can hide the original IP address who makes a request.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_is_tor_node(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: TorNodeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.i_p_address_is_tor_node_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.i_p_address_is_tor_node_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def i_p_address_is_tor_node_with_http_info(self, value, **kwargs):  # noqa: E501
        """Check if IP address is a Tor node server  # noqa: E501

        Check if the input IP address is a Tor exit node server.  Tor servers are a type of privacy-preserving technology that can hide the original IP address who makes a request.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_is_tor_node_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: TorNodeResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method i_p_address_is_tor_node" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `i_p_address_is_tor_node`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/validate/ip/is-tor-node', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TorNodeResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def i_p_address_post(self, value, **kwargs):  # noqa: E501
        """Geolocate an IP address  # noqa: E501

        Identify an IP address Country, State/Provence, City, Zip/Postal Code, etc.  Useful for security and UX applications.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_post(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to geolocate, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: GeolocateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.i_p_address_post_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.i_p_address_post_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def i_p_address_post_with_http_info(self, value, **kwargs):  # noqa: E501
        """Geolocate an IP address  # noqa: E501

        Identify an IP address Country, State/Provence, City, Zip/Postal Code, etc.  Useful for security and UX applications.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_post_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to geolocate, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: GeolocateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method i_p_address_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `i_p_address_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/validate/ip/geolocate', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GeolocateResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def i_p_address_reverse_domain_lookup(self, value, **kwargs):  # noqa: E501
        """Perform a reverse domain name (DNS) lookup on an IP address  # noqa: E501

        Gets the domain name, if any, associated with the IP address.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_reverse_domain_lookup(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: IPReverseDNSLookupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.i_p_address_reverse_domain_lookup_with_http_info(value, **kwargs)  # noqa: E501
        else:
            (data) = self.i_p_address_reverse_domain_lookup_with_http_info(value, **kwargs)  # noqa: E501
            return data

    def i_p_address_reverse_domain_lookup_with_http_info(self, value, **kwargs):  # noqa: E501
        """Perform a reverse domain name (DNS) lookup on an IP address  # noqa: E501

        Gets the domain name, if any, associated with the IP address.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.i_p_address_reverse_domain_lookup_with_http_info(value, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str value: IP address to check, e.g. \"55.55.55.55\".  The input is a string so be sure to enclose it in double-quotes. (required)
        :return: IPReverseDNSLookupResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['value']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method i_p_address_reverse_domain_lookup" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'value' is set
        if ('value' not in params or
                params['value'] is None):
            raise ValueError("Missing the required parameter `value` when calling `i_p_address_reverse_domain_lookup`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'value' in params:
            body_params = params['value']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/json', 'application/xml', 'text/xml'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Apikey']  # noqa: E501

        return self.api_client.call_api(
            '/validate/ip/reverse-domain-lookup', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='IPReverseDNSLookupResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
