# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:19:03 2020

@author: J.S. Kroodsma
"""

from aws.aws_base import AWS_CLASS_MODULES

# get_persistent_objects
def get_persistent_objects(username,**kwargs):
    """ persistent client objects from package aws """
    #body
    import aws, importlib
    outargs=[]
    for awsclass,v in kwargs.items():
        if awsclass in AWS_CLASS_MODULES and v:
                if awsclass in globals():
                    class0=globals()[awsclass]
                    print('get {0} from globals()'.format(awsclass))
                else:
                    mod=importlib.import_module(awsclass,aws)
                    class0=getattr(mod,awsclass)
                    print('initialize {0}'.format(awsclass))
                    globals()[awsclass]=class0(username=username)
        else:
            raise AwsClassNotDefined(awsclass)
        outargs.append(class0)
    #return value
    return(tuple(outargs))

class AwsClassNotDefined(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        self.message=message
        self.extra='NOT in {}'.format(AWS_CLASS_MODULES)

    def __str__(self):
        return self.message + ': ' +self.extra
