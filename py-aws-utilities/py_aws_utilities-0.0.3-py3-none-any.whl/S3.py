# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 16:14:45 2018

@author: jskro
python class s3 , inherits from Aws:
classes: S3, s3Bucket, s3BucketDirectory
20201024: renamed to S3 to prevent confusion with boto3.s3
"""
import os, re, json
from aws.aws_base import Aws
from utilities.base import __copy__, nvl
import utilities.lists as lists
from utilities.DictList import DictList
from utilities.filesystem import get_ext

# CONSTANTS
S3_PATH_SEPERATOR='/'
AWS_SERVICE_NAME='s3'

#from boto3.resources.factory.s3.ServiceResource import Bucket
class S3(Aws):
   """
   #class variables: same for all instances of class 
   """

   """initialization"""
   def __init__(self, username=None, environ_params=True):
      if username!=None:
          environ_params=False
      super().__init__(username=username, environ_params=environ_params)
      self.client=self.get_client(service_name=AWS_SERVICE_NAME)
      # initialize BucketList
      self.getBucketList()
      self.bucket_names=self.get_bucket_names()
   
   """property setters"""

   
   """class functions"""
   def getBucketList(self, **kwargs):
      """ docstring """
      self.BucketList = DictList(self.client.list_buckets()['Buckets'])
      #return value
      return(self.BucketList)
   
   # subsetting methods 
   def get_bucket_names(self):
      #body         
      v=self.getBucketList().query('Name')
      self.bucket_names=v
      return(v)

   def list_buckets(self):
      return(self.get_bucket_names())
       
   def bucketnames(self):
      #body         
      return(self.getBucketList().query('Name'))
      
   def bucket_exist(self, bucket_name):
      #body         
      return(bucket_name in self.list_buckets())
   
   # factory methods
   def create_bucket(self,bucket_name,raise_error=True):
       #body         
        if bucket_name not in self.get_bucket_names():
            location = {'LocationConstraint': self.aws_region}
            res=self.client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
            self.raise_aws_response_error(res)
        elif raise_error:
            raise KeyError('bucket {0} exists'.format(bucket_name))
        else:
            print('bucket {0} exists'.format(bucket_name))
        return(self)
        
   def delete_bucket(self, bucket_name, deletekeys=False):
      #body    
      if deletekeys:
          s3Bucket0=self.getBucket(bucket_name)
          for ky in s3Bucket0.bucketkeys():
              s3Bucket0.deletekey(key=ky)
      res = self.client.delete_bucket(Bucket=bucket_name)      
      self.raise_aws_response_error(res)
      return(res)
   
   def getBucket(self,bucket_name):
       return(s3Bucket(bucket_name,self.client))

from utilities.filesystem import load_file,save_file,remove, find_path
class s3Bucket():
   """
   #class variables: same for all instances of class 
   """

   """initialization"""
   def __init__(self, bucket_name, s3):
        # attach client/s3
        self.client=s3
        self.s3=s3
        
        self.bucket_name=bucket_name
        self.name=bucket_name
        # get single bucket objects
        # get bucket object list
        self.getBucketObjectList()
        # get the bucket directories
        self.bucket_directories=self.get_bucket_directories()
        
   def __iter__(self):
       bucketkeys=self.getBucketObjectList().query('Key')
       yield(bucketkeys)

   def getBucketObjectList(self):
        """ each bucketobject item has a directory, top level directory and (optionally) a subdirectory """
        try:
            #body
            kwargs={'Bucket':self.bucket_name}
            list_objects_paginator=self.client.get_paginator('list_objects').paginate(**kwargs)
            # add response as last response:
            self.last_res=list_objects_paginator   
            all_objects=[__copy__(obj['Contents']) for obj in list_objects_paginator if 'Contents' in obj]
            self.BucketObjectList=DictList(all_objects)
            # add the object's directory to the list item
            dirs=[o['Key'].split(S3_PATH_SEPERATOR)[0] for o in self.BucketObjectList]
            
            for i,o in enumerate(self.BucketObjectList):
                o['Dir']=dirs[i]
                o['DirToplevel']=dirs[i].split('/')[0]
            
                # get the object subpath
                dirname=re.sub('/$','',o['Dir'])+'/'
                dirparts=re.sub(dirname,'',o['Key']).split(S3_PATH_SEPERATOR)
                # last part has no extension
                lastpart=dirparts[-1]
                if get_ext(lastpart)=='':
                   subdir=S3_PATH_SEPERATOR.join(dirparts)
                else:
                   subdir=S3_PATH_SEPERATOR.join(dirparts[:len(dirparts)-1])
                o['subDir']=subdir
               
            # list of bucket object directories
            self.dirs=dirs
        except Exception as e:
            print('error in getBucketObjects')
            raise e
        #return value
        return(self.BucketObjectList)
 
   # CRUD on bucket objects
   def list_bucket_objects(self):
      #body         
      return(self.getBucketObjectList().query('Key'))

   def list_objects(self):
      """ better name for list_bucket_objects """         
      return(self.getBucketObjectList().query('Key'))

   # s3Bucket getters: bucketkeys, get_object_body
   def bucketkeys(self):
       #body         
       self.bucket_keys=self.getBucketObjectList().query('Key')
       return(self.bucket_keys)
    
   def get_object(self,key):
       self.last_res=self.client.get_object(Bucket=self.name,Key=key)
       return(self.last_res)
       
   def getobjectbody(self,key,asjson=False):
       #body         
       res=self.client.get_object(Bucket=self.name,Key=key)
       self.last_res=res 
       res_string=res['Body'].read()
       if asjson:
           res=json.loads(res_string)
       else:
           res=res_string
       return(res)
       
   def deletekey(self,key):
       if key in self.bucketkeys():
           self.s3.delete_object(**{'Bucket':self.name, 'Key':key})

   # bucket methods
   def generate_presigned_url(self, key, expiry=3600):
      """ shorthand for s3.generate_presigned_url """
      url=self.client.generate_presigned_url('get_object', {'Bucket':self.name,'Key':key}, ExpiresIn=expiry)
      return(url)
      
   # file management: download, upload
   # TODO: allow for bucket "directory" upload/download. eg with key dirname/filename
   def upload(self, fname, dir0=None, key=None):
      """ upload file dir/fname as bucket.key """
      fpath=find_path(fname,dir0=dir0)
      key=nvl(key,fname)
      self.s3.upload_file(fpath,self.name,Key=key)
     
   def download(self, key, dir0=None, fname=None):
      """ docstring """
      dir0=nvl(dir0,os.getcwd())
      fname=nvl(fname,key).split(S3_PATH_SEPERATOR)[0] # if fname is key then take last part
      fpath=os.path.join(dir0,fname) # construct local path
      self.s3.download_file(self.name,key,fpath)

   def download_files(self):
      #body
      pass
      #return value
      return()

   # bucketdirectories
   def get_bucket_directories(self):
       # body         
       # add list of directories and subdirectories: bucket_directories
       self.getBucketObjectList()
       self.bucket_directories=lists.unique([d.split('/')[0] for d in self.dirs])
       return(self.bucket_directories)
      
   def create_dir(self,dir_name):
        """ create s3/directory """
        #body
        dir_name=re.sub('/$','',dir_name)+'/'
        self.last_res=self.client.put_object(Bucket=self.bucket_name, Key=(dir_name))
        if self.last_res['ResponseMetadata']['HTTPStatusCode']<=299:
            print('directory created {0}/{1}'.format(self.bucket_name,dir_name))
        #return value
        return(self)
        
   def delete_dir(self,dir_name):
        """ delete s3/directory """
        #body
        dir_name=re.sub('/$','',dir_name)+'/'
        self.last_res = self.client.delete_object(
            Bucket=self.bucket_name,
            Key=dir_name
        )
        if self.last_res['ResponseMetadata']['HTTPStatusCode']<=299:
            print('directory deleted {0}/{1}'.format(self.bucket_name,dir_name))
        #return value
        return(self)
           
   def getBucketDirectories(self):
       """ generate map of S3BucketDirectory instances, grouped by the top level directory (DirTopLevel) """
       #body     
       self.BucketDirs=self.BucketObjectList.group_by_key('DirToplevel')
       BucketDirectories={}
       for ky in self.BucketDirs:
           s3Directory=s3BucketDirectory(ky,self.BucketDirs[ky],self.client)
           BucketDirectories[ky]=s3Directory
           s3Directory.bucketname=self.bucket_name
       return(BucketDirectories)
   
class s3BucketDirectory():
    """
    #class variables: same for all instances of class 
    """
    """initialization: from BucketDirectory list"""
    def __init__(self,dirname,directory_content,client):
        self.client=client
        self.dirname=re.sub('/$','',dirname)+'/'
        self.directory_content=directory_content
        # set bucket directory object names
        objnames=[re.sub(self.dirname,'',f['Key']) for f in directory_content]
        objnames=[o for o in objnames if o!=''] # remove the empty object (is root)
        self.objnames=objnames
                        
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
    def list_objects(self):
        """ return names of objects in bucket\dirname """
        return(self.objnames)   
        
    def upload(self,fname,obj_name=None):
        """ docstring """
        #body
        if obj_name!=None:
            obj_name=lists.last_itm(fname.split('/'))   
        objkey=self.dirname+obj_name
        res=self.client.upload_file(fname, self.bucketname, objkey)
        #return value
        return(res)
        
    def download(self,objname,fname=None,path=None):
        """ download files from bucket\dirname """
        #body
        objkey=self.dirname+objname
        path=nvl(path,os.getcwd())
        if fname==None:
            fname=os.path.join(path,objname)  
        res=self.client.download_file(self.bucketname, objkey, fname)
        #return value
        return(res)
        
    def put(self,**kwargs):
        """ docstring """
        #body
        pass
        #return value
        return()


        
"""class exceptions, inherit from Exception"""



