# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 16:14:45 2018

@author: jskro
python class AWSCloudwatchReporting , inherits from ApiRequestBuilder_v2.ApiRequestBuilder:
wrappers for AWS API reporting services

"""
import datetime as dt
from RequestBuilder.ApiRequestBuilder_v2 import ApiRequestBuilder
from utilities.dicts import json_query, json_expand
from utilities import lists
from aws.aws_base import Aws

class AWSCloudwatchReporting(ApiRequestBuilder):
   """
   #class variables: same for all instances of class 
   """
   template={'request_template': {
                     'Namespace':'AWS/Lambda',
                     'MetricName':'Invocations',
                     'StartTime':None,
                     'EndTime':None,
                     'Period':86400,
                     'Dimensions':[
                    {
                        'Name': 'FunctionName',
                        'Value':None
                    }
                    ],
                    'Statistics':[
                        'Sum', #|'Average'|'Sum'|'Minimum'|'Maximum',
                    ]
                    },
             'map_params_to_key':{
                    'statistics':'Statistics->0',
                    'Period':{'target':'Period','transform':int},
                    'startdate':'StartTime','enddate':'EndTime','lambda_name':'Dimensions->0->Value',
                    'metric':'MetricName',
                    'namespace':'Namespace'},
             'RETURN_ERROR': True,
             'output_transform': {'append':[],'format_names':True,'copy':{'startdate':'starttime','enddate':'endtime'},'append_input_parameters':['namespace','metric','lambda_name','Period','statistics','startdate','enddate']}
            } 
   """initialization"""
   def __init__(self):
      super().__init__(**self.template)
      # initialize Aws service client using environment parameters
      self.Aws=Aws(environ_params=True)
      self.client=self.Aws.get_client('cloudwatch')
      # set from api client: execution function and response parser
      self.execute_function=lambda x: self.client.get_metric_statistics(**x)
      self.response_parser=lambda x: json_query(x,'Datapoints')

class AWSCostExplorerReport(ApiRequestBuilder):
   """
   #class variables: same for all instances of class 
   """
   template = {'request_template':{
                    'TimePeriod':{
                        'Start': None,
                        'End': None
                    },
                    'Granularity':'DAILY',
                    'Metrics':None,
                    #'Filter':{
                    #        'Dimensions': {
                    #'Key': 'SERVICE',
                    #'Values': ['Amazon Relational Database Service', 'AWS Lambda']
                    #}
                    #}
                    'GroupBy':[
                        {
                            'Type': 'DIMENSION',
                            'Key': 'SERVICE'
                        },
                    ]
                   },
                  'map_params_to_key':{
                   'startdate':
                   {'target':'TimePeriod->Start','transform':lambda x: dt.datetime.strftime(x,'%Y-%m-%d')},
                   'enddate':
                   {'target':'TimePeriod->End','transform':lambda x: dt.datetime.strftime(x,'%Y-%m-%d')}
                   ,'Metrics':{'transform':lists.to_list},
                   'service':{'target':'Filter->Dimensions->Values','transform':lists.to_list}
                   },
                  'response_parser': lambda x: json_query(x,'ResultsByTime'), # lambda x: json_query(x,'ResultsByTime')
                  'output_parser': lambda x: lists.flatten_list([json_expand(r1,'Groups') for r1 in x])
                }
   """initialization"""
   def __init__(self):
       super().__init__(**self.template)
       # initialize Aws service client using environment parameters
       self.Aws=Aws(environ_params=True)
       self.client=self.Aws.get_client('ce')
       # set from api client: execution function
       self.execute_function=lambda x: self.client.get_cost_and_usage(**x)