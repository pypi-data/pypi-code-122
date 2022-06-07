# coding: utf-8

"""
    API Reference: Billing

      # Introduction  Welcome to the reference for the Zuora Billing REST API!  To learn about the common use cases of Zuora Billing REST APIs, check out the [API Guides](https://www.zuora.com/developer/api-guides/).  In addition to Zuora API Reference; Billing, we also provide API references for other Zuora products:    * [API Reference: Collections](https://www.zuora.com/developer/collect-api/)   * [API Reference: Revenue](https://www.zuora.com/developer/revpro-api/)      The Zuora REST API provides a broad set of operations and resources that:    * Enable Web Storefront integration from your website.   * Support self-service subscriber sign-ups and account management.   * Process revenue schedules through custom revenue rule models.   * Enable manipulation of most objects in the Zuora Billing Object Model.  Want to share your opinion on how our API works for you? <a href=\"https://community.zuora.com/t5/Developers/API-Feedback-Form/gpm-p/21399\" target=\"_blank\">Tell us how you feel </a>about using our API and what we can do to make it better.  ## Access to the API  If you have a Zuora tenant, you can access the Zuora REST API via one of the following endpoints:  | Tenant              | Base URL for REST Endpoints | |-------------------------|-------------------------| |US Cloud 1 Production | https://rest.na.zuora.com  | |US Cloud 1 API Sandbox |  https://rest.sandbox.na.zuora.com | |US Cloud 2 Production | https://rest.zuora.com | |US Cloud 2 API Sandbox | https://rest.apisandbox.zuora.com| |US Central Sandbox | https://rest.test.zuora.com |   |US Performance Test | https://rest.pt1.zuora.com | |US Production Copy | Submit a request at <a href=\"http://support.zuora.com/\" target=\"_blank\">Zuora Global Support</a> to enable the Zuora REST API in your tenant and obtain the base URL for REST endpoints. See [REST endpoint base URL of Production Copy (Service) Environment for existing and new customers](https://community.zuora.com/t5/API/REST-endpoint-base-URL-of-Production-Copy-Service-Environment/td-p/29611) for more information. | |EU Production | https://rest.eu.zuora.com | |EU API Sandbox | https://rest.sandbox.eu.zuora.com | |EU Central Sandbox | https://rest.test.eu.zuora.com |  The Production endpoint provides access to your live user data. Sandbox tenants are a good place to test code without affecting real-world data. If you would like Zuora to provision a Sandbox tenant for you, contact your Zuora representative for assistance.   If you do not have a Zuora tenant, go to <a href=\"https://www.zuora.com/resource/zuora-test-drive\" target=\"_blank\">https://www.zuora.com/resource/zuora-test-drive</a> and sign up for a Production Test Drive tenant. The tenant comes with seed data, including a sample product catalog.  # API Changelog You can find the <a href=\"https://bit.ly/3JGqyR3\" target=\"_blank\">Changelog</a> of the API Reference: Billing in the Zuora Community.  # Authentication  ## OAuth v2.0  Zuora recommends that you use OAuth v2.0 to authenticate to the Zuora REST API. Currently, OAuth is not available in every environment. See [Zuora Testing Environments](https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/D_Zuora_Environments) for more information.  Zuora recommends you to create a dedicated API user with API write access on a tenant when authenticating via OAuth, and then create an OAuth client for this user. See <a href=\"https://knowledgecenter.zuora.com/CF_Users_and_Administrators/A_Administrator_Settings/Manage_Users/Create_an_API_User\" target=\"_blank\">Create an API User</a> for how to do this. By creating a dedicated API user, you can control permissions of the API user without affecting other non-API users.  If a user is deactivated, all of the user's OAuth clients will be automatically deactivated.  Authenticating via OAuth requires the following steps: 1. Create a Client 2. Generate a Token 3. Make Authenticated Requests  ### Create a Client  You must first [create an OAuth client](https://knowledgecenter.zuora.com/CF_Users_and_Administrators/A_Administrator_Settings/Manage_Users#Create_an_OAuth_Client_for_a_User) in the Zuora UI. To do this, you must be an administrator of your Zuora tenant. This is a one-time operation. You will be provided with a Client ID and a Client Secret. Please note this information down, as it will be required for the next step.  **Note:** The OAuth client will be owned by a Zuora user account. If you want to perform PUT, POST, or DELETE operations using the OAuth client, the owner of the OAuth client must have a Platform role that includes the \"API Write Access\" permission.  ### Generate a Token  After creating a client, you must make a call to obtain a bearer token using the [Generate an OAuth token](https://www.zuora.com/developer/api-reference/#operation/createToken) operation. This operation requires the following parameters: - `client_id` - the Client ID displayed when you created the OAuth client in the previous step - `client_secret` - the Client Secret displayed when you created the OAuth client in the previous step - `grant_type` - must be set to `client_credentials`  **Note**: The Client ID and Client Secret mentioned above were displayed when you created the OAuth Client in the prior step. The [Generate an OAuth token](https://www.zuora.com/developer/api-reference/#operation/createToken) response specifies how long the bearer token is valid for. You should reuse the bearer token until it is expired. When the token is expired, call [Generate an OAuth token](https://www.zuora.com/developer/api-reference/#operation/createToken) again to generate a new one.  ### Make Authenticated Requests  To authenticate subsequent API requests, you must provide a valid bearer token in an HTTP header:  `Authorization: Bearer {bearer_token}`  If you have [Zuora Multi-entity](https://www.zuora.com/developer/api-reference/#tag/Entities) enabled, you need to set an additional header to specify the ID of the entity that you want to access. You can use the `scope` field in the [Generate an OAuth token](https://www.zuora.com/developer/api-reference/#operation/createToken) response to determine whether you need to specify an entity ID.  If the `scope` field contains more than one entity ID, you must specify the ID of the entity that you want to access. For example, if the `scope` field contains `entity.1a2b7a37-3e7d-4cb3-b0e2-883de9e766cc` and `entity.c92ed977-510c-4c48-9b51-8d5e848671e9`, specify one of the following headers: - `Zuora-Entity-Ids: 1a2b7a37-3e7d-4cb3-b0e2-883de9e766cc` - `Zuora-Entity-Ids: c92ed977-510c-4c48-9b51-8d5e848671e9`  **Note**: For a limited period of time, Zuora will accept the `entityId` header as an alternative to the `Zuora-Entity-Ids` header. If you choose to set the `entityId` header, you must remove all \"-\" characters from the entity ID in the `scope` field.  If the `scope` field contains a single entity ID, you do not need to specify an entity ID.  ## Other Supported Authentication Schemes  Zuora continues to support the following additional legacy means of authentication:    * Use username and password. Include authentication with each request in the header:         * `apiAccessKeyId`      * `apiSecretAccessKey`          Zuora recommends that you create an API user specifically for making API calls. See <a href=\"https://knowledgecenter.zuora.com/CF_Users_and_Administrators/A_Administrator_Settings/Manage_Users/Create_an_API_User\" target=\"_blank\">Create an API User</a> for more information.      * Use an authorization cookie. The cookie authorizes the user to make calls to the REST API for the duration specified in  **Administration > Security Policies > Session timeout**. The cookie expiration time is reset with this duration after every call to the REST API. To obtain a cookie, call the [Connections](https://www.zuora.com/developer/api-reference/#tag/Connections) resource with the following API user information:         *   ID         *   Password        * For CORS-enabled APIs only: Include a 'single-use' token in the request header, which re-authenticates the user with each request. See below for more details.  ### Entity Id and Entity Name  The `entityId` and `entityName` parameters are only used for [Zuora Multi-entity](https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/Multi-entity \"Zuora Multi-entity\"). These are the legacy parameters that Zuora will only continue to support for a period of time. Zuora recommends you to use the `Zuora-Entity-Ids` parameter instead.   The  `entityId` and `entityName` parameters specify the Id and the [name of the entity](https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/Multi-entity/B_Introduction_to_Entity_and_Entity_Hierarchy#Name_and_Display_Name \"Introduction to Entity and Entity Hierarchy\") that you want to access, respectively. Note that you must have permission to access the entity.   You can specify either the `entityId` or `entityName` parameter in the authentication to access and view an entity.    * If both `entityId` and `entityName` are specified in the authentication, an error occurs.    * If neither `entityId` nor `entityName` is specified in the authentication, you will log in to the entity in which your user account is created.      To get the entity Id and entity name, you can use the GET Entities REST call. For more information, see [API User Authentication](https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/Multi-entity/A_Overview_of_Multi-entity#API_User_Authentication \"API User Authentication\").      ### Token Authentication for CORS-Enabled APIs      The CORS mechanism enables REST API calls to Zuora to be made directly from your customer's browser, with all credit card and security information transmitted directly to Zuora. This minimizes your PCI compliance burden, allows you to implement advanced validation on your payment forms, and  makes your payment forms look just like any other part of your website.    For security reasons, instead of using cookies, an API request via CORS uses **tokens** for authentication.  The token method of authentication is only designed for use with requests that must originate from your customer's browser; **it should  not be considered a replacement to the existing cookie authentication** mechanism.  See [Zuora CORS REST](https://knowledgecenter.zuora.com/DC_Developers/C_REST_API/Zuora_CORS_REST \"Zuora CORS REST\") for details on how CORS works and how you can begin to implement customer calls to the Zuora REST APIs. See  [HMAC Signatures](https://www.zuora.com/developer/api-reference/#operation/POSTHMACSignature \"HMAC Signatures\") for details on the HMAC method that returns the authentication token.  # Requests and Responses  ## Request IDs  As a general rule, when asked to supply a \"key\" for an account or subscription (accountKey, account-key, subscriptionKey, subscription-key), you can provide either the actual ID or  the number of the entity.  ## HTTP Request Body  Most of the parameters and data accompanying your requests will be contained in the body of the HTTP request.   The Zuora REST API accepts JSON in the HTTP request body. No other data format (e.g., XML) is supported.  ### Data Type  ([Actions](https://www.zuora.com/developer/api-reference/#tag/Actions) and CRUD operations only) We recommend that you do not specify the decimal values with quotation marks, commas, and spaces. Use characters of `+-0-9.eE`, for example, `5`, `1.9`, `-8.469`, and `7.7e2`. Also, Zuora does not convert currencies for decimal values.   ## Making asynchronous requests  Most Zuora REST API endpoints documented in this API Reference process requests synchronously. In high-throughput scenarios, your requests to these endpoints are usually rate limited.   One strategy for avoiding rate limits is to make asynchronous requests, and Zuora provides this option to you.  Making asynchronous requests allows you to scale your applications more efficiently by leveraging Zuora's infrastructure to enqueue and execute requests for you without blocking. These requests also use built-in retry semantics, which makes them much less likely to fail for non-deterministic reasons, even in extreme high-throughput scenarios.  Meanwhile, when you send a request to one of these endpoints, you can receive a response in less than 150 milliseconds and these calls are unlikely to trigger rate limit errors.   You can make asynchronous requests to the POST, PUT, or DELETE operations, except [Actions](https://www.zuora.com/developer/api-reference/#tag/Actions), for all resources documented in this API Reference.  Take the following steps to take advantage of the asynchronous API:    1. Set up callout notification   2. Make asynchronous requests  The following sections describes the high-level steps for you to get the most of the asynchronous API. For detailed instructions, see [Make asynchronous requests](https://knowledgecenter.zuora.com/Central_Platform/API/AA_REST_API/Make_asynchronous_requests) in the Knowledge Center.   ### Set up notifications  You can create callout notification definitions based on the following custom events through the Zuora UI or the [Create a notification definition](https://www.zuora.com/developer/api-reference/#operation/POST_Create_Notification_Definition) API operation:   * Async Request Succeeded   * Async Request Failed  This step ensures that your system receives a callout when an asynchronous request succeeds or fails.   ### Make asynchronous requests  By design, asynchronous requests differ from their synchronous counterparts in endpoints, and the HTTP status response code and response body they return. ​​The header parameters and request body schema for asynchronous operations are the same as their synchronous counterparts.   * The endpoints for asynchronous API operations contain `/async` in the path after `/v1`. See the following table for examples:  | Operation               | Synchronous endpoint  | Asynchronous endpoint      | |:-------- |:-------- |:-------- | | Create an account       | `/v1/accounts`        | `/v1/async/accounts`       | | CRUD: Create an account | `/v1/object/account`  | `/v1/async/object/account` |  * Unlike the 200 OK response for synchronous requests, Zuora returns a 202 Accepted response for all asynchronous requests, and the response body contains only a request ID.   **Note**: These asynchronous API endpoints are in addition to the previously introduced endpoints that support asynchronous processing. You should continue to use them:   * [Perform a mass action](https://www.zuora.com/developer/api-reference/#operation/POST_MassUpdater)   * [Create an order asynchronously](https://www.zuora.com/developer/api-reference/#operation/POST_CreateOrderAsynchronously)   * [Preview an order asynchronously](https://www.zuora.com/developer/api-reference/#operation/POST_PreviewOrderAsynchronously)   * [Create a job to hard delete billing document files](https://www.zuora.com/developer/api-reference/#operation/POST_BillingDocumentFilesDeletionJob)   * [CRUD: Post or cancel a bill run](https://www.zuora.com/developer/api-reference/#operation/Object_PUTBillRun)   * [Cancel a journal run](https://www.zuora.com/developer/api-reference/#operation/PUT_JournalRun)   * [Run trial balance](https://www.zuora.com/developer/api-reference/#operation/PUT_RunTrialBalance)  For more information, see [Make asynchronous requests](https://knowledgecenter.zuora.com/Central_Platform/API/AA_REST_API/Make_asynchronous_requests).  ## Testing a Request  Use a third party client, such as [curl](https://curl.haxx.se \"curl\"), [Postman](https://www.getpostman.com \"Postman\"), or [Advanced REST Client](https://advancedrestclient.com \"Advanced REST Client\"), to test the Zuora REST API.  You can test the Zuora REST API from the Zuora API Sandbox or Production tenants. If connecting to Production, bear in mind that you are working with your live production data, not sample data or test data.  ## Testing with Credit Cards  Sooner or later it will probably be necessary to test some transactions that involve credit cards. For suggestions on how to handle this, see [Going Live With Your Payment Gateway](https://knowledgecenter.zuora.com/CB_Billing/M_Payment_Gateways/C_Managing_Payment_Gateways/B_Going_Live_Payment_Gateways#Testing_with_Credit_Cards \"C_Zuora_User_Guides/A_Billing_and_Payments/M_Payment_Gateways/C_Managing_Payment_Gateways/B_Going_Live_Payment_Gateways#Testing_with_Credit_Cards\" ).  ## Concurrent Request Limits  Zuora enforces tenant-level concurrent request limits. See <a href=\"https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/Policies/Concurrent_Request_Limits\" target=\"_blank\">Concurrent Request Limits</a> for more information.  ## Timeout Limit  If a request does not complete within 120 seconds, the request times out and Zuora returns a Gateway Timeout error.   # Error Handling  If a request to Zuora Billing REST API with an endpoint starting with `/v1` (except [Actions](https://www.zuora.com/developer/api-reference/#tag/Actions) and CRUD operations) fails, the response will contain an eight-digit error code with a corresponding error message to indicate the details of the error.  The following code snippet is a sample error response that contains an error code and message pair:  ```  {    \"success\": false,    \"processId\": \"CBCFED6580B4E076\",    \"reasons\":  [      {       \"code\": 53100320,       \"message\": \"'termType' value should be one of: TERMED, EVERGREEN\"      }     ]  } ``` The `success` field indicates whether the API request has succeeded. The `processId` field is a Zuora internal ID that you can provide to Zuora Global Support for troubleshooting purposes.  The `reasons` field contains the actual error code and message pair. The error code begins with `5` or `6` means that you encountered a certain issue that is specific to a REST API resource in Zuora Billing. For example, `53100320` indicates that an invalid value is specified for the `termType` field of the `subscription` object.  The error code beginning with `9` usually indicates that an authentication-related issue occurred, and it can also indicate other unexpected errors depending on different cases. For example, `90000011` indicates that an invalid credential is provided in the request header.   When troubleshooting the error, you can divide the error code into two components: REST API resource code and error category code. See the following Zuora error code sample:  <a href=\"https://assets.zuora.com/zuora-documentation/ZuoraErrorCode.jpeg\" target=\"_blank\"><img src=\"https://assets.zuora.com/zuora-documentation/ZuoraErrorCode.jpeg\" alt=\"Zuora Error Code Sample\"></a>   **Note:** Zuora determines resource codes based on the request payload. Therefore, if GET and DELETE requests that do not contain payloads fail, you will get `500000` as the resource code, which indicates an unknown object and an unknown field.  The error category code of these requests is valid and follows the rules described in the [Error Category Code](https://www.zuora.com/developer/api-reference/#section/Error-Handling/Error-Category-Code) section.  In such case, you can refer to the returned error message to troubleshoot.   ## REST API Resource Code  The 6-digit resource code indicates the REST API resource, typically a field of a Zuora object, on which the issue occurs. In the preceding example, `531003` refers to the `termType` field of the `subscription` object.   The value range for all REST API resource codes is from `500000` to `679999`. See [Resource Codes](https://knowledgecenter.zuora.com/Central_Platform/API/AA_REST_API/Resource_Codes) in the Knowledge Center for a full list of resource codes.  ## Error Category Code  The 2-digit error category code identifies the type of error, for example, resource not found or missing required field.   The following table describes all error categories and the corresponding resolution:  | Code    | Error category              | Description    | Resolution    | |:--------|:--------|:--------|:--------| | 10      | Permission or access denied | The request cannot be processed because a certain tenant or user permission is missing. | Check the missing tenant or user permission in the response message and contact [Zuora Global Support](https://support.zuora.com) for enablement. | | 11      | Authentication failed       | Authentication fails due to invalid API authentication credentials. | Ensure that a valid API credential is specified. | | 20      | Invalid format or value     | The request cannot be processed due to an invalid field format or value. | Check the invalid field in the error message, and ensure that the format and value of all fields you passed in are valid. | | 21      | Unknown field in request    | The request cannot be processed because an unknown field exists in the request body. | Check the unknown field name in the response message, and ensure that you do not include any unknown field in the request body. | | 22      | Missing required field      | The request cannot be processed because a required field in the request body is missing. | Check the missing field name in the response message, and ensure that you include all required fields in the request body. | | 23      | Missing required parameter  | The request cannot be processed because a required query parameter is missing. | Check the missing parameter name in the response message, and ensure that you include the parameter in the query. | | 30      | Rule restriction            | The request cannot be processed due to the violation of a Zuora business rule. | Check the response message and ensure that the API request meets the specified business rules. | | 40      | Not found                   | The specified resource cannot be found. | Check the response message and ensure that the specified resource exists in your Zuora tenant. | | 45      | Unsupported request         | The requested endpoint does not support the specified HTTP method. | Check your request and ensure that the endpoint and method matches. | | 50      | Locking contention          | This request cannot be processed because the objects this request is trying to modify are being modified by another API request, UI operation, or batch job process. | <p>Resubmit the request first to have another try.</p> <p>If this error still occurs, contact [Zuora Global Support](https://support.zuora.com) with the returned `Zuora-Request-Id` value in the response header for assistance.</p> | | 60      | Internal error              | The server encounters an internal error. | Contact [Zuora Global Support](https://support.zuora.com) with the returned `Zuora-Request-Id` value in the response header for assistance. | | 70      | Request exceeded limit      | The total number of concurrent requests exceeds the limit allowed by the system. | <p>Resubmit the request after the number of seconds specified by the `Retry-After` value in the response header.</p> <p>Check [Concurrent request limits](https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/Policies/Concurrent_Request_Limits) for details about Zuora’s concurrent request limit policy.</p> | | 90      | Malformed request           | The request cannot be processed due to JSON syntax errors. | Check the syntax error in the JSON request body and ensure that the request is in the correct JSON format. | | 99      | Integration error           | The server encounters an error when communicating with an external system, for example, payment gateway, tax engine provider. | Check the response message and take action accordingly. |   # Pagination  When retrieving information (using GET methods), the optional `pageSize` query parameter sets the maximum number of rows to return in a response. The maximum is `40`; larger values are treated as `40`. If this value is empty or invalid, `pageSize` typically defaults to `10`.  The default value for the maximum number of rows retrieved can be overridden at the method level.  If more rows are available, the response will include a `nextPage` element, which contains a URL for requesting the next page.  If this value is not provided, no more rows are available. No \"previous page\" element is explicitly provided; to support backward paging, use the previous call.  ## Array Size  For data items that are not paginated, the REST API supports arrays of up to 300 rows.  Thus, for instance, repeated pagination can retrieve thousands of customer accounts, but within any account an array of no more than 300 rate plans is returned.  # API Versions  The Zuora REST API are version controlled. Versioning ensures that Zuora REST API changes are backward compatible. Zuora uses a major and minor version nomenclature to manage changes. By specifying a version in a REST request, you can get expected responses regardless of future changes to the API.  ## Major Version  The major version number of the REST API appears in the REST URL. Currently, Zuora only supports the **v1** major version. For example, `POST https://rest.zuora.com/v1/subscriptions`.  ## Minor Version  Zuora uses minor versions for the REST API to control small changes. For example, a field in a REST method is deprecated and a new field is used to replace it.   Some fields in the REST methods are supported as of minor versions. If a field is not noted with a minor version, this field is available for all minor versions. If a field is noted with a minor version, this field is in version control. You must specify the supported minor version in the request header to process without an error.   If a field is in version control, it is either with a minimum minor version or a maximum minor version, or both of them. You can only use this field with the minor version between the minimum and the maximum minor versions. For example, the `invoiceCollect` field in the POST Subscription method is in version control and its maximum minor version is 189.0. You can only use this field with the minor version 189.0 or earlier.  If you specify a version number in the request header that is not supported, Zuora will use the minimum minor version of the REST API. In our REST API documentation, if a field or feature requires a minor version number, we note that in the field description.  You only need to specify the version number when you use the fields require a minor version. To specify the minor version, set the `zuora-version` parameter to the minor version number in the request header for the request call. For example, the `collect` field is in 196.0 minor version. If you want to use this field for the POST Subscription method, set the  `zuora-version` parameter to `196.0` in the request header. The `zuora-version` parameter is case sensitive.  For all the REST API fields, by default, if the minor version is not specified in the request header, Zuora will use the minimum minor version of the REST API to avoid breaking your integration.   ### Minor Version History  The supported minor versions are not serial. This section documents the changes made to each Zuora REST API minor version.  The following table lists the supported versions and the fields that have a Zuora REST API minor version.  | Fields         | Minor Version      | REST Methods    | Description | |:--------|:--------|:--------|:--------| | invoiceCollect | 189.0 and earlier  | [Create Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_Subscription \"Create Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\"); [Renew Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_RenewSubscription \"Renew Subscription\"); [Cancel Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_CancelSubscription \"Cancel Subscription\"); [Suspend Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_SuspendSubscription \"Suspend Subscription\"); [Resume Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_ResumeSubscription \"Resume Subscription\"); [Create Account](https://www.zuora.com/developer/api-reference/#operation/POST_Account \"Create Account\")|Generates an invoice and collects a payment for a subscription. | | collect        | 196.0 and later    | [Create Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_Subscription \"Create Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\"); [Renew Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_RenewSubscription \"Renew Subscription\"); [Cancel Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_CancelSubscription \"Cancel Subscription\"); [Suspend Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_SuspendSubscription \"Suspend Subscription\"); [Resume Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_ResumeSubscription \"Resume Subscription\"); [Create Account](https://www.zuora.com/developer/api-reference/#operation/POST_Account \"Create Account\")|Collects an automatic payment for a subscription. | | invoice | 196.0 and 207.0| [Create Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_Subscription \"Create Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\"); [Renew Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_RenewSubscription \"Renew Subscription\"); [Cancel Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_CancelSubscription \"Cancel Subscription\"); [Suspend Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_SuspendSubscription \"Suspend Subscription\"); [Resume Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_ResumeSubscription \"Resume Subscription\"); [Create Account](https://www.zuora.com/developer/api-reference/#operation/POST_Account \"Create Account\")|Generates an invoice for a subscription. | | invoiceTargetDate | 196.0 and earlier  | [Preview Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_SubscriptionPreview \"Preview Subscription\") |Date through which charges are calculated on the invoice, as `yyyy-mm-dd`. | | invoiceTargetDate | 207.0 and earlier  | [Create Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_Subscription \"Create Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\"); [Renew Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_RenewSubscription \"Renew Subscription\"); [Cancel Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_CancelSubscription \"Cancel Subscription\"); [Suspend Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_SuspendSubscription \"Suspend Subscription\"); [Resume Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_ResumeSubscription \"Resume Subscription\"); [Create Account](https://www.zuora.com/developer/api-reference/#operation/POST_Account \"Create Account\")|Date through which charges are calculated on the invoice, as `yyyy-mm-dd`. | | targetDate | 207.0 and later | [Preview Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_SubscriptionPreview \"Preview Subscription\") |Date through which charges are calculated on the invoice, as `yyyy-mm-dd`. | | targetDate | 211.0 and later | [Create Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_Subscription \"Create Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\"); [Renew Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_RenewSubscription \"Renew Subscription\"); [Cancel Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_CancelSubscription \"Cancel Subscription\"); [Suspend Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_SuspendSubscription \"Suspend Subscription\"); [Resume Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_ResumeSubscription \"Resume Subscription\"); [Create Account](https://www.zuora.com/developer/api-reference/#operation/POST_Account \"Create Account\")|Date through which charges are calculated on the invoice, as `yyyy-mm-dd`. | | includeExisting DraftInvoiceItems | 196.0 and earlier| [Preview Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_SubscriptionPreview \"Preview Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\") | Specifies whether to include draft invoice items in subscription previews. Specify it to be `true` (default) to include draft invoice items in the preview result. Specify it to be `false` to excludes draft invoice items in the preview result. | | includeExisting DraftDocItems | 207.0 and later  | [Preview Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_SubscriptionPreview \"Preview Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\") | Specifies whether to include draft invoice items in subscription previews. Specify it to be `true` (default) to include draft invoice items in the preview result. Specify it to be `false` to excludes draft invoice items in the preview result. | | previewType | 196.0 and earlier| [Preview Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_SubscriptionPreview \"Preview Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\") | The type of preview you will receive. The possible values are `InvoiceItem`(default), `ChargeMetrics`, and `InvoiceItemChargeMetrics`. | | previewType | 207.0 and later  | [Preview Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_SubscriptionPreview \"Preview Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\") | The type of preview you will receive. The possible values are `LegalDoc`(default), `ChargeMetrics`, and `LegalDocChargeMetrics`. | | runBilling  | 211.0 and later  | [Create Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_Subscription \"Create Subscription\"); [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\"); [Renew Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_RenewSubscription \"Renew Subscription\"); [Cancel Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_CancelSubscription \"Cancel Subscription\"); [Suspend Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_SuspendSubscription \"Suspend Subscription\"); [Resume Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_ResumeSubscription \"Resume Subscription\"); [Create Account](https://www.zuora.com/developer/api-reference/#operation/POST_Account \"Create Account\")|Generates an invoice or credit memo for a subscription. **Note:** Credit memos are only available if you have the Invoice Settlement feature enabled. | | invoiceDate | 214.0 and earlier  | [Invoice and Collect](https://www.zuora.com/developer/api-reference/#operation/POST_TransactionInvoicePayment \"Invoice and Collect\") |Date that should appear on the invoice being generated, as `yyyy-mm-dd`. | | invoiceTargetDate | 214.0 and earlier  | [Invoice and Collect](https://www.zuora.com/developer/api-reference/#operation/POST_TransactionInvoicePayment \"Invoice and Collect\") |Date through which to calculate charges on this account if an invoice is generated, as `yyyy-mm-dd`. | | documentDate | 215.0 and later | [Invoice and Collect](https://www.zuora.com/developer/api-reference/#operation/POST_TransactionInvoicePayment \"Invoice and Collect\") |Date that should appear on the invoice and credit memo being generated, as `yyyy-mm-dd`. | | targetDate | 215.0 and later | [Invoice and Collect](https://www.zuora.com/developer/api-reference/#operation/POST_TransactionInvoicePayment \"Invoice and Collect\") |Date through which to calculate charges on this account if an invoice or a credit memo is generated, as `yyyy-mm-dd`. | | memoItemAmount | 223.0 and earlier | [Create credit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromPrpc \"Create credit memo from charge\"); [Create debit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromPrpc \"Create debit memo from charge\") | Amount of the memo item. | | amount | 224.0 and later | [Create credit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromPrpc \"Create credit memo from charge\"); [Create debit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromPrpc \"Create debit memo from charge\") | Amount of the memo item. | | subscriptionNumbers | 222.4 and earlier | [Create order](https://www.zuora.com/developer/api-reference/#operation/POST_Order \"Create order\") | Container for the subscription numbers of the subscriptions in an order. | | subscriptions | 223.0 and later | [Create order](https://www.zuora.com/developer/api-reference/#operation/POST_Order \"Create order\") | Container for the subscription numbers and statuses in an order. | | creditTaxItems | 238.0 and earlier | [Get credit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItems \"Get credit memo items\"); [Get credit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItem \"Get credit memo item\") | Container for the taxation items of the credit memo item. | | taxItems | 238.0 and earlier | [Get debit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItems \"Get debit memo items\"); [Get debit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItem \"Get debit memo item\") | Container for the taxation items of the debit memo item. | | taxationItems | 239.0 and later | [Get credit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItems \"Get credit memo items\"); [Get credit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItem \"Get credit memo item\"); [Get debit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItems \"Get debit memo items\"); [Get debit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItem \"Get debit memo item\") | Container for the taxation items of the memo item. | | chargeId | 256.0 and earlier | [Create credit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromPrpc \"Create credit memo from charge\"); [Create debit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromPrpc \"Create debit memo from charge\") | ID of the product rate plan charge that the memo is created from. | | productRatePlanChargeId | 257.0 and later | [Create credit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromPrpc \"Create credit memo from charge\"); [Create debit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromPrpc \"Create debit memo from charge\") | ID of the product rate plan charge that the memo is created from. | | comment | 256.0 and earlier | [Create credit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromPrpc \"Create credit memo from charge\"); [Create debit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromPrpc \"Create debit memo from charge\"); [Create credit memo from invoice](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromInvoice \"Create credit memo from invoice\"); [Create debit memo from invoice](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromInvoice \"Create debit memo from invoice\"); [Get credit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItems \"Get credit memo items\"); [Get credit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItem \"Get credit memo item\"); [Get debit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItems \"Get debit memo items\"); [Get debit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItem \"Get debit memo item\") | Comments about the product rate plan charge, invoice item, or memo item. | | description | 257.0 and later | [Create credit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromPrpc \"Create credit memo from charge\"); [Create debit memo from charge](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromPrpc \"Create debit memo from charge\"); [Create credit memo from invoice](https://www.zuora.com/developer/api-reference/#operation/POST_CreditMemoFromInvoice \"Create credit memo from invoice\"); [Create debit memo from invoice](https://www.zuora.com/developer/api-reference/#operation/POST_DebitMemoFromInvoice \"Create debit memo from invoice\"); [Get credit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItems \"Get credit memo items\"); [Get credit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_CreditMemoItem \"Get credit memo item\"); [Get debit memo items](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItems \"Get debit memo items\"); [Get debit memo item](https://www.zuora.com/developer/api-reference/#operation/GET_DebitMemoItem \"Get debit memo item\") | Description of the the product rate plan charge, invoice item, or memo item. | | taxationItems | 309.0 and later | [Preview an order](https://www.zuora.com/developer/api-reference/#operation/POST_PreviewOrder \"Preview an order\") | List of taxation items for an invoice item or a credit memo item. | | batch | 309.0 and earlier | [Create a billing preview run](https://www.zuora.com/developer/api-reference/#operation/POST_BillingPreviewRun \"Create a billing preview run\") | The customer batches to include in the billing preview run. |       | batches | 314.0 and later | [Create a billing preview run](https://www.zuora.com/developer/api-reference/#operation/POST_BillingPreviewRun \"Create a billing preview run\") | The customer batches to include in the billing preview run. | | taxationItems | 315.0 and later | [Preview a subscription](https://www.zuora.com/developer/api-reference/#operation/POST_PreviewSubscription \"Preview a subscription\"); [Update a subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update a subscription\")| List of taxation items for an invoice item or a credit memo item. |    #### Version 207.0 and Later  The response structure of the [Preview Subscription](https://www.zuora.com/developer/api-reference/#operation/POST_SubscriptionPreview \"Preview Subscription\") and [Update Subscription](https://www.zuora.com/developer/api-reference/#operation/PUT_Subscription \"Update Subscription\") methods are changed. The following invoice related response fields are moved to the invoice container:    * amount   * amountWithoutTax   * taxAmount   * invoiceItems   * targetDate   * chargeMetrics  # Zuora Billing Object Model  The following diagram is a high-level view of how key business objects are related to one another within Zuora Billing.  Click the diagram to open it in a new tab and zoom in. For more information about the different sections of the diagram, see <a href=\"https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/A_Zuora_Billing_business_object_model\" target=\"_blank\">Zuora Billing business object model</a>.  <a href=\"https://assets.zuora.com/zuora-documentation/Zuora_Billing_object_model_Sep2020.png\" target=\"_blank\"><img src=\"https://assets.zuora.com/zuora-documentation/Zuora_Billing_object_model_Sep2020.png\" alt=\"Zuora Billing object model diagram\"></a>  This diagram is intended to provide a conceptual understanding; it does not illustrate a specific way to integrate with Zuora.  The diagram includes the Orders feature and the Invoice Settlement feature. If your organization does not use either of these features, see <a href=\"https://knowledgecenter.zuora.com/BB_Introducing_Z_Business/B_Zuora_Billing_business_object_model_prior_to_Orders_and_Invoice_Settlement\" target=\"_blank\">Zuora Billing business object model prior to Orders and Invoice Settlement</a> for an alternative diagram.  ## API Names  You can use the [Describe object](https://www.zuora.com/developer/api-reference/#operation/GET_Describe) operation to list the fields of each Zuora object that is available in your tenant. When you call the operation, you must specify the API name of the Zuora object.  The following table provides the API name of each Zuora object:  | Object                                        | API Name                                   | |-----------------------------------------------|--------------------------------------------| | Account                                       | `Account`                                  | | Accounting Code                               | `AccountingCode`                           | | Accounting Period                             | `AccountingPeriod`                         | | Amendment                                     | `Amendment`                                | | Application Group                             | `ApplicationGroup`                         | | Billing Run                                   | <p>`BillingRun` - API name used  in the [Describe object](https://www.zuora.com/developer/api-reference/#operation/GET_Describe) operation, Export ZOQL queries, and Data Query.</p> <p>`BillRun` - API name used in the [Actions](https://www.zuora.com/developer/api-reference/#tag/Actions). See the CRUD oprations of [Bill Run](https://www.zuora.com/developer/api-reference/#tag/Bill-Run) for more information about the `BillRun` object. `BillingRun` and `BillRun` have different fields. |                      | Contact                                       | `Contact`                                  | | Contact Snapshot                              | `ContactSnapshot`                          | | Credit Balance Adjustment                     | `CreditBalanceAdjustment`                  | | Credit Memo                                   | `CreditMemo`                               | | Credit Memo Application                       | `CreditMemoApplication`                    | | Credit Memo Application Item                  | `CreditMemoApplicationItem`                | | Credit Memo Item                              | `CreditMemoItem`                           | | Credit Memo Part                              | `CreditMemoPart`                           | | Credit Memo Part Item                         | `CreditMemoPartItem`                       | | Credit Taxation Item                          | `CreditTaxationItem`                       | | Custom Exchange Rate                          | `FXCustomRate`                             | | Debit Memo                                    | `DebitMemo`                                | | Debit Memo Item                               | `DebitMemoItem`                            | | Debit Taxation Item                           | `DebitTaxationItem`                        | | Discount Applied Metrics                      | `DiscountAppliedMetrics`                   | | Entity                                        | `Tenant`                                   | | Feature                                       | `Feature`                                  | | Gateway Reconciliation Event                  | `PaymentGatewayReconciliationEventLog`     | | Gateway Reconciliation Job                    | `PaymentReconciliationJob`                 | | Gateway Reconciliation Log                    | `PaymentReconciliationLog`                 | | Invoice                                       | `Invoice`                                  | | Invoice Adjustment                            | `InvoiceAdjustment`                        | | Invoice Item                                  | `InvoiceItem`                              | | Invoice Item Adjustment                       | `InvoiceItemAdjustment`                    | | Invoice Payment                               | `InvoicePayment`                           | | Journal Entry                                 | `JournalEntry`                             | | Journal Entry Item                            | `JournalEntryItem`                         | | Journal Run                                   | `JournalRun`                               | | Notification History - Callout                | `CalloutHistory`                           | | Notification History - Email                  | `EmailHistory`                             | | Order                                         | `Order`                                    | | Order Action                                  | `OrderAction`                              | | Order ELP                                     | `OrderElp`                                 | | Order Line Items                              | `OrderLineItems`                           |     | Order Item                                    | `OrderItem`                                | | Order MRR                                     | `OrderMrr`                                 | | Order Quantity                                | `OrderQuantity`                            | | Order TCB                                     | `OrderTcb`                                 | | Order TCV                                     | `OrderTcv`                                 | | Payment                                       | `Payment`                                  | | Payment Application                           | `PaymentApplication`                       | | Payment Application Item                      | `PaymentApplicationItem`                   | | Payment Method                                | `PaymentMethod`                            | | Payment Method Snapshot                       | `PaymentMethodSnapshot`                    | | Payment Method Transaction Log                | `PaymentMethodTransactionLog`              | | Payment Method Update                         | `UpdaterDetail`                            | | Payment Part                                  | `PaymentPart`                              | | Payment Part Item                             | `PaymentPartItem`                          | | Payment Run                                   | `PaymentRun`                               | | Payment Transaction Log                       | `PaymentTransactionLog`                    | | Processed Usage                               | `ProcessedUsage`                           | | Product                                       | `Product`                                  | | Product Feature                               | `ProductFeature`                           | | Product Rate Plan                             | `ProductRatePlan`                          | | Product Rate Plan Charge                      | `ProductRatePlanCharge`                    | | Product Rate Plan Charge Tier                 | `ProductRatePlanChargeTier`                | | Rate Plan                                     | `RatePlan`                                 | | Rate Plan Charge                              | `RatePlanCharge`                           | | Rate Plan Charge Tier                         | `RatePlanChargeTier`                       | | Refund                                        | `Refund`                                   | | Refund Application                            | `RefundApplication`                        | | Refund Application Item                       | `RefundApplicationItem`                    | | Refund Invoice Payment                        | `RefundInvoicePayment`                     | | Refund Part                                   | `RefundPart`                               | | Refund Part Item                              | `RefundPartItem`                           | | Refund Transaction Log                        | `RefundTransactionLog`                     | | Revenue Charge Summary                        | `RevenueChargeSummary`                     | | Revenue Charge Summary Item                   | `RevenueChargeSummaryItem`                 | | Revenue Event                                 | `RevenueEvent`                             | | Revenue Event Credit Memo Item                | `RevenueEventCreditMemoItem`               | | Revenue Event Debit Memo Item                 | `RevenueEventDebitMemoItem`                | | Revenue Event Invoice Item                    | `RevenueEventInvoiceItem`                  | | Revenue Event Invoice Item Adjustment         | `RevenueEventInvoiceItemAdjustment`        | | Revenue Event Item                            | `RevenueEventItem`                         | | Revenue Event Item Credit Memo Item           | `RevenueEventItemCreditMemoItem`           | | Revenue Event Item Debit Memo Item            | `RevenueEventItemDebitMemoItem`            | | Revenue Event Item Invoice Item               | `RevenueEventItemInvoiceItem`              | | Revenue Event Item Invoice Item Adjustment    | `RevenueEventItemInvoiceItemAdjustment`    | | Revenue Event Type                            | `RevenueEventType`                         | | Revenue Schedule                              | `RevenueSchedule`                          | | Revenue Schedule Credit Memo Item             | `RevenueScheduleCreditMemoItem`            | | Revenue Schedule Debit Memo Item              | `RevenueScheduleDebitMemoItem`             | | Revenue Schedule Invoice Item                 | `RevenueScheduleInvoiceItem`               | | Revenue Schedule Invoice Item Adjustment      | `RevenueScheduleInvoiceItemAdjustment`     | | Revenue Schedule Item                         | `RevenueScheduleItem`                      | | Revenue Schedule Item Credit Memo Item        | `RevenueScheduleItemCreditMemoItem`        | | Revenue Schedule Item Debit Memo Item         | `RevenueScheduleItemDebitMemoItem`         | | Revenue Schedule Item Invoice Item            | `RevenueScheduleItemInvoiceItem`           | | Revenue Schedule Item Invoice Item Adjustment | `RevenueScheduleItemInvoiceItemAdjustment` | | Subscription                                  | `Subscription`                             | | Subscription Product Feature                  | `SubscriptionProductFeature`               | | Taxable Item Snapshot                         | `TaxableItemSnapshot`                      | | Taxation Item                                 | `TaxationItem`                             | | Updater Batch                                 | `UpdaterBatch`                             | | Usage                                         | `Usage`                                    |   # noqa: E501

    OpenAPI spec version: 2022-06-02
    Contact: docs@zuora.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class OrderLineItem(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'uom': 'str',
        'accounting_code': 'str',
        'adjustment_liability_accounting_code': 'str',
        'adjustment_revenue_accounting_code': 'str',
        'amended_by_order_on': 'date',
        'amount_per_unit': 'float',
        'bill_target_date': 'date',
        'contract_asset_accounting_code': 'str',
        'contract_liability_accounting_code': 'str',
        'contract_recognized_revenue_accounting_code': 'str',
        'custom_fields': 'OrderLineItemCustomFieldsRetrieveOrderLineItem',
        'deferred_revenue_accounting_code': 'str',
        'description': 'str',
        'exclude_item_billing_from_revenue_accounting': 'bool',
        'exclude_item_booking_from_revenue_accounting': 'bool',
        'item_name': 'str',
        'item_number': 'str',
        'item_state': 'str',
        'item_type': 'str',
        'list_price': 'float',
        'list_price_per_unit': 'float',
        'original_order_date': 'date',
        'product_code': 'str',
        'product_rate_plan_charge_id': 'date',
        'purchase_order_number': 'str',
        'quantity': 'float',
        'recognized_revenue_accounting_code': 'str',
        'related_subscription_number': 'str',
        'revenue_recognition_rule': 'str',
        'tax_code': 'str',
        'tax_mode': 'str',
        'transaction_end_date': 'date',
        'transaction_start_date': 'date',
        'unbilled_receivables_accounting_code': 'str'
    }

    attribute_map = {
        'uom': 'UOM',
        'accounting_code': 'accountingCode',
        'adjustment_liability_accounting_code': 'adjustmentLiabilityAccountingCode',
        'adjustment_revenue_accounting_code': 'adjustmentRevenueAccountingCode',
        'amended_by_order_on': 'amendedByOrderOn',
        'amount_per_unit': 'amountPerUnit',
        'bill_target_date': 'billTargetDate',
        'contract_asset_accounting_code': 'contractAssetAccountingCode',
        'contract_liability_accounting_code': 'contractLiabilityAccountingCode',
        'contract_recognized_revenue_accounting_code': 'contractRecognizedRevenueAccountingCode',
        'custom_fields': 'customFields',
        'deferred_revenue_accounting_code': 'deferredRevenueAccountingCode',
        'description': 'description',
        'exclude_item_billing_from_revenue_accounting': 'excludeItemBillingFromRevenueAccounting',
        'exclude_item_booking_from_revenue_accounting': 'excludeItemBookingFromRevenueAccounting',
        'item_name': 'itemName',
        'item_number': 'itemNumber',
        'item_state': 'itemState',
        'item_type': 'itemType',
        'list_price': 'listPrice',
        'list_price_per_unit': 'listPricePerUnit',
        'original_order_date': 'originalOrderDate',
        'product_code': 'productCode',
        'product_rate_plan_charge_id': 'productRatePlanChargeId',
        'purchase_order_number': 'purchaseOrderNumber',
        'quantity': 'quantity',
        'recognized_revenue_accounting_code': 'recognizedRevenueAccountingCode',
        'related_subscription_number': 'relatedSubscriptionNumber',
        'revenue_recognition_rule': 'revenueRecognitionRule',
        'tax_code': 'taxCode',
        'tax_mode': 'taxMode',
        'transaction_end_date': 'transactionEndDate',
        'transaction_start_date': 'transactionStartDate',
        'unbilled_receivables_accounting_code': 'unbilledReceivablesAccountingCode'
    }

    def __init__(self, uom=None, accounting_code=None, adjustment_liability_accounting_code=None, adjustment_revenue_accounting_code=None, amended_by_order_on=None, amount_per_unit=None, bill_target_date=None, contract_asset_accounting_code=None, contract_liability_accounting_code=None, contract_recognized_revenue_accounting_code=None, custom_fields=None, deferred_revenue_accounting_code=None, description=None, exclude_item_billing_from_revenue_accounting=None, exclude_item_booking_from_revenue_accounting=None, item_name=None, item_number=None, item_state=None, item_type=None, list_price=None, list_price_per_unit=None, original_order_date=None, product_code=None, product_rate_plan_charge_id=None, purchase_order_number=None, quantity=None, recognized_revenue_accounting_code=None, related_subscription_number=None, revenue_recognition_rule=None, tax_code=None, tax_mode=None, transaction_end_date=None, transaction_start_date=None, unbilled_receivables_accounting_code=None):  # noqa: E501
        """OrderLineItem - a model defined in Swagger"""  # noqa: E501
        self._uom = None
        self._accounting_code = None
        self._adjustment_liability_accounting_code = None
        self._adjustment_revenue_accounting_code = None
        self._amended_by_order_on = None
        self._amount_per_unit = None
        self._bill_target_date = None
        self._contract_asset_accounting_code = None
        self._contract_liability_accounting_code = None
        self._contract_recognized_revenue_accounting_code = None
        self._custom_fields = None
        self._deferred_revenue_accounting_code = None
        self._description = None
        self._exclude_item_billing_from_revenue_accounting = None
        self._exclude_item_booking_from_revenue_accounting = None
        self._item_name = None
        self._item_number = None
        self._item_state = None
        self._item_type = None
        self._list_price = None
        self._list_price_per_unit = None
        self._original_order_date = None
        self._product_code = None
        self._product_rate_plan_charge_id = None
        self._purchase_order_number = None
        self._quantity = None
        self._recognized_revenue_accounting_code = None
        self._related_subscription_number = None
        self._revenue_recognition_rule = None
        self._tax_code = None
        self._tax_mode = None
        self._transaction_end_date = None
        self._transaction_start_date = None
        self._unbilled_receivables_accounting_code = None
        self.discriminator = None
        if uom is not None:
            self.uom = uom
        if accounting_code is not None:
            self.accounting_code = accounting_code
        if adjustment_liability_accounting_code is not None:
            self.adjustment_liability_accounting_code = adjustment_liability_accounting_code
        if adjustment_revenue_accounting_code is not None:
            self.adjustment_revenue_accounting_code = adjustment_revenue_accounting_code
        if amended_by_order_on is not None:
            self.amended_by_order_on = amended_by_order_on
        if amount_per_unit is not None:
            self.amount_per_unit = amount_per_unit
        if bill_target_date is not None:
            self.bill_target_date = bill_target_date
        if contract_asset_accounting_code is not None:
            self.contract_asset_accounting_code = contract_asset_accounting_code
        if contract_liability_accounting_code is not None:
            self.contract_liability_accounting_code = contract_liability_accounting_code
        if contract_recognized_revenue_accounting_code is not None:
            self.contract_recognized_revenue_accounting_code = contract_recognized_revenue_accounting_code
        if custom_fields is not None:
            self.custom_fields = custom_fields
        if deferred_revenue_accounting_code is not None:
            self.deferred_revenue_accounting_code = deferred_revenue_accounting_code
        if description is not None:
            self.description = description
        if exclude_item_billing_from_revenue_accounting is not None:
            self.exclude_item_billing_from_revenue_accounting = exclude_item_billing_from_revenue_accounting
        if exclude_item_booking_from_revenue_accounting is not None:
            self.exclude_item_booking_from_revenue_accounting = exclude_item_booking_from_revenue_accounting
        if item_name is not None:
            self.item_name = item_name
        if item_number is not None:
            self.item_number = item_number
        if item_state is not None:
            self.item_state = item_state
        if item_type is not None:
            self.item_type = item_type
        if list_price is not None:
            self.list_price = list_price
        if list_price_per_unit is not None:
            self.list_price_per_unit = list_price_per_unit
        if original_order_date is not None:
            self.original_order_date = original_order_date
        if product_code is not None:
            self.product_code = product_code
        if product_rate_plan_charge_id is not None:
            self.product_rate_plan_charge_id = product_rate_plan_charge_id
        if purchase_order_number is not None:
            self.purchase_order_number = purchase_order_number
        if quantity is not None:
            self.quantity = quantity
        if recognized_revenue_accounting_code is not None:
            self.recognized_revenue_accounting_code = recognized_revenue_accounting_code
        if related_subscription_number is not None:
            self.related_subscription_number = related_subscription_number
        if revenue_recognition_rule is not None:
            self.revenue_recognition_rule = revenue_recognition_rule
        if tax_code is not None:
            self.tax_code = tax_code
        if tax_mode is not None:
            self.tax_mode = tax_mode
        if transaction_end_date is not None:
            self.transaction_end_date = transaction_end_date
        if transaction_start_date is not None:
            self.transaction_start_date = transaction_start_date
        if unbilled_receivables_accounting_code is not None:
            self.unbilled_receivables_accounting_code = unbilled_receivables_accounting_code

    @property
    def uom(self):
        """Gets the uom of this OrderLineItem.  # noqa: E501

        Specifies the units to measure usage.   # noqa: E501

        :return: The uom of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._uom

    @uom.setter
    def uom(self, uom):
        """Sets the uom of this OrderLineItem.

        Specifies the units to measure usage.   # noqa: E501

        :param uom: The uom of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._uom = uom

    @property
    def accounting_code(self):
        """Gets the accounting_code of this OrderLineItem.  # noqa: E501

        The accountingCode for the Order Line Item.   # noqa: E501

        :return: The accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._accounting_code

    @accounting_code.setter
    def accounting_code(self, accounting_code):
        """Sets the accounting_code of this OrderLineItem.

        The accountingCode for the Order Line Item.   # noqa: E501

        :param accounting_code: The accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._accounting_code = accounting_code

    @property
    def adjustment_liability_accounting_code(self):
        """Gets the adjustment_liability_accounting_code of this OrderLineItem.  # noqa: E501

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :return: The adjustment_liability_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._adjustment_liability_accounting_code

    @adjustment_liability_accounting_code.setter
    def adjustment_liability_accounting_code(self, adjustment_liability_accounting_code):
        """Sets the adjustment_liability_accounting_code of this OrderLineItem.

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :param adjustment_liability_accounting_code: The adjustment_liability_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._adjustment_liability_accounting_code = adjustment_liability_accounting_code

    @property
    def adjustment_revenue_accounting_code(self):
        """Gets the adjustment_revenue_accounting_code of this OrderLineItem.  # noqa: E501

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :return: The adjustment_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._adjustment_revenue_accounting_code

    @adjustment_revenue_accounting_code.setter
    def adjustment_revenue_accounting_code(self, adjustment_revenue_accounting_code):
        """Sets the adjustment_revenue_accounting_code of this OrderLineItem.

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :param adjustment_revenue_accounting_code: The adjustment_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._adjustment_revenue_accounting_code = adjustment_revenue_accounting_code

    @property
    def amended_by_order_on(self):
        """Gets the amended_by_order_on of this OrderLineItem.  # noqa: E501

        The date when the rate plan charge is amended through an order or amendment. This field is to standardize the booking date information to increase audit ability and traceability of data between Zuora Billing and Zuora Revenue. It is mapped as the booking date for a sale order line in Zuora Revenue.   # noqa: E501

        :return: The amended_by_order_on of this OrderLineItem.  # noqa: E501
        :rtype: date
        """
        return self._amended_by_order_on

    @amended_by_order_on.setter
    def amended_by_order_on(self, amended_by_order_on):
        """Sets the amended_by_order_on of this OrderLineItem.

        The date when the rate plan charge is amended through an order or amendment. This field is to standardize the booking date information to increase audit ability and traceability of data between Zuora Billing and Zuora Revenue. It is mapped as the booking date for a sale order line in Zuora Revenue.   # noqa: E501

        :param amended_by_order_on: The amended_by_order_on of this OrderLineItem.  # noqa: E501
        :type: date
        """

        self._amended_by_order_on = amended_by_order_on

    @property
    def amount_per_unit(self):
        """Gets the amount_per_unit of this OrderLineItem.  # noqa: E501

        The actual charged amount per unit for the Order Line Item.   # noqa: E501

        :return: The amount_per_unit of this OrderLineItem.  # noqa: E501
        :rtype: float
        """
        return self._amount_per_unit

    @amount_per_unit.setter
    def amount_per_unit(self, amount_per_unit):
        """Sets the amount_per_unit of this OrderLineItem.

        The actual charged amount per unit for the Order Line Item.   # noqa: E501

        :param amount_per_unit: The amount_per_unit of this OrderLineItem.  # noqa: E501
        :type: float
        """

        self._amount_per_unit = amount_per_unit

    @property
    def bill_target_date(self):
        """Gets the bill_target_date of this OrderLineItem.  # noqa: E501

        The target date for the Order Line Item to be picked up by bill run for billing.   # noqa: E501

        :return: The bill_target_date of this OrderLineItem.  # noqa: E501
        :rtype: date
        """
        return self._bill_target_date

    @bill_target_date.setter
    def bill_target_date(self, bill_target_date):
        """Sets the bill_target_date of this OrderLineItem.

        The target date for the Order Line Item to be picked up by bill run for billing.   # noqa: E501

        :param bill_target_date: The bill_target_date of this OrderLineItem.  # noqa: E501
        :type: date
        """

        self._bill_target_date = bill_target_date

    @property
    def contract_asset_accounting_code(self):
        """Gets the contract_asset_accounting_code of this OrderLineItem.  # noqa: E501

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :return: The contract_asset_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._contract_asset_accounting_code

    @contract_asset_accounting_code.setter
    def contract_asset_accounting_code(self, contract_asset_accounting_code):
        """Sets the contract_asset_accounting_code of this OrderLineItem.

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :param contract_asset_accounting_code: The contract_asset_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._contract_asset_accounting_code = contract_asset_accounting_code

    @property
    def contract_liability_accounting_code(self):
        """Gets the contract_liability_accounting_code of this OrderLineItem.  # noqa: E501

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :return: The contract_liability_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._contract_liability_accounting_code

    @contract_liability_accounting_code.setter
    def contract_liability_accounting_code(self, contract_liability_accounting_code):
        """Sets the contract_liability_accounting_code of this OrderLineItem.

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :param contract_liability_accounting_code: The contract_liability_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._contract_liability_accounting_code = contract_liability_accounting_code

    @property
    def contract_recognized_revenue_accounting_code(self):
        """Gets the contract_recognized_revenue_accounting_code of this OrderLineItem.  # noqa: E501

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :return: The contract_recognized_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._contract_recognized_revenue_accounting_code

    @contract_recognized_revenue_accounting_code.setter
    def contract_recognized_revenue_accounting_code(self, contract_recognized_revenue_accounting_code):
        """Sets the contract_recognized_revenue_accounting_code of this OrderLineItem.

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :param contract_recognized_revenue_accounting_code: The contract_recognized_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._contract_recognized_revenue_accounting_code = contract_recognized_revenue_accounting_code

    @property
    def custom_fields(self):
        """Gets the custom_fields of this OrderLineItem.  # noqa: E501


        :return: The custom_fields of this OrderLineItem.  # noqa: E501
        :rtype: OrderLineItemCustomFieldsRetrieveOrderLineItem
        """
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, custom_fields):
        """Sets the custom_fields of this OrderLineItem.


        :param custom_fields: The custom_fields of this OrderLineItem.  # noqa: E501
        :type: OrderLineItemCustomFieldsRetrieveOrderLineItem
        """

        self._custom_fields = custom_fields

    @property
    def deferred_revenue_accounting_code(self):
        """Gets the deferred_revenue_accounting_code of this OrderLineItem.  # noqa: E501

        The deferred revenue accounting code for the Order Line Item.   # noqa: E501

        :return: The deferred_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._deferred_revenue_accounting_code

    @deferred_revenue_accounting_code.setter
    def deferred_revenue_accounting_code(self, deferred_revenue_accounting_code):
        """Sets the deferred_revenue_accounting_code of this OrderLineItem.

        The deferred revenue accounting code for the Order Line Item.   # noqa: E501

        :param deferred_revenue_accounting_code: The deferred_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._deferred_revenue_accounting_code = deferred_revenue_accounting_code

    @property
    def description(self):
        """Gets the description of this OrderLineItem.  # noqa: E501

        The description of the Order Line Item.   # noqa: E501

        :return: The description of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this OrderLineItem.

        The description of the Order Line Item.   # noqa: E501

        :param description: The description of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def exclude_item_billing_from_revenue_accounting(self):
        """Gets the exclude_item_billing_from_revenue_accounting of this OrderLineItem.  # noqa: E501

        The flag to exclude Order Line Item related invoice items, invoice item adjustments, credit memo items, and debit memo items from revenue accounting.  **Note**: This field is only available if you have the Billing - Revenue Integration feature enabled.    # noqa: E501

        :return: The exclude_item_billing_from_revenue_accounting of this OrderLineItem.  # noqa: E501
        :rtype: bool
        """
        return self._exclude_item_billing_from_revenue_accounting

    @exclude_item_billing_from_revenue_accounting.setter
    def exclude_item_billing_from_revenue_accounting(self, exclude_item_billing_from_revenue_accounting):
        """Sets the exclude_item_billing_from_revenue_accounting of this OrderLineItem.

        The flag to exclude Order Line Item related invoice items, invoice item adjustments, credit memo items, and debit memo items from revenue accounting.  **Note**: This field is only available if you have the Billing - Revenue Integration feature enabled.    # noqa: E501

        :param exclude_item_billing_from_revenue_accounting: The exclude_item_billing_from_revenue_accounting of this OrderLineItem.  # noqa: E501
        :type: bool
        """

        self._exclude_item_billing_from_revenue_accounting = exclude_item_billing_from_revenue_accounting

    @property
    def exclude_item_booking_from_revenue_accounting(self):
        """Gets the exclude_item_booking_from_revenue_accounting of this OrderLineItem.  # noqa: E501

        The flag to exclude Order Line Item from revenue accounting.  **Note**: This field is only available if you have the Billing - Revenue Integration feature enabled.    # noqa: E501

        :return: The exclude_item_booking_from_revenue_accounting of this OrderLineItem.  # noqa: E501
        :rtype: bool
        """
        return self._exclude_item_booking_from_revenue_accounting

    @exclude_item_booking_from_revenue_accounting.setter
    def exclude_item_booking_from_revenue_accounting(self, exclude_item_booking_from_revenue_accounting):
        """Sets the exclude_item_booking_from_revenue_accounting of this OrderLineItem.

        The flag to exclude Order Line Item from revenue accounting.  **Note**: This field is only available if you have the Billing - Revenue Integration feature enabled.    # noqa: E501

        :param exclude_item_booking_from_revenue_accounting: The exclude_item_booking_from_revenue_accounting of this OrderLineItem.  # noqa: E501
        :type: bool
        """

        self._exclude_item_booking_from_revenue_accounting = exclude_item_booking_from_revenue_accounting

    @property
    def item_name(self):
        """Gets the item_name of this OrderLineItem.  # noqa: E501

        The name of the Order Line Item.   # noqa: E501

        :return: The item_name of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._item_name

    @item_name.setter
    def item_name(self, item_name):
        """Sets the item_name of this OrderLineItem.

        The name of the Order Line Item.   # noqa: E501

        :param item_name: The item_name of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._item_name = item_name

    @property
    def item_number(self):
        """Gets the item_number of this OrderLineItem.  # noqa: E501

        The number for the Order Line Item.   # noqa: E501

        :return: The item_number of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._item_number

    @item_number.setter
    def item_number(self, item_number):
        """Sets the item_number of this OrderLineItem.

        The number for the Order Line Item.   # noqa: E501

        :param item_number: The item_number of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._item_number = item_number

    @property
    def item_state(self):
        """Gets the item_state of this OrderLineItem.  # noqa: E501

        The state of the Order Line Item. See [Order Line Item states, Order states, and state transitions](https://knowledgecenter.zuora.com/Billing/Subscriptions/Orders/Order_Line_Items/AB_Order_Line_Item_States_and_Order_States) for more information.   # noqa: E501

        :return: The item_state of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._item_state

    @item_state.setter
    def item_state(self, item_state):
        """Sets the item_state of this OrderLineItem.

        The state of the Order Line Item. See [Order Line Item states, Order states, and state transitions](https://knowledgecenter.zuora.com/Billing/Subscriptions/Orders/Order_Line_Items/AB_Order_Line_Item_States_and_Order_States) for more information.   # noqa: E501

        :param item_state: The item_state of this OrderLineItem.  # noqa: E501
        :type: str
        """
        allowed_values = ["Executing", "SentToBilling", "Complete", "Cancelled"]  # noqa: E501
        if item_state not in allowed_values:
            raise ValueError(
                "Invalid value for `item_state` ({0}), must be one of {1}"  # noqa: E501
                .format(item_state, allowed_values)
            )

        self._item_state = item_state

    @property
    def item_type(self):
        """Gets the item_type of this OrderLineItem.  # noqa: E501

        The type of the Order Line Item.    # noqa: E501

        :return: The item_type of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._item_type

    @item_type.setter
    def item_type(self, item_type):
        """Sets the item_type of this OrderLineItem.

        The type of the Order Line Item.    # noqa: E501

        :param item_type: The item_type of this OrderLineItem.  # noqa: E501
        :type: str
        """
        allowed_values = ["Product", "Fee", "Services"]  # noqa: E501
        if item_type not in allowed_values:
            raise ValueError(
                "Invalid value for `item_type` ({0}), must be one of {1}"  # noqa: E501
                .format(item_type, allowed_values)
            )

        self._item_type = item_type

    @property
    def list_price(self):
        """Gets the list_price of this OrderLineItem.  # noqa: E501

        The extended list price for an order line item, calculated by the formula: listPrice = listPricePerUnit * quantity   # noqa: E501

        :return: The list_price of this OrderLineItem.  # noqa: E501
        :rtype: float
        """
        return self._list_price

    @list_price.setter
    def list_price(self, list_price):
        """Sets the list_price of this OrderLineItem.

        The extended list price for an order line item, calculated by the formula: listPrice = listPricePerUnit * quantity   # noqa: E501

        :param list_price: The list_price of this OrderLineItem.  # noqa: E501
        :type: float
        """

        self._list_price = list_price

    @property
    def list_price_per_unit(self):
        """Gets the list_price_per_unit of this OrderLineItem.  # noqa: E501

        The list price per unit for the Order Line Item.   # noqa: E501

        :return: The list_price_per_unit of this OrderLineItem.  # noqa: E501
        :rtype: float
        """
        return self._list_price_per_unit

    @list_price_per_unit.setter
    def list_price_per_unit(self, list_price_per_unit):
        """Sets the list_price_per_unit of this OrderLineItem.

        The list price per unit for the Order Line Item.   # noqa: E501

        :param list_price_per_unit: The list_price_per_unit of this OrderLineItem.  # noqa: E501
        :type: float
        """

        self._list_price_per_unit = list_price_per_unit

    @property
    def original_order_date(self):
        """Gets the original_order_date of this OrderLineItem.  # noqa: E501

        The date when the rate plan charge is created through an order or amendment. This field is to standardize the booking date information to increase audit ability and traceability of data between Zuora Billing and Zuora Revenue. It is mapped as the booking date for a sale order line in Zuora Revenue.   # noqa: E501

        :return: The original_order_date of this OrderLineItem.  # noqa: E501
        :rtype: date
        """
        return self._original_order_date

    @original_order_date.setter
    def original_order_date(self, original_order_date):
        """Sets the original_order_date of this OrderLineItem.

        The date when the rate plan charge is created through an order or amendment. This field is to standardize the booking date information to increase audit ability and traceability of data between Zuora Billing and Zuora Revenue. It is mapped as the booking date for a sale order line in Zuora Revenue.   # noqa: E501

        :param original_order_date: The original_order_date of this OrderLineItem.  # noqa: E501
        :type: date
        """

        self._original_order_date = original_order_date

    @property
    def product_code(self):
        """Gets the product_code of this OrderLineItem.  # noqa: E501

        The product code for the Order Line Item.   # noqa: E501

        :return: The product_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._product_code

    @product_code.setter
    def product_code(self, product_code):
        """Sets the product_code of this OrderLineItem.

        The product code for the Order Line Item.   # noqa: E501

        :param product_code: The product_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._product_code = product_code

    @property
    def product_rate_plan_charge_id(self):
        """Gets the product_rate_plan_charge_id of this OrderLineItem.  # noqa: E501

        Id of a Product Rate Plan Charge. Only one-time charges are supported.   # noqa: E501

        :return: The product_rate_plan_charge_id of this OrderLineItem.  # noqa: E501
        :rtype: date
        """
        return self._product_rate_plan_charge_id

    @product_rate_plan_charge_id.setter
    def product_rate_plan_charge_id(self, product_rate_plan_charge_id):
        """Sets the product_rate_plan_charge_id of this OrderLineItem.

        Id of a Product Rate Plan Charge. Only one-time charges are supported.   # noqa: E501

        :param product_rate_plan_charge_id: The product_rate_plan_charge_id of this OrderLineItem.  # noqa: E501
        :type: date
        """

        self._product_rate_plan_charge_id = product_rate_plan_charge_id

    @property
    def purchase_order_number(self):
        """Gets the purchase_order_number of this OrderLineItem.  # noqa: E501

        Used by customers to specify the Purchase Order Number provided by the buyer.   # noqa: E501

        :return: The purchase_order_number of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._purchase_order_number

    @purchase_order_number.setter
    def purchase_order_number(self, purchase_order_number):
        """Sets the purchase_order_number of this OrderLineItem.

        Used by customers to specify the Purchase Order Number provided by the buyer.   # noqa: E501

        :param purchase_order_number: The purchase_order_number of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._purchase_order_number = purchase_order_number

    @property
    def quantity(self):
        """Gets the quantity of this OrderLineItem.  # noqa: E501

        The quantity of units, such as the number of authors in a hosted wiki service.   # noqa: E501

        :return: The quantity of this OrderLineItem.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this OrderLineItem.

        The quantity of units, such as the number of authors in a hosted wiki service.   # noqa: E501

        :param quantity: The quantity of this OrderLineItem.  # noqa: E501
        :type: float
        """

        self._quantity = quantity

    @property
    def recognized_revenue_accounting_code(self):
        """Gets the recognized_revenue_accounting_code of this OrderLineItem.  # noqa: E501

        The recognized revenue accounting code for the Order Line Item.   # noqa: E501

        :return: The recognized_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._recognized_revenue_accounting_code

    @recognized_revenue_accounting_code.setter
    def recognized_revenue_accounting_code(self, recognized_revenue_accounting_code):
        """Sets the recognized_revenue_accounting_code of this OrderLineItem.

        The recognized revenue accounting code for the Order Line Item.   # noqa: E501

        :param recognized_revenue_accounting_code: The recognized_revenue_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._recognized_revenue_accounting_code = recognized_revenue_accounting_code

    @property
    def related_subscription_number(self):
        """Gets the related_subscription_number of this OrderLineItem.  # noqa: E501

        Use this field to relate an order line item to an subscription. Specify this field to the subscription number of the subscription to relate.   # noqa: E501

        :return: The related_subscription_number of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._related_subscription_number

    @related_subscription_number.setter
    def related_subscription_number(self, related_subscription_number):
        """Sets the related_subscription_number of this OrderLineItem.

        Use this field to relate an order line item to an subscription. Specify this field to the subscription number of the subscription to relate.   # noqa: E501

        :param related_subscription_number: The related_subscription_number of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._related_subscription_number = related_subscription_number

    @property
    def revenue_recognition_rule(self):
        """Gets the revenue_recognition_rule of this OrderLineItem.  # noqa: E501

        The Revenue Recognition rule for the Order Line Item.   # noqa: E501

        :return: The revenue_recognition_rule of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._revenue_recognition_rule

    @revenue_recognition_rule.setter
    def revenue_recognition_rule(self, revenue_recognition_rule):
        """Sets the revenue_recognition_rule of this OrderLineItem.

        The Revenue Recognition rule for the Order Line Item.   # noqa: E501

        :param revenue_recognition_rule: The revenue_recognition_rule of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._revenue_recognition_rule = revenue_recognition_rule

    @property
    def tax_code(self):
        """Gets the tax_code of this OrderLineItem.  # noqa: E501

        The tax code for the Order Line Item.   # noqa: E501

        :return: The tax_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._tax_code

    @tax_code.setter
    def tax_code(self, tax_code):
        """Sets the tax_code of this OrderLineItem.

        The tax code for the Order Line Item.   # noqa: E501

        :param tax_code: The tax_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._tax_code = tax_code

    @property
    def tax_mode(self):
        """Gets the tax_mode of this OrderLineItem.  # noqa: E501

        The tax mode for the Order Line Item.   # noqa: E501

        :return: The tax_mode of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._tax_mode

    @tax_mode.setter
    def tax_mode(self, tax_mode):
        """Sets the tax_mode of this OrderLineItem.

        The tax mode for the Order Line Item.   # noqa: E501

        :param tax_mode: The tax_mode of this OrderLineItem.  # noqa: E501
        :type: str
        """
        allowed_values = ["TaxInclusive", "TaxExclusive"]  # noqa: E501
        if tax_mode not in allowed_values:
            raise ValueError(
                "Invalid value for `tax_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(tax_mode, allowed_values)
            )

        self._tax_mode = tax_mode

    @property
    def transaction_end_date(self):
        """Gets the transaction_end_date of this OrderLineItem.  # noqa: E501

        The date a transaction is completed. The default value of this field is the transaction start date. Also, the value of this field should always equal or be later than the value of the `transactionStartDate` field.   # noqa: E501

        :return: The transaction_end_date of this OrderLineItem.  # noqa: E501
        :rtype: date
        """
        return self._transaction_end_date

    @transaction_end_date.setter
    def transaction_end_date(self, transaction_end_date):
        """Sets the transaction_end_date of this OrderLineItem.

        The date a transaction is completed. The default value of this field is the transaction start date. Also, the value of this field should always equal or be later than the value of the `transactionStartDate` field.   # noqa: E501

        :param transaction_end_date: The transaction_end_date of this OrderLineItem.  # noqa: E501
        :type: date
        """

        self._transaction_end_date = transaction_end_date

    @property
    def transaction_start_date(self):
        """Gets the transaction_start_date of this OrderLineItem.  # noqa: E501

        The date a transaction starts. The default value of this field is the order date.   # noqa: E501

        :return: The transaction_start_date of this OrderLineItem.  # noqa: E501
        :rtype: date
        """
        return self._transaction_start_date

    @transaction_start_date.setter
    def transaction_start_date(self, transaction_start_date):
        """Sets the transaction_start_date of this OrderLineItem.

        The date a transaction starts. The default value of this field is the order date.   # noqa: E501

        :param transaction_start_date: The transaction_start_date of this OrderLineItem.  # noqa: E501
        :type: date
        """

        self._transaction_start_date = transaction_start_date

    @property
    def unbilled_receivables_accounting_code(self):
        """Gets the unbilled_receivables_accounting_code of this OrderLineItem.  # noqa: E501

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :return: The unbilled_receivables_accounting_code of this OrderLineItem.  # noqa: E501
        :rtype: str
        """
        return self._unbilled_receivables_accounting_code

    @unbilled_receivables_accounting_code.setter
    def unbilled_receivables_accounting_code(self, unbilled_receivables_accounting_code):
        """Sets the unbilled_receivables_accounting_code of this OrderLineItem.

        The accounting code on the Order Line Item object for customers using [Zuora Billing - Revenue Integration](https://knowledgecenter.zuora.com/Zuora_Revenue/Zuora_Billing_-_Revenue_Integration).   # noqa: E501

        :param unbilled_receivables_accounting_code: The unbilled_receivables_accounting_code of this OrderLineItem.  # noqa: E501
        :type: str
        """

        self._unbilled_receivables_accounting_code = unbilled_receivables_accounting_code

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(OrderLineItem, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OrderLineItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
