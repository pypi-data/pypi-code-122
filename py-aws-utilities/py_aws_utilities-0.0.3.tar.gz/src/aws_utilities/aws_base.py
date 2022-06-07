# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 16:14:45 2018

@author: jskro
python class Aws , inherits from None

writer.write_class_function('set_user',small=True)   


"""
import os, boto3, datetime as dt
from dateutil import tz
from utilities.base import nvl,typename
from utilities.filesystem import load_file, save_file
from utilities.dicts import get_from_dict, dictValidator
from utilities.DictList import DictList

# constants
AWS_CLASS_MODULES=['Lambda','S3']

class Aws():
    """
    #class variables: same for all instances of class 
    """
    DEFAULT_AWS_REGION='eu-west-1'
    REQUIRED_VERSION_BOTO3= '1.10.35' #'1.12.3'
    PATHS=['/tmp','tmp', os.getcwd()]
    EXCLUDE_PATHS=['/var/task']
    
    """initialization"""
    def __init__(self, username=None, aws_region=None, environ_params=False, include_security_token=True, aws_credentials=None, raise_error=False):
        # check required version boto3
        if boto3.__version__<self.REQUIRED_VERSION_BOTO3:
           #raise BOTO3_VERSION_ERROR('required version is {0}, current version is {1}'.format(self.REQUIRED_VERSION_BOTO3,boto3.__version__))
           print('required version is {0}, current version is {1}'.format(self.REQUIRED_VERSION_BOTO3,boto3.__version__))
        
        # check passed arguments
        if username==None and environ_params==False and aws_credentials==None:
           raise ValueError('username is None with environ_params False')
        elif username!=None:
           if aws_credentials == None:
           # get aws_credentials from file
           # import aws credential from aws credentials file in AWS_CRED_PATH
              if 'AWS_CRED_PATH' in os.environ:
                 self.aws_cred_path=os.environ['AWS_CRED_PATH']
                 if os.path.exists(self.aws_cred_path) and os.path.isfile(self.aws_cred_path):
                    self.aws_credentials=load_file(fname=self.aws_cred_path,as_json=True) 
                    self.aws_credential_path=self.aws_cred_path
                    environ_params=False
                 elif raise_error:
                    raise FileNotFoundError(self.aws_cred_path)
                 else:
                    print('failing over to environment variables...')
                    environ_params=True                        
              elif raise_error:
                 raise AWS_CREDENTIAL_PATH_ERROR('AWS_CRED_PATH not in environ')
              else:
                 print('failing over to environment variables...')
                 environ_params=True
           else:
              self.aws_credentials=aws_credentials
              if username in self.aws_credentials:
                 environ_params=False
              elif raise_error:
                 raise KeyError('username not in passed aws_credentials')
              else:
                 print('failing over to environment variables...')
                 environ_params=True                   
        else:
           environ_params=True # use environment variables
            
        # initialization from environment parameters or aws_credentials
        self.environ_params=environ_params
        if self.environ_params: # get AWS parameters from environment
            self.aws_credential = {'AWS_ACCESS_KEY_ID':os.environ['AWS_ACCESS_KEY_ID'],'AWS_SECRET_ACCESS_KEY':os.environ['AWS_SECRET_ACCESS_KEY']}
            # set session token in credential
            if 'AWS_SESSION_TOKEN' in dict(os.environ) and include_security_token:
                self.aws_credential['AWS_SESSION_TOKEN']=dict(os.environ)['AWS_SESSION_TOKEN']
            # aws parameters
            self.username='default-user'
            self.aws_credentials={self.username:self.aws_credential}
            aws_region=os.environ['AWS_DEFAULT_REGION']
            self.aws_credential_path=None
        else: # get AWS parameters from aws_credentials 
            self.username=username
            self.aws_credential=self.get_credential(self.username) if self.username != None else None
            
        # arn role    
        self.arn=self.aws_credential.get('ARN_ROLE')
        # root_user_arn (root user arn)
        self.root_user_arn=self.aws_credential.get('root_user_arn')
        self.account_id=str(self.aws_credential.get('account_id'))
        
        # aws settings
        # region + timezones
        self.aws_region=nvl(aws_region,self.DEFAULT_AWS_REGION)
        if self.aws_region=='eu-west-1':
            self.tzname='Europe/Dublin'
            self.localzone=tz.gettz(self.tzname)
        else:
            self.tzname=''
            self.localzone=None
            print('timezone not set for region {0}'.format(self.aws_region))        
        
        # defaults for aws classes
        # aws/lambda
        self.LAMBDA_KWARGS=self.aws_credential.get('LAMBDA_KWARGS',{})
        
        # settings
        self.PRINT=True
        self.MAXITEMS=50
        self.PAGESIZE=100
        
    """property setters"""
   
    """class functions"""
    def list_users(self):
       users=list(self.aws_credentials.keys())
       #return value
       return(users)
       
    def get_credential(self,username):
       aws_credential=get_from_dict(self.aws_credentials,username,exception_to_raise=AwsCredentialNotFound)
       credentialValidator=dictValidator(schema={'keys':{'required':['AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY']}},raise_error=True)
       credentialValidator.validate(aws_credential)
       #return value
       return(aws_credential)

    # utilities: error handling, response parsing
    def parse_response(self,res,**kwargs):
       """ parses a boto3 response as DictList (if contains list value) """
       parsed=None
       for ky in res:
          if ky != 'ResponseMetadata':
             res2=res[ky]
             break
       if isinstance(res2,list):
           parsed=DictList(res2,**kwargs)
       elif isinstance(res2,dict):
          for ky,v in res2.items():
             if isinstance(v,list):
                parsed=DictList(v,**kwargs)
                break
       else:
          raise TypeError(typename(res2))
       if parsed==None:
          raise ValueError('no list value in response')
       #return value
       return(parsed)

    def __paginated_request__(self,client,funcname,items_key,**kwargs):
        """ client: aws service object, funcname: function to paginate, items_key: key of paginated response containing list of function responses, **kwargs: function args """
        try:
            #body
            if not hasattr(client,funcname):
                raise KeyError('function not found {0}'.format(funcname))
            if not client.can_paginate(funcname):
                raise FUNCTION_CANNOT_BE_PAGINATED(funcname)
            paginator = client.get_paginator(funcname)
            response_iterator = paginator.paginate(
                PaginationConfig={
                    'MaxItems': self.MAXITEMS,
                    'PageSize': self.PAGESIZE,
                    'StartingToken': None, 
                }, **kwargs
            )
            reslist=[]
            items_key_found=False
            for r in response_iterator:
                if not items_key_found:
                    if items_key in r:
                        items_key_found=True
                    else:
                        for ky in r:
                            if type(r[ky])==list:
                                items_key=ky
                                items_key_found=True
                            else:
                                items_key_found=False
                if items_key_found:
                    reslist=reslist+r[items_key]
        except Exception as e:
            print('error in __paginated_request__')
            raise e
        #return value
        return(reslist)     
        
    # time
    def __servertime__(self):
       #body         
       v=dt.datetime.now().astimezone(self.localzone)
       return(v)
    
    # error handling    
    def raise_aws_response_error(self, r, msg=None):
       """ raise error is aws boto3 request returns response status code <= 299 """ 
       # body
       # set r as last_res
       self.last_res=r
          
       if 'ResponseMetadata' in r:
          res_status_code=r['ResponseMetadata']['HTTPStatusCode']
          b=False if res_status_code<=299 else True
       else:
          res_status_code=r['ResponseMetadata']
          b=False if res_status_code<=299 else True
       if b:
          msg=nvl(msg,'AWS returns status code {0}'.format(res_status_code))
          raise AwsResponseError(msg)
       #return value
       return()
    
    # clients
    # get service client
    def get_client(self,service_name,username=None):
       #body
       if self.aws_credential == None:
          raise AWS_CREDENTIAL_NOT_SET() 
       self.aws_credential=self.aws_credential if username==None else self.get_credential(username)
       if 'AWS_SESSION_TOKEN' in self.aws_credential:
          # initiaize client with security token
          client = boto3.client(service_name,aws_access_key_id = self.aws_credential['AWS_ACCESS_KEY_ID'], 
                       aws_secret_access_key = self.aws_credential['AWS_SECRET_ACCESS_KEY'],
                       aws_session_token =self.aws_credential['AWS_SESSION_TOKEN']
                       )
       else:
          client = boto3.client(service_name, aws_access_key_id = self.aws_credential['AWS_ACCESS_KEY_ID'], 
                       aws_secret_access_key = self.aws_credential['AWS_SECRET_ACCESS_KEY'])
       #return value
       return(client)
       
    def get_service(self,service_name,username=None):
       """ alias for get_client """
       return(self.get_client(service_name,username))
       
    def persistent_clients(self,*args):
       """ returns map of standard aws clients/service objects,
            made persistent by storing in globals() """
       #body
       clients={}
       for ky in args:
          if not ky in globals():
             client=self.get_client(ky,self.username)
             globals()[ky]=client
          clients[ky]=globals()[ky]
       #return value
       return(clients)
    
    def get_persistent_client(self,clientname):
       """ returns single persistent client """
       return(self.persistent_clients(clientname)[clientname])
    
    # get persistent aws class instances
    def get_persistent_objects(self,**kwargs):
        """ persistent client objects from package aws """
        #body
        import aws, importlib
        outargs=[]
        for awsclass,v in kwargs.items():
            if awsclass in AWS_CLASS_MODULES and v:
                    if awsclass in globals():
                        print('get instance {0} from globals()'.format(awsclass))
                    else:
                        mod=importlib.import_module(awsclass,aws)
                        class0=getattr(mod,awsclass)
                        print('initialize {0}'.format(awsclass))
                        globals()[awsclass]=class0(username=self.username) #, environ_params=self.environ_params)
            else:
                raise AwsClassNotDefined(awsclass)
            outargs.append(globals()[awsclass])
        #return value
        return(tuple(outargs))

    def execute_client_function(self, function_name, kwargs={}, client=None, items=None):
        """ execute client.function_name with kwargs, return DictList of items """
        #body
        client = self.client if hasattr(self,'client') else client
        if isinstance(client,str):
            client = self.get_client(client)
        if client==None:
            raise ValueError('client is None')
        if hasattr(client,function_name):
            client_func=getattr(client,function_name)
            if not callable(client_func):
                raise AWS_BASE_CLIENT_FUNCTION_ERROR(function_name)
        else:
            raise AWS_BASE_CLIENT_FUNCTION_ERROR(function_name)
        res=client_func(**kwargs)
        if dict(res):
            if items!=None and items in res:
                reslist=res[items]
            elif [ky for ky in res if type(res[ky])==list]!=[]:
                reslist=res[[ky for ky in res if type(res[ky])==list][0]]
            else:
                raise AWS_RESPONSE_LIST_ERROR(list(res.keys()))
        else:
            raise AWS_RESPONSE_LIST_ERROR('res is of type {0}'.format(type(res)))
        DictList0=DictList(reslist)
        #return value
        return(DictList0)

    # paths, directories on Lambda
    def get_writable_path(self, raise_error=True, checkwriteable=True):
       """ get first path in PATHS if exists """        
       paths=[p for p in self.PATHS if os.access(p, os.W_OK) or (os.path.exists(p) and not checkwriteable and p not in self.EXCLUDE_PATHS)]
       if len(paths)==0 and raise_error: 
           raise ValueError('no path writable: {}'.format(self.PATHS))
       elif len(paths)==0:
           path=None
       else:
           path=paths[0]
       return(path)
       
    def listdir(self):
       """ shorthand for  """
       return(os.listdir(self.get_writable_path(False,False)))
      
    def openfile(self, fname):
      """ shorthand for load_file(writable_path) """
      return(load_file(fname,self.get_writable_path(False,False)))
      
    def savefile(self, s, fname):
      """ shorthand for save_file() """
      save_file(s,fname,self.get_writable_path(False,False))
    
    # environment parameters
    def load_credentials(self):
       self.aws_credential_path=os.environ['AWS_CRED_PATH']
       self.aws_credentials=load_file(fname=self.aws_credential_path,as_json=True)
       return(self.aws_credentials)
       
    def set_environ_params(self, username ):
      """ docstring """
      self.load_credentials()
      self.aws_credential=self.get_credential(username)
      os.environ['AWS_ACCESS_KEY_ID']=self.aws_credential['AWS_ACCESS_KEY_ID']
      os.environ['AWS_SECRET_ACCESS_KEY']=self.aws_credential['AWS_SECRET_ACCESS_KEY']
      return()
      
    # subclasses
    def getServiceGenerator(self,**kwargs):
        return(AwsServiceGenerator(username=self.username,aws_credentials=self.aws_credentials))
    
""" utilities """
def get_response_items(client, function_name,kwargs={},items=None):
    """ execute client.function_name with kwargs, return DictList of items """
    #body
    if hasattr(client,function_name):
        client_func=getattr(client,function_name)
        if not callable(client_func):
            raise AWS_BASE_CLIENT_FUNCTION_ERROR(function_name)
    else:
        raise AWS_BASE_CLIENT_FUNCTION_ERROR(function_name)
    
    res=client_func(**kwargs)
    if dict(res):
        if items!=None and items in res:
            reslist=res[items]
        elif [ky for ky in res if type(res[ky])==list]!=[]:
            reslist=res[[ky for ky in res if type(res[ky])==list][0]]
        else:
            raise AWS_RESPONSE_LIST_ERROR(list(res.keys()))
    else:
        raise AWS_RESPONSE_LIST_ERROR('res is of type {0}'.format(type(res)))
    
    DictList0=DictList(reslist)
    #return value
    return(DictList0)

   
"""class exceptions, inherit from Exception"""
class AWS_CREDENTIAL_NOT_SET(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class AwsResponseError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class FUNCTION_CANNOT_BE_PAGINATED(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class BOTO3_VERSION_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class AWS_BASE_CLIENT_FUNCTION_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class AWS_RESPONSE_LIST_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class AWS_CREDENTIAL_PATH_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class AwsCredentialNotFound(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class AwsClassNotDefined(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        self.message=message
        self.extra='NOT in {}'.format(AWS_CLASS_MODULES)

    def __str__(self):
        return self.message + ': ' +self.extra

""" AWS service generator """        
USERDEFINEDSERVICES=['Lambda','S3'] 
       
class AwsServiceGenerator(Aws):
    """
    #class variables: same for all instances of class 
    """
    SERVICES=['Lambda','S3']
    
    """initialization"""
    def __init__(self,**kwargs):
        """ object to generate user defined service objects (eg Lambda),
            store in globals()['AWS']"""
        # set AWS in globals
        if not 'AWS' in globals():
           globals()['AWS']={}
        # flush existing objects
        self.__flush_globals__()
        super().__init__(**kwargs)
     
    def __iter__(self):
        # generator of iterable, eg (iterable)
        yield(self.SERVICES)
        
    def __len__(self):
        return(len(self.SERVICES))
        
      
    def __contains__(self,item):
        # rule on item returning True/False
        return(self.object_in_globals(item))
        
    """  """
    def object_in_globals(self,x):
        return(x in globals()['AWS'])
        
    """property setters"""
    
    
    """class functions"""
    def getService(self,service,initialize=False,**kwargs):
            """ initialize user defined service, set to globals() """
            #body
            x=service
            kwargs={'username':self.username,'environ_params':self.environ_params}
            if x=='Lambda':
                if x in self:
                    Service=self.__get_from_globals__(x)
                else:
                    from aws.Lambda import Lambda
                    Service=Lambda(self.username,self.environ_params,self.aws_credentials)
                    self.__set_in_globals__(x,Service)
            elif x.upper()=='S3':
                if x.upper() in self:
                    Service=self.__get_from_globals__(x)
                else:
                    from aws.S3 import S3
                    Service=S3(**kwargs)
                    self.__set_in_globals__(x.upper(),Service)
            else:
                raise AwsUserDefinedServiceNotExists(x)
            #return value
            return(Service)
    

        
    def __get_from_globals__(self,servicename):
        print('getting from service {} from globals()'.format(servicename))
        return(globals()['AWS'][servicename.upper()])
    
    def __set_in_globals__(self,servicename,Service):
        globals()['AWS'][servicename]=Service
        
    def __flush_globals__(self):
        keys=list(globals()['AWS'].keys())
        for ky in keys:
            print('flushing: {}'.format(ky))
            del globals()['AWS'][ky]
    
    
    """subclass generator functions"""

"""subclasses"""


"""class exceptions, inherit from Exception"""
class AwsUserDefinedServiceNotExists(Exception):
    def __init__(self, message=None, errors=None):
        message='choose any of {}'.format(','.join(USERDEFINEDSERVICES))
        super().__init__(message)
        self.errors = errors