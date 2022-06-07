"""
Created on Fri Jan 26 16:14:45 2018
@author: jskro
python class ApiGateway , inherits from Aws:
"""

import os, re
import utilities.lists as lists, utilities.filesystem as fs, utilities.base as base
from utilities.base import nvl
from utilities.dicts import set_attributes
from utilities.DictList import DictList
from utilities.Request import Request
from aws.aws_base import Aws
from utilities.Entity import Entity
from uuid import uuid4

class ApiGateway(Aws):
    """
    #class variables: same for all instances of class 
    """
    """initialization"""
    def __init__(self,username,environ_params=False):
        super().__init__(username=username,environ_params=environ_params)
        self.client=self.get_client(service_name='apigateway')
    """	
    def __iter__(self):
        # generator of iterable, eg (iterable)
        yield(self)
    def __len__(self):
        v=0 # compute current number of items in instance
        return(v)
    def __contains__(self,item):
        bool=False # rule on item returning True/False
        return(bool)
    """
    
    """property setters"""
    
    
    """class functions"""
    
    # REST API: CRUD
    def getRestApi(self,api_name,**kwargs):
        """ get RestApi instance from api object in RestApiList """
        try:
            #body
            r=self.RestApiList().get_by_key(api_name)
            if r==None:
                KeyError('api_name not in RestApiList {0}'.format(api_name))
            RestApi0=RestApi(r,self.client)
            RestApi0.aws_region=self.aws_region
            RestApi0.root_user_arn=self.root_user_arn
            RestApi0.hostname='https://{0}.execute-api.{1}.amazonaws.com'.format(RestApi0.id,self.aws_region)
        except Exception as e:
            print('error in getRestApi')
            raise e
        #return value
        return(RestApi0)       
    
    def create_rest_api(self,api_name,dsc=None,**kwargs):
        """ create or get existing rest api """
        try:
            #body
            if api_name not in self.list_rest_apis():
                response = self.client.create_rest_api(
                name=api_name,
                description=dsc,
                binaryMediaTypes=[
                    'application/pdf',
                ],
                apiKeySource=kwargs.get('apiKeySource','AUTHORIZER'),
                endpointConfiguration={
                    'types': ['REGIONAL']
                }
                )
                self.last_res=response
            else:
                print('restapi exists: {0}'.format(api_name))
            # retrieve the api
            RestApi0=self.getRestApi(api_name)  
        except Exception as e:
            print('error in create_rest_api')
            raise e
        #return value
        return(RestApi0)
        
    def RestApiList(self,x=None,**kwargs):
        """ docstring """
        try:
            #body
            RestApisList = DictList(self.client.get_rest_apis()['items'])
            if len(RestApisList)>0:
                RestApisList.set_default_key('name')
        except Exception as e:
            print('error in RestApiList')
            raise e
        #return value
        return(RestApisList)

    def list_rest_apis(self):
       #body         
       return(self.RestApiList().query('name'))
       
    def getResource(self,api_name,resource_name):
       #body         
       v=self.getRestApi(api_name).getResource(resource_name)
       return(v)
       
    # account level operations:
    # update_account_cloudwatch_log_role: see https://kennbrodhagen.net/2016/07/23/how-to-enable-logging-for-api-gateway/ or https://docs.aws.amazon.com/cli/latest/reference/apigateway/update-account.html
    def update_account_cloudwatch_log_role(self, role_arn):
       """ """
       #body         
       response = self.client.update_account(
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/cloudwatchRoleArn',
                    'value': role_arn
                },
            ]
        )
       return(response)
       
    # getEvent: RestApi.getEvent for "default" api_name
    def getEvent(self, api_name, stage):
       """ convinience function for Event object of RestApi.api_name """
       Event=self.getRestApi(api_name).getEvent(stage=stage)
       return(Event)
        
"""subclasses"""
LIMIT=99
class RestApi(Entity):
    """
    #class variables: same for all instances of class 
    """
    """initialization"""
    def __init__(self,r,client,**kwargs):
         super().__init__(r)
         self.client=client
         self.api_id=self.id
         
         # get the REST api root path (/), root path id (parent_id)
         Resources=self.ResourceList()
         if len(Resources)>0:
             self.root_path=Resources.subset({'path':'/'},index=0)
             self.root_path_id=self.root_path['id']
             self.parent_id=self.root_path_id
         else:
             self.root_path=None
             self.root_path_id=None
             self.parent_id=None
        
    # resources: create, list     
    def ResourceList(self,x=None,**kwargs):
        """ docstring """
        try:
            #body
            self.last_res=self.client.get_resources(restApiId=self.api_id,limit=LIMIT)
            resource_list=self.last_res['items']
            if len(resource_list)>0:
                for r in resource_list:
                    if r.get('pathPart')==None:
                        r['pathPart']=r['path']
            self.resource_list=resource_list
            ApiResourceList = DictList(self.resource_list)
            try:
                ApiResourceList.set_default_key('pathPart')
            except Exception as e:
                print(e)
        except Exception as e:
            print('error in ResourceList')
            raise e
        #return value
        return(ApiResourceList)   
    
    def list_resources(self):
       #body         
       v=self.ResourceList().query('pathPart')
       return(v)
       
    def getResource(self,pathPart,**kwargs):
        """ get the api/resource by pathPart """
        #body
        r=self.ResourceList().get_by_key(pathPart)
        if r==None:
            KeyError('pathPart not in ResourceList {0}'.format(pathPart))
        Resource0=Resource(r,self.client,self.api_id,**{'aws_region':self.aws_region,'root_user_arn':self.root_user_arn,'hostname':self.hostname})
        #return value
        return(Resource0)

    def create_resource(self,new_resource):
        """ creates resource and returns as Resource instance """
        #body
        if new_resource not in self.list_resources():
            response = self.client.create_resource(
                restApiId=self.api_id,
                parentId=self.parent_id,
                pathPart=new_resource
            )
            self.last_res=response
        else:
            print('resource exists {0}'.format(new_resource))
        Resource0=self.getResource(new_resource) #Resource(response,self.client,self.api_id,**{'aws_region':self.aws_region,'root_user_arn':self.root_user_arn})
        return(Resource0)
     
    # CRUD on deployments: create, read (list)
    def create_deployment(self,stage='staging',dsc='new deployment'):
       #body         
       r = self.client.create_deployment(
            restApiId=self.api_id,
            stageName=stage,
            description=dsc
            )
       return(r)

    def Deployments(self,x=None,**kwargs):
        """ docstring """
        try:
            #body
            response = self.client.get_deployments(
                restApiId=self.api_id,
                limit=500
            )
            self.last_res=response
            if response['items']==[]:
                Deployments=DictList(response['items'])
            else:
                Deployments=DictList(response['items']).set_default_key('id')
        except Exception as e:
            print('error in Deployments')
            raise e
        #return value
        return(Deployments)

    def list_deployments(self):
       #body         
       v=self.Deployments().sort('createdDate').query(['id','description','createdDate'])
       return(v)

    def last_deployment_id(self):
       #body         
       last_deployment_id=lists.last_itm(self.list_deployments())
       return(last_deployment_id)
   
    # Stages: from the API deployment 
    def Stages(self,x=None,**kwargs):
        """ get the stages of the (last?) deployment """
        #body
        response = self.client.get_stages(
        restApiId=self.api_id,
        #deploymentId='string'
        )
        self.last_res=response
        Stages=ApiStageList(self.last_res['item'])
        #return value
        return(Stages)
    
    def getStages(self,x=None,**kwargs):
        """ alias for Stages """
        return(self.Stages(x=x,**kwargs))
        
    def list_stages(self):
       """ returns the name and deployment id of all stages associated with this restapi """      
       v=self.getStages().select(['stageName','deploymentId'])
       return(v)
       
    # stage event
    # get stage event at the RestApi level
    def getEvent(self,stage='staging',**kwargs):
       """args: stage, optional: body,params """
       v=self.getStages().get_by_key(stage).getEvent(**kwargs)
       return(v)
       
class Resource(Entity):
    """
    #class variables: same for all instances of class 
    """
    """initialization"""
    def __init__(self,r,client,api_id,**kwargs):
         super().__init__(r)
         self.client=client
         self.api_id=api_id
         self.resource_id=self.id
         for ky in kwargs:
             if ky in ['aws_region','root_user_arn','hostname']:
                 setattr(self,ky,kwargs[ky])
         self.source_arn='arn:aws:execute-api:{0}:{1}:{2}/*/POST{3}'.format(self.aws_region,self.root_user_arn,self.api_id,self.path)
         
    # CRUD on self         
    def get(self):
       response = self.client.get_resource(
       restApiId=self.api_id,
       resourceId=self.resource_id
       )
       return(response)
       
    def delete(self):
       #body         
       response = self.client.delete_resource(
       restApiId=self.api_id,
       resourceId=self.resource_id
       )
       return(response)
       
    # CRUD on self.methods
    def list_methods(self):
       #body         
       v=self.get().get('resourceMethods',[]) 
       v=[ky for ky in v]
       return(v)

    def create_method(self,method,auth_type='NONE',request_params={}):
       #body        
       if method in self.list_methods():
           print('resource method exists {0}/{1}'.format(self.pathPart,method))
           response={}
       else:
           response = self.client.put_method(
                    restApiId=self.api_id,
                    resourceId=self.resource_id,
                    httpMethod=method,
                    authorizationType=auth_type,
                    requestParameters=request_params
            )
       return(response)
       
    def delete_method(self,method):
       #body         
       res=self.getMethod(method).delete()
       return(res)       

    # create method but returns Method instance
    def getMethod(self,method):
       #body         
       response = self.client.get_method(
        restApiId=self.api_id,
        resourceId=self.resource_id,
        httpMethod=method
        )
       self=Method(response,client=self.client,api_id=self.api_id,resource_id=self.resource_id)
       return(self)

    # integrate with lambda function
    def put_lambda_integration(self,lambda_name,method='POST',include_stage_variables=True):
        """ integrating RestApi.Resource with lambda function requires two methods - POST and OPTIONS """
        try:
            #body
            # arguments:
            # method='POST' # always needs to be POST for lambda integration???
            # put the OPTIONS method integration
            if not 'OPTIONS' in self.list_methods():
                raise KeyError('method OPTIONS does not exist')
            Method0=self.getMethod('OPTIONS')
            
            # try to remove existing integration and response
            try:
               response = self.client.delete_method_response(
                    restApiId=Method0.api_id,
                    resourceId=Method0.resource_id,
                    httpMethod='OPTIONS',
                    statusCode='200'
                    )
               response = self.client.delete_integration(
                    restApiId=Method0.api_id,
                    resourceId=Method0.resource_id,
                    httpMethod='OPTIONS'
               )
            except Exception as e:
               pass
            
            response = self.client.put_method_response(
                restApiId=Method0.api_id,
                resourceId=Method0.resource_id,
                httpMethod=Method0.httpMethod,
                statusCode='200',
                responseParameters= {'method.response.header.Access-Control-Allow-Headers': False,
               'method.response.header.Access-Control-Allow-Methods': False,
               'method.response.header.Access-Control-Allow-Origin': False},
                responseModels={
                    "application/json": "Empty"
                }
            )
            
            response = self.client.put_integration(
                restApiId=Method0.api_id,
                resourceId=Method0.resource_id,
                httpMethod=Method0.httpMethod,
                type='MOCK',
                passthroughBehavior='WHEN_NO_MATCH',
                #cacheNamespace='string',
                #cacheKeyParameters=[    ],
                contentHandling='CONVERT_TO_TEXT',
                timeoutInMillis=29000,
                requestTemplates={
                'application/json': '{"statusCode": 200}'
                }
            )
            response = self.client.put_integration_response(
                restApiId=Method0.api_id,
                resourceId=Method0.resource_id,
                httpMethod=Method0.httpMethod,
                statusCode='200',
               # selectionPattern='string',
                responseParameters={'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"},
                responseTemplates={'application/json': 'Empty'},
            )
            
            # put the POST method integration
            if not method in self.list_methods():
                raise KeyError('method {0} does not exist'.format(method))
            Method0=self.getMethod(method)    
            # try to remove existing integration and response
            try:
               response = self.client.delete_method_response(
                    restApiId=Method0.api_id,
                    resourceId=Method0.resource_id,
                    httpMethod='POST',
                    statusCode='200'
                    )
               response = self.client.delete_integration(
                    restApiId=Method0.api_id,
                    resourceId=Method0.resource_id,
                    httpMethod='POST'
               )
            except Exception as e:
               pass
            
            # set CORS header on method response
            response = self.client.put_method_response(
                restApiId=Method0.api_id,
                resourceId=Method0.resource_id,
                httpMethod=Method0.httpMethod,
                #credentials=lambda_execution_role , 
                statusCode='200',
                responseParameters= {'method.response.header.Access-Control-Allow-Origin': False},
                responseModels={
                    'application/json': 'Empty'
                }
            )
            self.last_res=response

            # put the integration with lambda function
            service_api='2015-03-31/functions/arn:aws:lambda:{0}:{1}:function:{2}:'.format(self.aws_region,self.root_user_arn,lambda_name)
            service_api=service_api + '${stageVariables.stage}/invocations' if include_stage_variables else service_api
            lambda_uri='arn:aws:apigateway:{0}:{1}:path/{2}'.format(self.aws_region,'lambda',service_api)
            response = self.client.put_integration(
                restApiId=Method0.api_id,
                resourceId=Method0.resource_id,
                httpMethod=Method0.httpMethod,
                type='AWS_PROXY',
                uri=lambda_uri,
                connectionType='INTERNET',
                passthroughBehavior='WHEN_NO_MATCH',
                integrationHttpMethod =method,
                #cacheNamespace='string',
                cacheKeyParameters=[    ],
                contentHandling='CONVERT_TO_TEXT',
                timeoutInMillis=29000
            )
            self.last_res=response

            # put integration response
            response = self.client.put_integration_response(
                restApiId=Method0.api_id,
                resourceId=Method0.resource_id,
                httpMethod=Method0.httpMethod,
                statusCode='200',
               # selectionPattern='string',
                responseParameters={'method.response.header.Access-Control-Allow-Origin': "'*'"},
                responseTemplates={'application/json': 'Empty'}
            )
            self.last_res=response

        except Exception as e:
            print('error in put_lambda_integration')
            raise e
        #return value
        return({'uri':lambda_uri})    

    def give_lambda_permission(self,lambda_client,lambda_name,alias=None,action='lambda:InvokeFunction',method='POST',**kwargs):
        """ add permission to source_arn to invoke lambda function
            always POST """
        #body   
        lambda_client=lambda_client.client if hasattr(lambda_client,'client') else lambda_client
        source_arn='arn:aws:execute-api:{0}:{1}:{2}/*/{3}{4}'.format(self.aws_region,self.root_user_arn,self.api_id,method,self.path)
        response = lambda_client.add_permission(
            FunctionName=lambda_name + ':'+alias if alias!=None else lambda_name,
            StatementId=str(uuid4()),
            Action=action,
            Principal='apigateway.amazonaws.com',
            SourceArn=source_arn
        )
        self.last_res=response
        # optional printing
        self.__print__(self.last_res,**kwargs)
        return(self.last_res)
        
    # invocation
    def get_endpoint(self,stage='staging'):
       #body         
       stage='/' + stage if stage!=None else ''
       print('endpoint stage is: {0}'.format(stage))
       v=self.hostname + stage + self.path
       return(v)
       
    def invoke_method_endpoint(self,stage,method,data=None):
       #body      
       endpoint=self.get_endpoint(stage=stage)   
       res=Request().send_request(endpoint,method=method,data=data,raise_error=False,return_response=True)
       return(res)
   
class Method(Entity):
    """
    #class variables: same for all instances of class 
    """
    """initialization"""
    def __init__(self,r, **kwargs):
         super().__init__(r)
         set_attributes(self,kwargs,['client','api_id','resource_id'])
         
    def put_response_method(self,statusCode='200',responseParameters={},responseModels={}):
       """ add method response to method """
       #body         
       response = self.client.put_method_response(
            restApiId=self.api_id,
            resourceId=self.resource_id,
            httpMethod=self.httpMethod,
            statusCode=statusCode,
            responseParameters=responseParameters,
            responseModels=responseModels
        )
       return(response)
   
    def delete(self):
       #body         
       response = self.client.delete_method(
        restApiId=self.api_id,
        resourceId=self.resource_id,
        httpMethod=self.httpMethod
        )
       return(response)
        
    # method integration
    def get_integration(self):
        #body         
        response = self.client.get_integration(
            restApiId=self.api_id,
            resourceId=self.resource_id,
            httpMethod=self.httpMethod
        )
        self.last_res=response
        return(response)

    def put_method_mock_integration(self,**kwargs):
        """ add integration of MOCK type to method """
        try:
            #body
            # put the MOCK integration            
            response = self.client.put_method_response(
                restApiId=self.api_id,
                resourceId=self.resource_id,
                httpMethod=self.httpMethod,
                statusCode='200',
                responseParameters= {'method.response.header.Access-Control-Allow-Headers': False,
               'method.response.header.Access-Control-Allow-Methods': False,
               'method.response.header.Access-Control-Allow-Origin': False},
                responseModels={
                    'application/json': 'Empty'
                }
            )
            
            response = self.client.put_integration(
                restApiId=self.api_id,
                resourceId=self.resource_id,
                httpMethod=self.httpMethod,
                type='MOCK',
                passthroughBehavior='WHEN_NO_MATCH',
                cacheNamespace='string',
                cacheKeyParameters=[    ],
                timeoutInMillis=29000
            )
            
            response = self.client.put_integration_response(
                restApiId=self.api_id,
                resourceId=self.resource_id,
                httpMethod=self.httpMethod,
                statusCode='200',
               # selectionPattern='string',
                responseParameters={'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                'method.response.header.Access-Control-Allow-Methods': "'POST,OPTIONS'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"},
                responseTemplates={'application/json': 'Empty'}
            )
            
        except Exception as e:
            print('error in put_mock_integration')
            raise e
        #return value
        return(self)             

class ApiStageList(DictList):
    """
    #class variables: same for all instances of class 
    """
    """initialization"""
    def __init__(self,x):
        super().__init__(x,generator=lambda r: ApiStage(r),default_key='stageName', return_object=True,idkeys='stageName')
        
        
class ApiStage(Entity):
    """
    #class variables: same for all instances of class 
    """
    """initialization"""
    def __init__(self,x):
        super().__init__(x=x)
        if not hasattr(self,'variables'):
            self.variables={}
            
    """property setters"""
        
    def getEvent(self,body=None,params=None):
        """ from self.variables set event.stageVariables, optionally add body and parameters """
        ApiEvent0=ApiEvent({'stageVariables':self.variables})
        if body!=None:
            ApiEvent0.set_body(body)
        if params!=None:
            ApiEvent0.update_params(params)
        #return value
        return(ApiEvent0)

    def list_stages(self):
      """"""
      return(self.query('stageName'))
      
import json
from utilities.base import from_kwargs
from utilities.Dict2 import Dict2

class ApiEvent(Dict2):
    """
    Legacy version for backward compatibility
    """
    default_keys=['stageVariables','headers','queryStringParameters']
    placeholders=['stage','dbvariables','dbcredential']
    
    """initialization"""
    def __init__(self, x={}, body=None):
        super().__init__(x)
        self.event=x
        
        # set the default keys to {} if not dictionary
        self.__set_defaults__(self.default_keys)
        
        # from headers get the referer (could be none)
        self.referer=self['headers'].get('referer')
        
        # set the placeholder attributes to None
        base.set_attributes(self,self.placeholders)
        self.stagevariables=self['stageVariables']

        # set database variables (type + credential)
        if self.stagevariables!={}:
            dbtype,dbname,dbport,dbpw,dbuser,dbhost=from_kwargs(self.stagevariables,'dbtype','dbName','dbPort','dbPw','dbUser','dbHost')
            self.dbcredential={'dbname':dbname,'port':dbport,'pw':dbpw, 'host':dbhost, 'un':dbuser}
            self.dbtype=dbtype
            if self.dbtype!=None:
                self.dbcredential['dbtype']=self.dbtype # add dbtype to dbcredential to initialize dbconnection for event
            self.dbvariables={'dbtype':dbtype,'dbcredential':self.dbcredential}
            self.stage=self.stagevariables['stage']
            
        # set event body   
        if body==None:
            body=self.event.get('body')         
        self.set_body(x=body)
        
    """property setters"""
    
    
    """class functions"""
    def __set_defaults__(self,keys,default={}):
        for ky in keys:
           if not isinstance(self.get(ky),dict):
               self[ky]=default
               
    def set_body(self,x=None,**kwargs):
        """ set event.body """
        if isinstance(x,dict):  
            # dump serialized body as key
            self['body']=json.dumps(x)
            self.body=self['body']
        elif isinstance(x,str):
            self['body']=x
            self.body=self['body']
        else:
            self.body=None
        #return value
        return(self)
    
    def setbody(self,x=None,**kwargs): # alias
        return(self.set_body(x,**kwargs))
        
    def get_body(self, **kwargs):
        """ return body as Dict2 """
        bodystr=nvl(self.get('body','{}'),'{}')
        body=json.loads(bodystr)
        return(Dict2(body))
        
    def getbody(self,**kwargs): # alias
        return(self.get_body(**kwargs))
        
    def update_body(self, updates):
        """ docstring """
        body=self.get_body().update_keys(updates)
        self.set_body(x=body)
        return(self)    
        
    def update_params(self,params):
        """ updates event parameters not in body """
        for ky in params:
            if not ky in ['body']:
                self[ky]=params.get(ky)
        #return value
        return(self)

    def getQueryStringParams(self):
        return(self.get('queryStringParameters'))
        
    def updateQueryStringParameters(self, updates):
        """ queryStringParameters are always set as a dict """
        self['queryStringParameters'].update(updates)
        return(self)     

    # connect to RDS database
    def getRDSConnection(self , dbtype='postgres'):
        """ connects to RDS database of postgres type (default) """
        from db_utilities.dbConnection import dbConnection
        dbconn=dbConnection(credential=self.dbcredential,dbtype=dbtype)
        return(dbconn)

from utilities.Entity import Entity
class ApiEventV2(Entity):
    """
    #class variables: same for all instances of class 
    """
    placeholders=['stage','dbvariables']
    
    """initialization"""
    def __init__(self, x={}, body=None):
        if body!=None:
           x['body']=body
        super().__init__(x,placeholders=self.placeholders)
        self.event=x
        self.stagevariables=self.get('stageVariables')
        
        # set database variables (type + credential)
        if self.stagevariables!=None:
            dbtype,dbname,dbport,dbpw,dbuser,dbhost=from_kwargs(self.stagevariables,'dbtype','dbName','dbPort','dbPw','dbUser','dbHost')
            self.dbcredential={'dbname':dbname,'port':dbport,'pw':dbpw, 'host':dbhost, 'un':dbuser}
            self.dbtype=dbtype
            self.dbvariables={'dbtype':dbtype,'dbcredential':self.dbcredential}
            self.stage=self.stagevariables['stage']
            
        # set event body   
        if body==None:
            body=self.event.get('body')         
        self.set_body(x=body)
        
    """property setters"""
    
    
    """class functions"""
    def set_body(self,x=None,**kwargs):
        """ set event.body """
        if isinstance(x,dict) or isinstance(x,str):  
            # dump serialized body as key
            self.x['body']=json.dumps(x) if isinstance(x,dict) else x
        else:
            self.x['body']=None
        self.body=self.x['body']
        #return value
        return(self)
    
    def setbody(self,x=None,**kwargs): # alias
        return(self.set_body(x,**kwargs))
        
    def get_body(self, **kwargs):
        """ return body as Dict2 """
        body=json.loads(self.x.get('body','{}'))
        return(Dict2(body))
        
    def getbody(self,**kwargs): # alias
        return(self.get_body(**kwargs))
        
    def update_body(self, updates):
        """ update the event.body """
        body=self.get_body().update_keys(updates)
        self.set_body(x=body)
        return(self)    
        
    def update_params(self,params):
        """ updates event parameters not in body """
        for ky in params:
            if not ky in ['body']:
                self[ky]=params.get(ky)
        #return value
        return(self)

    def updateQueryStringParameters(self, updates):
      """ update the queryStringParameters key """
      current_parameters=self.x.get('queryStringParameters')
      if not isinstance(current_parameters,dict):
          self['queryStringParameters']=updates
      else:
          self['queryStringParameters'].update(updates)
      self.x['queryStringParameters'].update()
      return(self)     

    # connect to RDS database
    def getRDSConnection(self , dbtype='postgres'):
      """ connects to RDS database of postgres type (default) """
      from db_utilities.dbConnection import dbConnection
      dbconn=dbConnection(credential=self.dbcredential,dbtype=dbtype)
      return(dbconn)

# inherits from ApiEvent
class ApiTestEvent(ApiEvent):
    """
    #class variables: same for all instances of class 
    """
    TESTCASEPATHS=['deck-testcases']
    METADATAPATHS=['deck-metadata']
    S3BUCKETNAMES=['deck-metadata']
    EVENTFILENAME='events.json'
    
    """initialization"""
    def __init__(self, from_s3=False, stage='staging',host='deck', testcase=None):
        
        # place holders
        self.from_s3=from_s3
        
        if not self.from_s3:
            eventsjson=self.import_event()
            eventjson=eventsjson[host][stage]
        else:
            raise ValueError('froms3 not configured')
            
        super().__init__(x=eventjson)
        
        if testcase != None:
            self.importtestcase(testcase)
        
    """property setters"""
    
    
    """class functions"""
    def import_event(self):
      """ import event json from location, set as input """
      paths=fs.findpaths(self.METADATAPATHS)
      if len(paths)==0:
          raise ValueError('no path found in METADATAPATHS: {0}'.format(', '.join(self.METADATAPATHS)))
      path=paths[0]
      fpath=os.path.join(path,self.EVENTFILENAME)
      if os.path.exists(fpath) and not os.path.isdir(fpath):
          f=open(fpath,'r')
          r=json.loads(f.read())
          f.close()          
      else:
          raise FileNotFoundError(fpath)
          
      return(r)

    def __testcase_path__(self):
      paths=fs.findpaths(self.TESTCASEPATHS)
      if len(paths)==0:
          raise ValueError('no path found in TESTCASEPATHS: {0}'.format(', '.join(self.TESTCASEPATHS)))
      return(paths[0])
        
    def list_testcases(self):
      """ docstring """
      fnames=[f for f in os.listdir(self.__testcase_path__()) if re.findall('.*?\\.(json|txt)$',f)!=[]]  
      return(fnames)
      
    def importtestcase(self, testcasename):
      """ docstring """
      fname=os.path.join(self.__testcase_path__(),testcasename)
      with open(fname, "r") as testcase:
        body=json.loads(testcase.read())   
        testcase.close()
      
      self.set_body(body)
      return(self)

    def exporttestcase(self, json_obj, testcasename):
        fname=os.path.join(self.__testcase_path__(),testcasename)
        with open(fname, "w") as testcase:
            testcase.write(json.dumps(json_obj))
            testcase.close()
        print('testcase exported as {0}'.format(fname))
        return(self)
        
"""class exceptions, inherit from Exception"""
class error1(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
class error2(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors


