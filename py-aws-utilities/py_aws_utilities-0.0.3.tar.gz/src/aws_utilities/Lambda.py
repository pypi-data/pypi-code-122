"""
changes: added Lambda.invoke(), added classes LambdaReponse, LambdaDeploymentPackage
Lambda:
    1. lambda utilities
    2. lambda management
    3. lambda deployment package management
    4. lambda layers
    5. build deploy promote pipeline
    6. other services: ApiGateway
    
TODO: list_aliases(function)
TODO: check if '0' is accepted as $LATEST version or not
TODO: invoke, raise_lambda_error (call check_error())
TODO: invoke, optionally raise error if the Payload response is empty (null bytes)
"""

import os, re, shutil, json, time as tm
from uuid import uuid4
from utilities.base import serialize_object, nvl, __copy__, first_value, from_kwargs
from utilities.dicts import jsonlist_subset, set_attributes, get_from_dict, sort_dict
from utilities.DictList import DictList
import utilities.filesystem as fs
from utilities.filesystem import find_first_path
from utilities.lists import flatten_list, to_list, unique
import utilities.lists as lists

# constants
MAX_TIMEOUT=900     
MIN_TIMEOUT=15   
DEFAULT_HANDLER_NAMES={'nodejs':'',
                      'nodejs4.3':'',
                      'nodejs6.10':'',
                      'nodejs8.10':'','nodejs10.x':'','nodejs12.x':'',
                      'python2.7':'$lambda_name.lambda_handler',
                      'python3.6':'$lambda_name.lambda_handler',
                      'python3.7':'$lambda_name.lambda_handler',
                      'python3.8':'$lambda_name.lambda_handler'}    

MAP_RUNTIME_LAYER_FOLDER={'python':'python','python3.6':'python','python3.8':'python','nodejs':'nodejs/node_modules'}
DEF_WAIT_UPDATE_CONFIG=1

# utility functions
def __format_version_number__(version):
   #body         
   return(re.sub('\\$LATEST','0', str(version)))
   
def __function_version__(v):
   #body         
   v = '$LATEST' if str(v)=='0' else str(v)
   return(v)  
 
# class LambdaFunction
class LambdaFunction:
   """ represents the lambda function """
   name='LambdaFunction'  
   # lambda invocation
   def invoke(self, InvocationType='RequestResponse', Payload={}, alias=None, version=None, return_json=False, raise_error=True, return_lambda_response=False):
       """ invoke calls Lambda.invoke """
       # body
       lambda_name= self.lambda_name #self.__validate_full_name__(alias, version)
       # check alias/version
       if alias !=None and version!=None:
          raise ValueError('choose either alias or version, not both')
       if alias != None and not alias in self.aliases:
          raise ALIAS_DOES_NOT_EXIST(alias)
       if version != None and not int(version) in self.version_numbers:
          raise VERSION_DOES_NOT_EXIST(version)
       # execute invoke function
       res = self.Lambda.invoke(lambda_name=lambda_name,InvocationType=InvocationType, 
                                Payload=Payload,alias=alias, version=version, 
                                return_json=return_json,raise_error=raise_error,
                                return_lambda_response=return_lambda_response)
       #return value
       return(res)

   def __validate_full_name__(self, alias=None, version=None):
       """ validate the full function name: function_name:stage/version"""
       #body
       if alias != None and not alias in self.aliases:
          raise ALIAS_DOES_NOT_EXIST(alias)
       if version != None and not int(version) in self.version_numbers:
          raise VERSION_DOES_NOT_EXIST(version)
       if alias !=None:
          function_name = self.lambda_name + ':' + alias
       elif version!=None:
          function_name = self.lambda_name + ':' + str(version)
       else:
          function_name=self.lambda_name
       #return value
       return(function_name)
 
   def force_new_container(self,delta_timeout=1,wait=None):
       """ make a minor config change to force new aws lambda instance """
       #body
       if self.Timeout >= MAX_TIMEOUT:
          delta_timeout=-1
       new_timeout = self.Timeout+delta_timeout
       kwargs={'FunctionName':self.function_name,'Timeout':new_timeout}
       tm.sleep(nvl(wait,DEF_WAIT_UPDATE_CONFIG))
       res=self.client.update_function_configuration(**kwargs)
       #return value
       return(res)    

   def set_alias_version(self, alias_name, version=None, latest=False, prv=False, nxt=False):
       """ set the LambdaFunction.alias version using: version, latest, prv or nxt """
       # check if alias exists
       if alias_name not in self.aliases:
          raise ALIAS_DOES_NOT_EXIST('alias doesnt exist: {0}'.format(alias_name))
       # get the current version number of the alias     
       current_version_number = int(__format_version_number__(self.map_alias_versions.get(alias_name)))
       self.version_numbers.sort()
       current_version_index=self.version_numbers.index(current_version_number)
       # logic to set version to latest, previous (prv) or next (nxt)
       if latest:
           if current_version_number == 0:
               print('alias already $LATEST version')
           version_number=0
       elif prv:
           version_number = self.version_numbers[current_version_index-1] if current_version_index>1 else current_version_number
       elif nxt:
           version_number = self.version_numbers[current_version_index+1] if current_version_number!=0 and current_version_index<len(self.version_numbers)-1 else 0
       elif version!=None:
           version_number = int(__format_version_number__(version))
           if version_number == current_version_number:
               print('alias already at version {0}'.format(version_number))
       else:
           raise ValueError('no parameter passed: version, latest, prv, nxt')
         
       # update the alias version and reset LF alias information or do nothing
       if current_version_number!=version_number:
           res = self.client.update_alias(FunctionName=self.lambda_name, Name=alias_name, FunctionVersion=__function_version__(version_number))
           self.Lambda.__set_LF_aliases__(self)
       else:
           print('new version number equal to current version number')
           res = {}
       # return value
       return(res)
    
# class Lambda
from aws.aws_base import Aws
class Lambda(Aws):
   """
   #class variables: same for all instances of class 
   """
   DEFAULT_LAMBDA_KWARGS={'lambda_deployment_path':'lambda-deployment-path',
                          'DEFAULT_LAMBDA_DEPLOYMENT_S3_BUCKET':'deck-lambda-deployment-s3-bucket',
                          'lambda_project_path':'lambda-project-path'}
   
   # lambda dependencies for packages
   DEPENDENCIES={'googleapis':[ 'oauth2client', 'cachetools', 'googleapiclient', 'httplib2','pyasn1','pyasn1_modules', 'rsa','uritemplate'],
                 'deck':['pydeck','utilities','db_utilities','MailChimp','aws'],
                 'docx':['lxml','docx'],
                 'bcrypt':['bcrypt','cffi','libffi-d78936b1.so.6.0.4','psycopg2', '_cffi_backend.cpython-36m-x86_64-linux-gnu.so'],
                 'Bcrypt':['bcrypt','cffi','libffi-d78936b1.so.6.0.4', '_cffi_backend.cpython-36m-x86_64-linux-gnu.so'],
                 'requests':['idna','chardet','urllib3','requests','certifi']}
   
   """initialization"""
   def __init__(self,username=None,environ_params=True,aws_credentials=None,lambda_deployment_path=None, lambda_project_path=None, 
                lambda_deployment_s3_bucket=None, lambda_arn_role=None):
      """ extends boto3.lambda service """
      environ_params=False if username!=None else environ_params
      super().__init__(username=username,environ_params=environ_params,aws_credentials=aws_credentials)
      
      # placeholders
      self.source_paths=None
      self.LambdaDeployment=None
      
      # options
      self.WAIT_UPDATE_CONFIG=DEF_WAIT_UPDATE_CONFIG
      
      # parameters: set LAMBDA_KWARGS for aws_credential or default
      self.LAMBDA_KWARGS=self.aws_credential.get('LAMBDA_KWARGS') if self.aws_credential.get('LAMBDA_KWARGS')!=None else self.LAMBDA_KWARGS
      # path/bucket references
      self.LAMBDA_DEPLOYMENT_PATH=find_first_path(lambda_deployment_path,self.LAMBDA_KWARGS.get('lambda_deployment_path'),self.DEFAULT_LAMBDA_KWARGS.get('lambda_deployment_path'))
      self.LAMBDA_PROJECT_PATH=find_first_path(lambda_project_path,self.LAMBDA_KWARGS.get('lambda_project_path'),self.DEFAULT_LAMBDA_KWARGS.get('lambda_project_path'))
      self.LAMBDA_SOURCE_PATH=find_first_path(self.LAMBDA_KWARGS.get('lambda-source-path'))
      
      # add warnings if paths are None
      import warnings
      if self.LAMBDA_DEPLOYMENT_PATH==None:
          warnings.warn('path variable {0} is None'.format('LAMBDA_DEPLOYMENT_PATH'))
      if self.LAMBDA_PROJECT_PATH==None:
          warnings.warn('path variable {0} is None'.format('LAMBDA_PROJECT_PATH'))
      if self.LAMBDA_SOURCE_PATH==None:
          warnings.warn('path variable {0} is None'.format('LAMBDA_SOURCE_PATH'))
                        
      self.LAMBDA_DEPENDENCY_PATHS=self.LAMBDA_KWARGS.get('lambda-dependency-paths',[])
      if self.LAMBDA_DEPENDENCY_PATHS==[]:
          warnings.warn('path variable {0} is []'.format('LAMBDA_DEPENDENCY_PATHS'))
      # add site-packages to dependency paths
      if 'PyLib' in self.LAMBDA_DEPENDENCY_PATHS:
          self.LAMBDA_DEPENDENCY_PATHS.append(os.path.join(os.getenv('PyLib'),'site-packages'))
                  
      self.LAMBDA_DEPLOYMENT_S3_BUCKET=nvl(lambda_deployment_s3_bucket,self.LAMBDA_KWARGS.get('lambda_deployment_s3_bucket',self.DEFAULT_LAMBDA_KWARGS.get('DEFAULT_LAMBDA_DEPLOYMENT_S3_BUCKET')))
      # ARN role for lambda execution
      self.arn_role=self.LAMBDA_KWARGS.get('lambda_arn_role',lambda_arn_role)
      # bind client
      self.client=self.get_client('lambda')  
      
      # flow: get lambda functions + lambda layers
      self.lambda_names=self.get_lambda_names()
      self.Layers=self.list_lambda_layers()
       
   """property setters"""
   
   """class functions"""
   # utilities
   def __paginator__(self,funcname,node, FunctionName=None):
       try:
            #body
            func=getattr(self.client, funcname)
            kwargs={}
            if FunctionName!=None:
                kwargs['FunctionName']=FunctionName
            kwargs['MaxItems']=self.MAXITEMS
            r=func(**kwargs)
            list0=[]
            nodelist=r[node]
            list0.append(nodelist)
            next_marker=''
            while next_marker != None:
                if 'NextMarker' in r:
                    kwargs['MaxItems']=self.MAXITEMS
                    kwargs['Marker']=r['NextMarker']
                    r=func(**kwargs)
                    nodelist=r[node]
                    list0.append(nodelist)
                else:
                    next_marker = None
            outputlist=flatten_list(list0) 
       except Exception as e:
          print('error in __paginator__')
          raise e
       #return value
       return(outputlist)
       
   def __function_version__(self, v):
       #body         
       v = '$LATEST' if v=='0' else str(v)
       return(v)  
       
   def get_lambda_names(self):
       """ gets all lambda names """
       # paginate list_functions
       self.functions=self.__paginator__('list_functions','Functions')
       self.lambda_names=[f['FunctionName'] for f in self.functions]
       self.lambda_names.sort()
       return(self.lambda_names)
     
   def list_lambdas(self):
       """ alias for get_lambda_names """
       return(self.get_lambda_names())
    
   # 1 LAMBDA FUNCTIONS
   def lambda_exists(self, lambda_name):
       v = lambda_name in self.list_lambdas()
       return(v)
   
   def get_lambda(self,lambda_name,alias=None,version=None):
       """ returns LambdaFunction instance """
       try:
          # body
          
          # initialize empty LambdaFunction object
          LF0=LambdaFunction()
          
          # flow: get lambda by name
          if lambda_name not in self.lambda_names:
              # not found: re-init lambda_names 
              self.lambda_names=self.get_lambda_names()              
          
          # set reference to lambda client
          LF0.client=self.client
          # set reference to Lambda object
          LF0.Lambda=self
          # paginate list versions
          versions_by_function=self.__paginator__('list_versions_by_function','Versions', lambda_name)


          # get lambda function as LambdaFunction object
          function=jsonlist_subset(self.functions, conditions={'FunctionName':lambda_name})
          if len(function)>0:
             LF0.lambda_function=function[0]
          else:
             raise LambdaDoesNotExist('{0}'.format(lambda_name))
             
          # set LambdaFunction properties
          LF0.lambda_name=lambda_name
          
          # from lambda function response
          function_attributes={}
          for ky in ['Description','Runtime','Handler','Timeout','LastModified','Version']:\
              function_attributes[ky.lower()]=LF0.lambda_function[ky]
          set_attributes(LF0,function_attributes)
          
          # lambda versions, aliases
          # version numbers and max version
          LF0.versions_by_function=versions_by_function
          version_numbers=[__format_version_number__(x['Version']) for x in versions_by_function] 
          version_numbers=[int(x) for x in version_numbers]
          
          # get max_version_number
          max_version_number=max(version_numbers)
          LF0.max_version=max_version_number
          LF0.version_numbers=version_numbers
          
          # get the Description of the last version if availible
          LF0.last_version=DictList(LF0.versions_by_function).subset({'Version':str(LF0.max_version)},index=0)
          LF0.last_description=LF0.last_version.get('Description') if LF0.last_version!=None else None
        
          # flow: set function aliases
          self.__set_LF_aliases__(LF0)

          # layers
          LF0.layers=LF0.lambda_function['Layers'] if 'Layers' in LF0.lambda_function else []
          LF0.layer_arns=[l['Arn'] for l in LF0.layers]
          LF0.layer_names=[re.findall('layer:(.*?):',LF0.layer_arns[i])[0] for i in range(0,len(LF0.layer_arns))]
          
          # set LF.fuction_name => aws full function name
          LF0.function_name=LF0.__validate_full_name__(alias,version)
          
          #  add functions: add_permission
          LF0.add_permission=lambda x,y,z: self.add_permission(lambda_name=LF0.lambda_name,source_arn=x,principal=y,alias=z)
          
       except Exception as e:
          print('error in get_lambda: {0}'.format(lambda_name))
          raise e
       #return value
       return(LF0)

   def __set_LF_aliases__(self,LF0):
       # utility function for setting alias attributes to the LF object         
       
       # paginated call to client function list_aliases
       LF0.aliases_by_function=self.__paginator__('list_aliases','Aliases',LF0.lambda_name)
       
       # set aliases (names), versions and mapping name, version
       LF0.aliases=[alias['Name'] for alias in LF0.aliases_by_function]
       LF0.alias_versions=[alias['FunctionVersion'] for alias in LF0.aliases_by_function]
       LF0.map_alias_versions=dict(zip(LF0.aliases,LF0.alias_versions))
       return()
   
   def get_records(self):
       try:
          #body
          lambda_records=[]
          for lambda_name in self.lambda_names:
              LF0=self.get_lambda(lambda_name)
              lambda_record=serialize_object(LF0,as_string=False)
              lambda_record['alias_with_version']=dict(zip(LF0.aliases,LF0.alias_versions))
              lambda_record=sort_dict(lambda_record,keys=['lambda_name','LastModified','max_version','aliases','alias_versions'])
              lambda_records.append(lambda_record)
       except Exception as e:
          print('error in get_records: {0}'.format(lambda_name))
          raise e
       #return value
       return(lambda_records)
                 
   # lambda management: deploy (create or update), delete
   def __get_default_handler_name__(self, lambda_function_name, runtime):
       try:
          #body
          if runtime in ['python2.7','python3.6','python3.7','python3.8']:
              #python:
              handler_name = lambda_function_name+'.'+'lambda_handler'
          elif runtime in ['nodejs','nodejs4.3','nodejs6.10','nodejs8.10','nodejs10.x','nodejs12.x']:
              #nodejs
              handler_name = 'index.handler'
          else:
              handler_name = lambda_function_name+'.'+'lambda_handler'
       except Exception as e:
          print('error in __get_default_handler_name__')
          raise e
       #return value
       return(handler_name)
   
   def __deploy__(self,fname, runtime, handler_name = None):
       """ returns parameters for deploy_aws_lambda """
       try:
          #body
          zipfilepath=os.path.join(self.LAMBDA_DEPLOYMENT_PATH,fname)
          #zipfilepath=os.environ['deck-lambda-deployment']+'/'+fname
          if not os.path.isfile(zipfilepath):
              raise LAMBDA_DEPLOYMENT_PKG_NOT_FOUND(zipfilepath)
          zpfile=open(zipfilepath,mode='rb').read()
          lambda_function_name=re.sub('\\.(py|zip)','',fname)
          if handler_name==None:
              # get default handler name conditional on runtime as handler name
              handler_name = self.__get_default_handler_name__(lambda_function_name, runtime)
          else:
              handler_name = re.sub('\\.(py|zip)','',handler_name)+'.'+'lambda_handler' # TODO NOT for NODEJS (!)
       except Exception as e:
          print('error in __deploy__')
          raise e
       #return value
       return({'zpfile':zpfile,
               'lambda_function_name':lambda_function_name,
               'handler_name':handler_name})

   def __validate_full_name__(self, lambda_name, alias=None, version=None):
       """ validate the full function name: function_name:stage/version"""
       try:
          #body
          if alias !=None:
              function_name = lambda_name + ':' + alias
          elif version!=None:
              function_name = lambda_name + ':' + str(version)
          else:
              function_name = lambda_name
       except Exception as e:
          print('error in __validate_full_name__')
          raise e
       #return value
       return(function_name)
       
   def deploy_aws_lambda(self, fname, timeout=30, runtime='python3.6', handler_name=None, print0=True, arn_role=None, update_config=True):
       try:
          #body
          # get parameters
          if self.environ_params:
              arn_role=first_value(arn_role,self.arn_role,os.getenv('ARN_ROLE'))
          else:
              arn_role=first_value(arn_role,self.arn_role)
          # raise error if arn_role is not set
          if arn_role == None:
              raise LAMBDA_ARN_ROLE_ERROR('deploy_aws_lambda: arn_role is None')
          
          # get deployment parameters
          params=self.__deploy__(fname, runtime, handler_name)
          lambda_function_name,zpfile,handler_name=from_kwargs(params,'lambda_function_name','zpfile','handler_name')
          # check if lambda_function_name in lambda_names
          lambda_exists=self.lambda_exists(lambda_function_name)
          # create or update lambda
          if lambda_exists==False:
              #create new lambda function 
              self.client.create_function(FunctionName=lambda_function_name,Runtime=runtime,Role=arn_role,Handler=handler_name,Timeout=timeout,Code={'ZipFile':zpfile})
              msg='new lambda function created in AWS: {0}'.format(lambda_function_name)
          else:
              # update existing lambda function
              self.client.update_function_code(FunctionName=lambda_function_name,ZipFile=zpfile)
              if update_config==True and handler_name != None:
                 tm.sleep(self.WAIT_UPDATE_CONFIG)
                 runtime=nvl(runtime,'provided')
                 self.client.update_function_configuration(FunctionName=lambda_function_name, Handler=handler_name, Runtime=runtime,Timeout=timeout)
              msg='lambda function updated in AWS: {0}'.format(lambda_function_name)
          
          if print0==True:
              print(msg)
       except Exception as e:
          print('error in deploy_aws_lambda')
          raise e
       #return value
       return(self)
       
   def delete_aws_lambda(self, lambda_function_name, print0=True):
       #body    
       #update
       self.client.delete_function(FunctionName=lambda_function_name)
       if print0==True:
          print('lambda function deleted in AWS: {0}'.format(lambda_function_name))
       #return value
       return(self)
        
   # 3 DEPLOYMENT: build, deploy packages
   def build_lambda_deployment(self, source_files, target_name, source_folder=None , dependencies=[], dependencies_folders=[], print0=True, subpath=None):
        """ package source_files into lambda deployment package target_name. optionally package dependencies (modules) """
        try:
            # body 
            # source 
            source_folder=nvl(source_folder,self.LAMBDA_SOURCE_PATH)
            if not os.path.exists(source_folder):
                raise FileNotFoundError('source_folder or LAMBDA_SOURCE_PATH does not exist:{}'.format(self.LAMBDA_DEPLOYMENT_PATH))
            # make target directory, optionally make subdirectory target/subpath
            if not os.path.exists(self.LAMBDA_DEPLOYMENT_PATH):
                raise FileNotFoundError('LAMBDA_DEPLOYMENT_PATH does not exist:{}'.format(self.LAMBDA_DEPLOYMENT_PATH))
            target_path=self.LAMBDA_DEPLOYMENT_PATH+'/'+re.sub('\\.(py|zip)','',target_name)
            fs.fs_mkdir(target_path,overwrite=True)
            if subpath!=None:
                subpath='/'+re.sub('^/','',subpath)
                fs.fs_mkdir(target_path+subpath,overwrite=True)
            
            #copy source_files to target directory, source file paths can be 1. qualified paths, or file names in paths in source_folder(s)
            source_files=lists.to_list(source_files)
            self.source_paths=[source_folder+'/'+s if not os.path.exists(s) else s for s in source_files]
            for i in range(0,len(source_files)):
                s=self.source_paths[i]
                d=target_path+'/'+source_files[i] if subpath == None else target_path+subpath+'/'+source_files[i]
                fs.fs_copy(s,d,overwrite=True)
            
            # copy dependencies from dependencies_folders to target
            self.lambda_dependency_paths=[find_first_path(p) for p in self.LAMBDA_DEPENDENCY_PATHS]
            all_dependencies_folders=lists.to_list(dependencies_folders)+self.lambda_dependency_paths

            # find dependency file in any all_dependencies_folders and copy to target
            dependencies=lists.to_list(dependencies)
            for fname in dependencies:
                s=fs.find_filepath(fname,paths=all_dependencies_folders)
                if s==None:
                    raise LAMBDA_DEPENDENCY_NOT_FOUND(fname)                
                d=target_path+'/'+fname if subpath == None else target_path+subpath+'/'+fname
                fs.fs_copy(s,d,overwrite=True)
                        
            # compress target to zip archive
            zipfilepath=os.path.join(self.LAMBDA_DEPLOYMENT_PATH,re.sub('\\.(py|zip)','',target_name))
            shutil.make_archive(zipfilepath, 'zip', target_path)
            
            if print0==True:
                print('lambda deployment package built: {0}.zip '.format(zipfilepath))
        except Exception as e:
            print('error in build_lambda_deployment')
            raise e
        return(self)

   # build and deploy using the LambdaDeploymentPackage
   def build_lambda_deployment_v2(self, target_name,  source_files=[], source_paths=None, dependencies=[], dependencies_folders=[], runtime='python', as_layer=False):
       self.LambdaDeployment=LambdaDeploymentPackage(self, target_name, source_files=source_files, source_paths=source_paths, dependencies=dependencies, dependencies_paths=dependencies_folders, runtime=runtime)
       if as_layer:
          # build a lambda layer deployment package
          self.LambdaDeployment.build_layer_pkg()
       else:
          # build a regular package
          self.LambdaDeployment.build_pkg()
       return(self)
   
   def getLambdaDeploymentPackage(self, target_name, source_files=[], source_paths=None , dependencies=[], dependencies_folders=[], runtime='python'):
       """ get the LambdaDeploymentPackage instance for packaging dependencies, source files into deployment package zipfiles """
       return(LambdaDeploymentPackage(self, target_name, source_files=source_files, source_paths=source_paths, dependencies=dependencies, dependencies_paths=dependencies_folders, runtime='python'))
   
   # list, get deployment pkgs     
   def list_deployment_pkgs(self):
       """ deployment packages (zipfiles) in LAMBDA_DEPLOYMENT_PATH"""
       self.pkgnames=[f for f in os.listdir(self.LAMBDA_DEPLOYMENT_PATH) if re.findall('\\.zip$',f)!=[]]
       return(self.pkgnames)

   def list_deployment_packages(self):
       """ more informative than list_deployment_pkgs """      
       return(self.list_deployment_pkgs())
       
   def get_deployment_pkg(self,pkgname):
       """ get deployment package content from pkgname (qualified zipfile name)"""
       try:
          #body
          pkgname=re.sub('\\.(py|zip)','',pkgname)+'.zip'
          if not pkgname in self.list_deployment_pkgs():
              raise FileNotFoundError('deployment package not found {0}'.format(pkgname))
          pkgcontent= open(self.LAMBDA_DEPLOYMENT_PATH+'/'+pkgname,mode='rb').read()
       except Exception as e:
          print('error in get_deployment_pkg')
          raise e
       #return value
       return(pkgcontent)

   def list_s3_deployment_pkg(self):
       """ list the lambda deployment packages (zip) in the lambda deployment s3 bucket """
       try:
          #body
          s3=self.get_client('s3')
          bucket_names=[d['Name'] for d in s3.list_buckets()['Buckets']]
          if not self.LAMBDA_DEPLOYMENT_S3_BUCKET in bucket_names:
            raise S3_BUCKET_NOT_FOUND(self.LAMBDA_DEPLOYMENT_S3_BUCKET)
          kwargs={'Bucket':self.LAMBDA_DEPLOYMENT_S3_BUCKET}
          list_objects_paginator=s3.get_paginator('list_objects').paginate(**kwargs)
          all_objects=[__copy__(obj['Contents']) for obj in list_objects_paginator]
          all_objects_list=[o['Key'] for o in lists.flatten_list(all_objects)]
       except Exception as e:
          print('error in list_s3_deployment_pkg')
          raise e
       #return value
       return(all_objects_list)
    
   def upload_deployment_pkg_to_s3(self,pkgname):
       """ upload lambda deployment package (zip) from lambda deployment package folder to lambda deployment s3 bucket """
       try:
          #body
          s3=Aws(username=self.username, environ_params=self.environ_params).get_client('s3')
          bytes0=self.get_deployment_pkg(pkgname)
          bucket_name=self.LAMBDA_DEPLOYMENT_S3_BUCKET
          r=s3.put_object(Bucket=bucket_name,Key=pkgname,Body=bytes0)      
       except Exception as e:
          print('error in upload_deployment_pkg_to_s3')
          raise e
       #return value
       return(r)
       
   # alias management
   def list_aliases(self,lambda_name):
       return(self.get_lambda(lambda_name).aliases)
       
   def create_alias(self,lambda_name, alias_name='prod', alias_dsc='production',version_number=None):
      #body
      LF0=self.get_lambda(lambda_name)  
      if alias_name in LF0.aliases:
          print('alias exists: {0}'.format(alias_name))
          response={}
      else:
          function_version=nvl(version_number,min(LF0.version_numbers))
          response = self.client.create_alias(
                            FunctionName=lambda_name,
                            Name=alias_name,
                            FunctionVersion=__function_version__(function_version),
                            Description=alias_dsc
          )
          print('alias created {0}:{1}'.format(lambda_name,alias_name))
      #return value
      return(response)
        
   def promote_lambda(self, lambda_name, alias_name='prod', version_dsc='',version_number=None):
       """ promote the lambda_name.alias to target version """
       try:
          #body
          LF0=self.get_lambda(lambda_name)
          
          # check if alias exists
          if alias_name not in LF0.aliases:
              raise ALIAS_DOES_NOT_EXIST('alias doesnt exist: {0}'.format(alias_name))
              
          # first publish...
          response = self.client.publish_version(FunctionName=lambda_name, Description=version_dsc)
          print('New version of lambda {0} published: {1}'.format(lambda_name, response['Version']))
          
          # ...then set alias prod to latest version
          LF0=self.get_lambda(lambda_name)
          version_number=nvl(version_number,LF0.max_version)
          response = self.client.update_alias(FunctionName=lambda_name, Name=alias_name, FunctionVersion=__function_version__(version_number))
          if response['FunctionVersion']==__function_version__(LF0.max_version):
              #msg='no change in code, alias {0}.{1} not updated'.format(lambda_name, alias_name)
              pass
          else:
              msg='alias updated {0}.{1} to version {2}'.format(lambda_name, alias_name, LF0.max_version)
          msg='alias updated {0}.{1} to version {2}'.format(lambda_name, alias_name, LF0.max_version)
          print(msg)   
       except Exception as e:
          print('error in promote_lambda')
          raise e
       #return value
       return(response)
       
   def promote_lambdas(self, lambda_names={}):
       """ promote lambdas using key-value {lambda_name : version_dsc} """
       #body
       for name in lambda_names:
           self.promote_lambda(name, alias_name='prod', version_dsc=lambda_names[name])
       #return value
       return(self)

   # invocation
   def invoke(self, lambda_name, Payload={}, InvocationType='RequestResponse', alias=None, version=None, return_json=False, raise_error=True, return_lambda_response=False):
       """ invokes the lambda """
       # format payload + get the full lambda_name
       if not lambda_name in self.lambda_names:
          if not lambda_name in self.list_lambdas():
             raise LambdaDoesNotExist('{0}'.format(lambda_name))
       payload=json.dumps(dict(Payload)) if isinstance(Payload,dict) else Payload
       function_name=self.__validate_full_name__(lambda_name, alias, version)
          
       # invoke lambda function from client
       res=self.client.invoke(**{'FunctionName':function_name,'InvocationType':InvocationType,'Payload':payload})
          
       # print FunctionError
       function_error=res.get('FunctionError')
       if function_error!=None:
          print('invocation of function {0}:{1} yields error: {2}'.format(lambda_name,res['ExecutedVersion'],res['FunctionError']))
          if raise_error:
             raise LAMBDA_EXECUTION_ERROR(function_error)
            
       # optional: return Payload as json or return Payload as LambdaResponse
       if InvocationType=='RequestResponse':
          if return_json:
             res=json.loads(res['Payload'].read().decode('utf-8'))
          elif return_lambda_response:
             res_json=json.loads(res['Payload'].read().decode('utf-8'))
             res=LambdaResponse(res_json, lambda_name=lambda_name)
             if raise_error:
                pass
                #res.check_error()
             
       #return value
       return(res)
       
   def add_permission(self,lambda_name,source_arn,principal,alias=None,action='lambda:InvokeFunction'):
        """ add permission to source_arn to invoke lambda function """
        #body         
        response = self.client.add_permission(
            FunctionName=lambda_name + ':'+alias if alias!=None else lambda_name,
            StatementId=str(uuid4()),
            Action=action,
            Principal=principal,
            SourceArn=source_arn
        )
        self.last_res=response
        return(self)

   # 4 Lambda layers
   def list_lambda_layers(self):
       #body
       self.Layers=DictList(self.client.list_layers()['Layers'])
       self.layer_names=self.Layers.query('LayerName')
       #return value
       return(self.Layers)

   def list_layer_names(self):
        return(self.list_lambda_layers().query('LayerName'))
        
   def layer_exists(self, layer_name):
       #body    
       return(layer_name in self.list_layer_names())
       
   def publish_layer_version(self, deployment_pkg_name, layer_name,layer_dsc='new layer', compatible_runtimes=['python3.6'], from_s3=False):
       try:
             #body
             msg= 'updating layer: {0}' if layer_name in self.layer_names else 'published new layer: {0}'
             msg= msg.format(layer_name)
             # from s3 or deployment package folder
             if from_s3:
                 if self.LAMBDA_DEPLOYMENT_S3_BUCKET==None:
                     raise S3_BUCKET_NOT_DEFINED(self.LAMBDA_DEPLOYMENT_S3_BUCKET)
                 pkg_source='bucket {0}'.format(self.LAMBDA_DEPLOYMENT_S3_BUCKET)
                 content={'S3Bucket': self.LAMBDA_DEPLOYMENT_S3_BUCKET,
                          'S3Key':deployment_pkg_name}
             else:
                 layer_content=self.get_deployment_pkg(deployment_pkg_name)
                 pkg_source=self.LAMBDA_DEPLOYMENT_PATH
                 content={'ZipFile': layer_content}
             # send request to AWS 
             response = self.client.publish_layer_version(
                        LayerName=layer_name,
                        Description=layer_dsc,
                        Content=content,
                        CompatibleRuntimes=compatible_runtimes,
                        LicenseInfo='string'
                        )
             if response['ResponseMetadata']['HTTPStatusCode']<=299:
                  print(msg)
             else:
                  print('failed to crete or update layer {0} from lambda package {1} in {2}'.format(layer_name,deployment_pkg_name,pkg_source))
       except Exception as e:
          print('error in publish_layer_version')
          raise e
       #return value
       return(response)

   def assign_layer_to_lambda(self,lambda_name,layer_names,layer_version_arn=None):
      #body
      # get layer version's arn
      layer_version_arns=[]
      for layer_name in lists.to_list(layer_names):
          if not layer_name in self.list_layer_names():
              raise LAYER_DOES_NOT_EXIST(layer_name)
          last_layer_version_arn=self.list_lambda_layers().subset({'LayerName':layer_name})[0]['LatestMatchingVersion']['LayerVersionArn']
          layer_version_arns.append(last_layer_version_arn)
      # add layer to function
      tm.sleep(self.WAIT_UPDATE_CONFIG)
      r=self.client.update_function_configuration(FunctionName=lambda_name,Layers=layer_version_arns)
      #return value
      return(r)

   # 5 lambda build-deploy-promote pipeline
   def build_deploy_promote(self,**kwargs):
       try:
          # body
          # build lambda deployment package
          lambda_name=kwargs.get('lambda_name','')
          lambda_dir=kwargs.get('lambda_dir',lambda_name)  
          # get lambda project path
          projpath = nvl(self.LAMBDA_PROJECT_PATH,'') + '/' + lambda_dir
          if not os.path.isdir(str(projpath)):
              raise LAMBDA_PROJECT_PATH_NOT_FOUND(projpath)          
          source_files=kwargs['source_files']
          dependencies=kwargs['dependencies']
          subpath=get_from_dict(kwargs,'subpath',None)  
          self.build_lambda_deployment(source_files, lambda_name+'.zip', source_folder=projpath, dependencies=dependencies, subpath=subpath)
          # deploy lambda
          timeout=get_from_dict(kwargs,'timeout',30)      
          runtime=get_from_dict(kwargs,'runtime','python3.6')   
          handler_name=get_from_dict(kwargs,'handler_name')   
          res=self.deploy_aws_lambda(lambda_name+'.zip', timeout=timeout, runtime=runtime, handler_name=handler_name)
          # optional: attach layers
          layer_names=get_from_dict(kwargs,'layer_names',[])
          if len(layer_names)>0:
              self.assign_layer_to_lambda(lambda_name,layer_names)
          # optional: promote lambda prod alias
          promote_lambda=get_from_dict(kwargs,'promote',False)
          version_dsc=get_from_dict(kwargs,'version_dsc','new version '+lambda_name)
          if promote_lambda:
              aliases_by_function=self.__paginator__('list_aliases','Aliases',lambda_name)
              if 'prod' not in aliases_by_function:
                  self.create_alias(lambda_name, alias_name='prod', alias_dsc='production') 
              self.promote_lambda(lambda_name,alias_name='prod',version_dsc=version_dsc)
       except Exception as e:
          print('error in build_deploy_promote')
          raise e
       #return value
       return(res)
   
   def get_lambda_deployment_template(self):
       try:
          #body
          template={'lambda_name':None,'lambda_dir':None,'source_files':[],'dependencies':[],'timeout':None,'runtime':None,'handler_name':None,'subpath':None,
                    'layer_names':[],'promote':False,
                    'version_dsc':None}
       except Exception as e:
          print('error in get_lambda_deployment_template')
          raise e
       #return value
       return(template) 
       
   def build_publish_lambda_layer(self, **kwargs):
       """ build (upload) and publish lambda layer from deployment specification:
           kwargs: layer_name,deployment_pkg_name,source_files,dependencies,layer_dsc, subpath, from_s3"""
       try:
          #body
          layer_name=kwargs['layer_name']
          deployment_pkg_name=kwargs.get('deployment_pkg_name',layer_name+'.zip')
          source_files=kwargs.get('source_files',[])
          dependencies=kwargs.get('dependencies',[])
          dependencies_folders=kwargs.get('dependencies_folders',[])
          compatible_runtimes=kwargs.get('compatible_runtimes',['python3.6'])
          runtime=kwargs.get('runtime','python')
          subpath=kwargs.get('subpath','python') # default to Python layer
          
          # deployment parameters
          deployment_function_version=kwargs.get('deployment_function_version','v2')
          from_s3=get_from_dict(kwargs,'from_s3',False)
          
          # layer publishing parameters
          layer_dsc=kwargs.get('layer_dsc','update layer')
          
          # set layer lambda project path
          projpath = nvl(self.LAMBDA_PROJECT_PATH,os.getcwd())
          if not os.path.isdir(str(projpath)):
              raise LAMBDA_PROJECT_PATH_NOT_FOUND(projpath)
              
          # build the layer
          if deployment_function_version=='v2':
             self.build_lambda_deployment_v2(layer_name, source_files=source_files, source_paths=projpath, dependencies=dependencies, dependencies_folders=dependencies_folders, runtime=runtime, as_layer=True)
          else:
             self.build_lambda_deployment(source_files, deployment_pkg_name, source_folder=projpath, dependencies=dependencies, subpath=subpath)
          
          # optional: upload layer deployment package zip file to s3
          if from_s3:
              self.upload_deployment_pkg_to_s3(deployment_pkg_name)
              
          # publish layer
          res=self.publish_layer_version(deployment_pkg_name,layer_name,layer_dsc=layer_dsc, compatible_runtimes=compatible_runtimes, from_s3=from_s3)
       except Exception as e:
          print('error in build_publish_lambda_layer')
          raise e
       #return value
       return(res)
       
   def get_lambda_layer_deployment_template(self):
       """ lambda layer deployment specification template """
       try:
          #body
          template={'layer_name':None,'source_files':[],'dependencies':[],'compatible_runtimes':['python3.6'],'subpath':'/python','deployment_pkg_name':None,'from_s3':False}
       except Exception as e:
          print('error in get_lambda_layer_deployment_template')
          raise e
       #return value
       return(template)   
 
   # 6 other services: APIGateway
   def getApiGateway(self):
       from aws.ApiGateway import ApiGateway
       return(ApiGateway(username=self.username))
       
   def getEvent(self , stage='staging', apiname='deckapi'):
       """ get the api gateway event """
       AG0=self.getApiGateway()
       Event=AG0.getEvent(apiname,stage=stage)
       return(Event)  
   
from utilities.filesystem import findpaths
from utilities.Directory import Directory

class LambdaDeploymentPackage(Directory):
    """
    helper class, LambdaDeploymentPackage: creates deployment package archive from source and dependency files
    deployment package types: regular or layer package
    """
    
    DEF_PRINT=True
    DEF_SOURCE_PATH=os.getcwd()
    
    """initialization"""
    def __init__(self, Lambda, target_name, source_files=[], source_paths=None, dependencies=[], runtime='python', dependencies_paths=[], **kwargs):
        
        super().__init__(path=Lambda.LAMBDA_DEPLOYMENT_PATH)
        self.LAMBDA_DEPLOYMENT_PATH=Lambda.LAMBDA_DEPLOYMENT_PATH
        self.target_name=target_name
        self.source_files=to_list(source_files)
        self.source_paths=to_list(nvl(source_paths, self.DEF_SOURCE_PATH)) # defaults to DEF_SOURCE_PATH
        
        self.DEPENDENCIES=Lambda.DEPENDENCIES
        self.LAMBDA_DEPENDENCY_PATHS=Lambda.LAMBDA_DEPENDENCY_PATHS+dependencies_paths # Lambda dependency paths + extra passed dependency paths
        self.dependencies=to_list(dependencies)
        self.__get_dependencies__()
        
        self.runtime=runtime
        
        # placeholders
        self.pkgpath=None
        self.zipfilepath=None
        
    
    """ utilities """           
    def __get_dependencies__(self):
      """ get dependencies as items in self.dependencies, if dependency is alias and in DEPENDENCIES mapping, get dependencies_list """
      # add dependencies from DEPENDENCIES: 
      DEPENDENCIES=self.DEPENDENCIES
      dependencies=self.dependencies
      
      dependency_aliases=[];alias_dependencies=[]
      for dep in dependencies:
         if dep in DEPENDENCIES:
            alias_dependencies+=DEPENDENCIES[dep]
            dependency_aliases+=[dep]
      
      # rm dependepency aliases
      for dep in dependency_aliases:
        dependencies.pop(dependencies.index(dep))
        
      # add alias_dependencies to dependencies
      for dep in alias_dependencies:
        dependencies.append(dep)
      
      # JKR 20200912: make dependencies unique
      dependencies=unique(dependencies)
      self.dependencies=dependencies
      
    """property setters"""
    
    
    """class functions"""
    def get_dependency_paths(self):
      """ get dependency_paths from dependencies and LAMBDA_DEPENDENCY_PATHS """
      self.map_dependencies={}
      if len(self.dependencies)>0:
         dependencies_paths=findpaths(self.LAMBDA_DEPENDENCY_PATHS)
         # map_dependencies
         for dep in self.dependencies:
              paths=[os.path.join(p,dep) for p in dependencies_paths]
              self.map_dependencies[dep]=[p for p in paths if os.path.isdir(p) or os.path.exists(p)]
              if len(self.map_dependencies[dep])==0:
                 raise LAMBDA_DEPENDENCY_NOT_FOUND(dep)
      else:
        pass
      dependency_paths=[self.map_dependencies.get(ky)[0] for ky in self.map_dependencies]
      
      return(dependency_paths)
   
    def get_sourcefile_paths(self ):
      """ get sourcefile_paths from source_files, source_path(s) """
      self.map_sourcefiles={}
      source_paths=findpaths(self.source_paths)
      for src in self.source_files:
         paths=[os.path.join(p,src) for p in source_paths]
         self.map_sourcefiles[src]=[p for p in paths if os.path.exists(p)]
         if len(self.map_sourcefiles[src])==0:
            raise FileNotFoundError('lambda source file: {0}'.format(src))
      
      sourcefile_paths=[self.map_sourcefiles.get(ky)[0] for ky in self.map_sourcefiles]
      
      return(sourcefile_paths)

    def make_deployment_pkg(self):
      """ make deployment package of current target """
      self.zipfilepath=os.path.join(self.LAMBDA_DEPLOYMENT_PATH,re.sub('\\.(py|zip)','',self.target_name))
      zipext='zip'
      shutil.make_archive(self.zipfilepath, zipext, self.pkgpath)
      self.pkgname=os.path.split(self.zipfilepath)[1]+'.'+zipext

      if self.PRINT==True:
         print('lambda deployment package built: {0}'.format(self.pkgname))
         
    def build_pkg(self):
      # create regular deployment package
      # get the package files
      sourcefile_paths=self.get_sourcefile_paths()
      dependency_paths=self.get_dependency_paths()
      
      # create the deployment package directory and put files
      target_name=self.target_name
      self.create_directory(target_name, overwrite=True).goto(target_name).put_files(dependency_paths+sourcefile_paths)
      self.pkgpath=self.path
      self.moveup()
      
      # make archive from package directory
      self.make_deployment_pkg()
      
    def build_layer_pkg(self):
      # create layer package, see #https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-path
      dependency_paths=self.get_dependency_paths()
      runtime_root=get_from_dict(MAP_RUNTIME_LAYER_FOLDER, self.runtime, exception_to_raise=LambdaRuntimeNotConfigured)
      
      # create the directory structure
      self.create_directory(self.target_name, overwrite=True).goto(self.target_name)
      self.create_directory(runtime_root, overwrite=True).goto(runtime_root).put_files(dependency_paths)
      self.pkgpath=self.moveup().path
      
      # make archive from package directory
      self.make_deployment_pkg()

from utilities.Dict2 import Dict2
class LambdaResponse():
    """helper class: maps lambda function response to object with response body as Dict2 instance """
    def __init__(self, res, lambda_name=None, raise_error=False):
        self.res=res
        self.lambda_name=lambda_name
        if isinstance(res,dict):
            self.body=Dict2(json.loads(res.get('body','{}')))
            self.statusCode=res.get('statusCode')
            self.headers=res.get('headers')
        else:
            print('response is not dict')
            self.body=None
            
        if raise_error:
            self.check_error()

    def check_error(self):
      """ checks if body.has_error """
      if isinstance(self.body,dict) and self.body.match({'has_error':True}):
          raise LambdaResponseError('lambda {0}, response {1}'.format(self.lambda_name,self.body))
      elif self.res in ['null']:
          raise LambdaResponseError('lambda {0}, response is null'.format(self.lambda_name))
            
"""class exceptions, inherit from Exception"""
class LambdaDoesNotExist(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class ALIAS_DOES_NOT_EXIST(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class VERSION_DOES_NOT_EXIST(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class LAYER_DOES_NOT_EXIST(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class LAMBDA_DEPENDENCY_NOT_FOUND(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class LAMBDA_DEPLOYMENT_PKG_NOT_FOUND(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class LAMBDA_PROJECT_PATH_NOT_FOUND(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class S3_BUCKET_NOT_DEFINED(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class S3_BUCKET_NOT_FOUND(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class LAMBDA_ARN_ROLE_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

class LAMBDA_EXECUTION_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

# not a runtime but functional error (res.has_error=True)
class LambdaResponseError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class LambdaRuntimeNotConfigured(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors