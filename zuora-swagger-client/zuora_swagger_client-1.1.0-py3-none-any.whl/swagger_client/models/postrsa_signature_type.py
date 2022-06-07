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

class POSTRSASignatureType(object):
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
        'iban': 'str',
        'account_id': 'str',
        'authorization_amount': 'float',
        'bank_branch_code': 'str',
        'bank_check_digit': 'str',
        'bank_city': 'str',
        'bank_postal_code': 'str',
        'bank_street_name': 'str',
        'bank_street_number': 'str',
        'business_identification_code': 'str',
        'city_black_list': 'str',
        'city_white_list': 'str',
        'currency': 'str',
        'device_session_id': 'str',
        'gateway_name': 'str',
        'id': 'str',
        'key': 'str',
        'locale': 'str',
        'max_consecutive_payment_failures': 'int',
        'method': 'str',
        'page_id': 'str',
        'param_gw_options__option': 'str',
        'param_supported_types': 'str',
        'passthrough_12345': 'str',
        'payment_gateway': 'str',
        'payment_retry_window': 'int',
        'pm_id': 'str',
        'signature': 'str',
        'signature_type': 'str',
        'style': 'str',
        'submit_enabled': 'bool',
        'tenant_id': 'str',
        'token': 'str',
        'uri': 'str',
        'use_default_retry_rule': 'bool'
    }

    attribute_map = {
        'iban': 'IBAN',
        'account_id': 'accountId',
        'authorization_amount': 'authorizationAmount',
        'bank_branch_code': 'bankBranchCode',
        'bank_check_digit': 'bankCheckDigit',
        'bank_city': 'bankCity',
        'bank_postal_code': 'bankPostalCode',
        'bank_street_name': 'bankStreetName',
        'bank_street_number': 'bankStreetNumber',
        'business_identification_code': 'businessIdentificationCode',
        'city_black_list': 'cityBlackList',
        'city_white_list': 'cityWhiteList',
        'currency': 'currency',
        'device_session_id': 'deviceSessionId',
        'gateway_name': 'gatewayName',
        'id': 'id',
        'key': 'key',
        'locale': 'locale',
        'max_consecutive_payment_failures': 'maxConsecutivePaymentFailures',
        'method': 'method',
        'page_id': 'pageId',
        'param_gw_options__option': 'param_gwOptions_[*option*]',
        'param_supported_types': 'param_supportedTypes',
        'passthrough_12345': 'passthrough[1,2,3,4,5]',
        'payment_gateway': 'paymentGateway',
        'payment_retry_window': 'paymentRetryWindow',
        'pm_id': 'pmId',
        'signature': 'signature',
        'signature_type': 'signatureType',
        'style': 'style',
        'submit_enabled': 'submitEnabled',
        'tenant_id': 'tenantId',
        'token': 'token',
        'uri': 'uri',
        'use_default_retry_rule': 'useDefaultRetryRule'
    }

    def __init__(self, iban=None, account_id=None, authorization_amount=None, bank_branch_code=None, bank_check_digit=None, bank_city=None, bank_postal_code=None, bank_street_name=None, bank_street_number=None, business_identification_code=None, city_black_list=None, city_white_list=None, currency=None, device_session_id=None, gateway_name=None, id=None, key=None, locale=None, max_consecutive_payment_failures=None, method=None, page_id=None, param_gw_options__option=None, param_supported_types=None, passthrough_12345=None, payment_gateway=None, payment_retry_window=None, pm_id=None, signature=None, signature_type=None, style=None, submit_enabled=None, tenant_id=None, token=None, uri=None, use_default_retry_rule=None):  # noqa: E501
        """POSTRSASignatureType - a model defined in Swagger"""  # noqa: E501
        self._iban = None
        self._account_id = None
        self._authorization_amount = None
        self._bank_branch_code = None
        self._bank_check_digit = None
        self._bank_city = None
        self._bank_postal_code = None
        self._bank_street_name = None
        self._bank_street_number = None
        self._business_identification_code = None
        self._city_black_list = None
        self._city_white_list = None
        self._currency = None
        self._device_session_id = None
        self._gateway_name = None
        self._id = None
        self._key = None
        self._locale = None
        self._max_consecutive_payment_failures = None
        self._method = None
        self._page_id = None
        self._param_gw_options__option = None
        self._param_supported_types = None
        self._passthrough_12345 = None
        self._payment_gateway = None
        self._payment_retry_window = None
        self._pm_id = None
        self._signature = None
        self._signature_type = None
        self._style = None
        self._submit_enabled = None
        self._tenant_id = None
        self._token = None
        self._uri = None
        self._use_default_retry_rule = None
        self.discriminator = None
        if iban is not None:
            self.iban = iban
        if account_id is not None:
            self.account_id = account_id
        if authorization_amount is not None:
            self.authorization_amount = authorization_amount
        if bank_branch_code is not None:
            self.bank_branch_code = bank_branch_code
        if bank_check_digit is not None:
            self.bank_check_digit = bank_check_digit
        if bank_city is not None:
            self.bank_city = bank_city
        if bank_postal_code is not None:
            self.bank_postal_code = bank_postal_code
        if bank_street_name is not None:
            self.bank_street_name = bank_street_name
        if bank_street_number is not None:
            self.bank_street_number = bank_street_number
        if business_identification_code is not None:
            self.business_identification_code = business_identification_code
        if city_black_list is not None:
            self.city_black_list = city_black_list
        if city_white_list is not None:
            self.city_white_list = city_white_list
        if currency is not None:
            self.currency = currency
        if device_session_id is not None:
            self.device_session_id = device_session_id
        if gateway_name is not None:
            self.gateway_name = gateway_name
        if id is not None:
            self.id = id
        if key is not None:
            self.key = key
        if locale is not None:
            self.locale = locale
        if max_consecutive_payment_failures is not None:
            self.max_consecutive_payment_failures = max_consecutive_payment_failures
        self.method = method
        self.page_id = page_id
        if param_gw_options__option is not None:
            self.param_gw_options__option = param_gw_options__option
        if param_supported_types is not None:
            self.param_supported_types = param_supported_types
        if passthrough_12345 is not None:
            self.passthrough_12345 = passthrough_12345
        if payment_gateway is not None:
            self.payment_gateway = payment_gateway
        if payment_retry_window is not None:
            self.payment_retry_window = payment_retry_window
        if pm_id is not None:
            self.pm_id = pm_id
        if signature is not None:
            self.signature = signature
        if signature_type is not None:
            self.signature_type = signature_type
        if style is not None:
            self.style = style
        if submit_enabled is not None:
            self.submit_enabled = submit_enabled
        if tenant_id is not None:
            self.tenant_id = tenant_id
        if token is not None:
            self.token = token
        self.uri = uri
        if use_default_retry_rule is not None:
            self.use_default_retry_rule = use_default_retry_rule

    @property
    def iban(self):
        """Gets the iban of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The iban of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._iban

    @iban.setter
    def iban(self, iban):
        """Sets the iban of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param iban: The iban of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._iban = iban

    @property
    def account_id(self):
        """Gets the account_id of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The account_id of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param account_id: The account_id of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def authorization_amount(self):
        """Gets the authorization_amount of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The authorization_amount of this POSTRSASignatureType.  # noqa: E501
        :rtype: float
        """
        return self._authorization_amount

    @authorization_amount.setter
    def authorization_amount(self, authorization_amount):
        """Sets the authorization_amount of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param authorization_amount: The authorization_amount of this POSTRSASignatureType.  # noqa: E501
        :type: float
        """

        self._authorization_amount = authorization_amount

    @property
    def bank_branch_code(self):
        """Gets the bank_branch_code of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The bank_branch_code of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._bank_branch_code

    @bank_branch_code.setter
    def bank_branch_code(self, bank_branch_code):
        """Sets the bank_branch_code of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param bank_branch_code: The bank_branch_code of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._bank_branch_code = bank_branch_code

    @property
    def bank_check_digit(self):
        """Gets the bank_check_digit of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The bank_check_digit of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._bank_check_digit

    @bank_check_digit.setter
    def bank_check_digit(self, bank_check_digit):
        """Sets the bank_check_digit of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param bank_check_digit: The bank_check_digit of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._bank_check_digit = bank_check_digit

    @property
    def bank_city(self):
        """Gets the bank_city of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The bank_city of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._bank_city

    @bank_city.setter
    def bank_city(self, bank_city):
        """Sets the bank_city of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param bank_city: The bank_city of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._bank_city = bank_city

    @property
    def bank_postal_code(self):
        """Gets the bank_postal_code of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The bank_postal_code of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._bank_postal_code

    @bank_postal_code.setter
    def bank_postal_code(self, bank_postal_code):
        """Sets the bank_postal_code of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param bank_postal_code: The bank_postal_code of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._bank_postal_code = bank_postal_code

    @property
    def bank_street_name(self):
        """Gets the bank_street_name of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The bank_street_name of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._bank_street_name

    @bank_street_name.setter
    def bank_street_name(self, bank_street_name):
        """Sets the bank_street_name of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param bank_street_name: The bank_street_name of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._bank_street_name = bank_street_name

    @property
    def bank_street_number(self):
        """Gets the bank_street_number of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The bank_street_number of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._bank_street_number

    @bank_street_number.setter
    def bank_street_number(self, bank_street_number):
        """Sets the bank_street_number of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param bank_street_number: The bank_street_number of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._bank_street_number = bank_street_number

    @property
    def business_identification_code(self):
        """Gets the business_identification_code of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The business_identification_code of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._business_identification_code

    @business_identification_code.setter
    def business_identification_code(self, business_identification_code):
        """Sets the business_identification_code of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for Bank Transfer - Direct Debit.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param business_identification_code: The business_identification_code of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._business_identification_code = business_identification_code

    @property
    def city_black_list(self):
        """Gets the city_black_list of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The city_black_list of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._city_black_list

    @city_black_list.setter
    def city_black_list(self, city_black_list):
        """Sets the city_black_list of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param city_black_list: The city_black_list of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._city_black_list = city_black_list

    @property
    def city_white_list(self):
        """Gets the city_white_list of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The city_white_list of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._city_white_list

    @city_white_list.setter
    def city_white_list(self, city_white_list):
        """Sets the city_white_list of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param city_white_list: The city_white_list of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._city_white_list = city_white_list

    @property
    def currency(self):
        """Gets the currency of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The currency of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param currency: The currency of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def device_session_id(self):
        """Gets the device_session_id of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The device_session_id of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._device_session_id

    @device_session_id.setter
    def device_session_id(self, device_session_id):
        """Sets the device_session_id of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param device_session_id: The device_session_id of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._device_session_id = device_session_id

    @property
    def gateway_name(self):
        """Gets the gateway_name of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The gateway_name of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._gateway_name

    @gateway_name.setter
    def gateway_name(self, gateway_name):
        """Sets the gateway_name of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param gateway_name: The gateway_name of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._gateway_name = gateway_name

    @property
    def id(self):
        """Gets the id of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The id of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param id: The id of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def key(self):
        """Gets the key of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The key of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param key: The key of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def locale(self):
        """Gets the locale of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The locale of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._locale

    @locale.setter
    def locale(self, locale):
        """Sets the locale of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param locale: The locale of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._locale = locale

    @property
    def max_consecutive_payment_failures(self):
        """Gets the max_consecutive_payment_failures of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The max_consecutive_payment_failures of this POSTRSASignatureType.  # noqa: E501
        :rtype: int
        """
        return self._max_consecutive_payment_failures

    @max_consecutive_payment_failures.setter
    def max_consecutive_payment_failures(self, max_consecutive_payment_failures):
        """Sets the max_consecutive_payment_failures of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param max_consecutive_payment_failures: The max_consecutive_payment_failures of this POSTRSASignatureType.  # noqa: E501
        :type: int
        """

        self._max_consecutive_payment_failures = max_consecutive_payment_failures

    @property
    def method(self):
        """Gets the method of this POSTRSASignatureType.  # noqa: E501

        The type of the request. Set it to POST.   # noqa: E501

        :return: The method of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """Sets the method of this POSTRSASignatureType.

        The type of the request. Set it to POST.   # noqa: E501

        :param method: The method of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """
        if method is None:
            raise ValueError("Invalid value for `method`, must not be `None`")  # noqa: E501

        self._method = method

    @property
    def page_id(self):
        """Gets the page_id of this POSTRSASignatureType.  # noqa: E501

        The page id of your Payment Pages 2.0 form. Click **Show Page Id** next to the Payment Page name in the Hosted Page List to retrieve the page id.   # noqa: E501

        :return: The page_id of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._page_id

    @page_id.setter
    def page_id(self, page_id):
        """Sets the page_id of this POSTRSASignatureType.

        The page id of your Payment Pages 2.0 form. Click **Show Page Id** next to the Payment Page name in the Hosted Page List to retrieve the page id.   # noqa: E501

        :param page_id: The page_id of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """
        if page_id is None:
            raise ValueError("Invalid value for `page_id`, must not be `None`")  # noqa: E501

        self._page_id = page_id

    @property
    def param_gw_options__option(self):
        """Gets the param_gw_options__option of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The param_gw_options__option of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._param_gw_options__option

    @param_gw_options__option.setter
    def param_gw_options__option(self, param_gw_options__option):
        """Sets the param_gw_options__option of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param param_gw_options__option: The param_gw_options__option of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._param_gw_options__option = param_gw_options__option

    @property
    def param_supported_types(self):
        """Gets the param_supported_types of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The param_supported_types of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._param_supported_types

    @param_supported_types.setter
    def param_supported_types(self, param_supported_types):
        """Sets the param_supported_types of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param param_supported_types: The param_supported_types of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._param_supported_types = param_supported_types

    @property
    def passthrough_12345(self):
        """Gets the passthrough_12345 of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.  Note: Although up to 15 passthrough parameters can be supported when passing in your client parameters, only the first 5 parameters are used for signature generation and validation.   # noqa: E501

        :return: The passthrough_12345 of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._passthrough_12345

    @passthrough_12345.setter
    def passthrough_12345(self, passthrough_12345):
        """Sets the passthrough_12345 of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.  Note: Although up to 15 passthrough parameters can be supported when passing in your client parameters, only the first 5 parameters are used for signature generation and validation.   # noqa: E501

        :param passthrough_12345: The passthrough_12345 of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._passthrough_12345 = passthrough_12345

    @property
    def payment_gateway(self):
        """Gets the payment_gateway of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The payment_gateway of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._payment_gateway

    @payment_gateway.setter
    def payment_gateway(self, payment_gateway):
        """Sets the payment_gateway of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param payment_gateway: The payment_gateway of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._payment_gateway = payment_gateway

    @property
    def payment_retry_window(self):
        """Gets the payment_retry_window of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The payment_retry_window of this POSTRSASignatureType.  # noqa: E501
        :rtype: int
        """
        return self._payment_retry_window

    @payment_retry_window.setter
    def payment_retry_window(self, payment_retry_window):
        """Sets the payment_retry_window of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param payment_retry_window: The payment_retry_window of this POSTRSASignatureType.  # noqa: E501
        :type: int
        """

        self._payment_retry_window = payment_retry_window

    @property
    def pm_id(self):
        """Gets the pm_id of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The pm_id of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._pm_id

    @pm_id.setter
    def pm_id(self, pm_id):
        """Sets the pm_id of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters specific for credit cards.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param pm_id: The pm_id of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._pm_id = pm_id

    @property
    def signature(self):
        """Gets the signature of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The signature of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._signature

    @signature.setter
    def signature(self, signature):
        """Sets the signature of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param signature: The signature of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._signature = signature

    @property
    def signature_type(self):
        """Gets the signature_type of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The signature_type of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._signature_type

    @signature_type.setter
    def signature_type(self, signature_type):
        """Sets the signature_type of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param signature_type: The signature_type of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._signature_type = signature_type

    @property
    def style(self):
        """Gets the style of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The style of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._style

    @style.setter
    def style(self, style):
        """Sets the style of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param style: The style of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._style = style

    @property
    def submit_enabled(self):
        """Gets the submit_enabled of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The submit_enabled of this POSTRSASignatureType.  # noqa: E501
        :rtype: bool
        """
        return self._submit_enabled

    @submit_enabled.setter
    def submit_enabled(self, submit_enabled):
        """Sets the submit_enabled of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param submit_enabled: The submit_enabled of this POSTRSASignatureType.  # noqa: E501
        :type: bool
        """

        self._submit_enabled = submit_enabled

    @property
    def tenant_id(self):
        """Gets the tenant_id of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The tenant_id of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, tenant_id):
        """Sets the tenant_id of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param tenant_id: The tenant_id of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._tenant_id = tenant_id

    @property
    def token(self):
        """Gets the token of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The token of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param token: The token of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def uri(self):
        """Gets the uri of this POSTRSASignatureType.  # noqa: E501

        The URL that the Payment Page will be served from. * For US Cloud 1 Production environment: Use https://na.zuora.com/apps/PublicHostedPageLite.do * For US Cloud 1 Sandbox environment: Use https://sandbox.na.zuora.com/apps/PublicHostedPageLite.d * For US Cloud 2 Production environment: Use https://www.zuora.com/apps/PublicHostedPageLite.do * For US Cloud 2 API Sandbox environment: Use https://apisandbox.zuora.com/apps/PublicHostedPageLite.do * For US Central Sandbox environment: Use https://test.zuora.com/apps/PublicHostedPageLite.do * For EU Cloud Production environment: Use https://eu.zuora.com/apps/PublicHostedPageLite.do * For EU Cloud Sandbox environment: Use https://sandbox.eu.zuora.com/apps/PublicHostedPageLite.do * For EU Central Sandbox environment: Use https://test.eu.zuora.com/apps/PublicHostedPageLite.do   # noqa: E501

        :return: The uri of this POSTRSASignatureType.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this POSTRSASignatureType.

        The URL that the Payment Page will be served from. * For US Cloud 1 Production environment: Use https://na.zuora.com/apps/PublicHostedPageLite.do * For US Cloud 1 Sandbox environment: Use https://sandbox.na.zuora.com/apps/PublicHostedPageLite.d * For US Cloud 2 Production environment: Use https://www.zuora.com/apps/PublicHostedPageLite.do * For US Cloud 2 API Sandbox environment: Use https://apisandbox.zuora.com/apps/PublicHostedPageLite.do * For US Central Sandbox environment: Use https://test.zuora.com/apps/PublicHostedPageLite.do * For EU Cloud Production environment: Use https://eu.zuora.com/apps/PublicHostedPageLite.do * For EU Cloud Sandbox environment: Use https://sandbox.eu.zuora.com/apps/PublicHostedPageLite.do * For EU Central Sandbox environment: Use https://test.eu.zuora.com/apps/PublicHostedPageLite.do   # noqa: E501

        :param uri: The uri of this POSTRSASignatureType.  # noqa: E501
        :type: str
        """
        if uri is None:
            raise ValueError("Invalid value for `uri`, must not be `None`")  # noqa: E501

        self._uri = uri

    @property
    def use_default_retry_rule(self):
        """Gets the use_default_retry_rule of this POSTRSASignatureType.  # noqa: E501

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :return: The use_default_retry_rule of this POSTRSASignatureType.  # noqa: E501
        :rtype: bool
        """
        return self._use_default_retry_rule

    @use_default_retry_rule.setter
    def use_default_retry_rule(self, use_default_retry_rule):
        """Sets the use_default_retry_rule of this POSTRSASignatureType.

        An optional client parameter that can be used for validating client-side HPM parameters.  See [Client parameters for Payment Pages 2.0](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/J_Client_Parameters_for_Payment_Pages_2.0)  and [Validate client-side HPM parameters](https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/LA_Hosted_Payment_Pages/B_Payment_Pages_2.0/F_Generate_the_Digital_Signature_for_Payment_Pages_2.0#Validate_Client-side_HPM_Parameters)  for details.   # noqa: E501

        :param use_default_retry_rule: The use_default_retry_rule of this POSTRSASignatureType.  # noqa: E501
        :type: bool
        """

        self._use_default_retry_rule = use_default_retry_rule

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
        if issubclass(POSTRSASignatureType, dict):
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
        if not isinstance(other, POSTRSASignatureType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
