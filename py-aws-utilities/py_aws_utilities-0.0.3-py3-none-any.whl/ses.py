# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:50:51 2019

@author: jskro
"""
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from utilities.base import __copy__,nvl
from utilities.dicts import get_from_dict
from utilities.lists import last_itm

from utilities.webhtml import build_html_table

class Email():
   """
   helper class representing Email message. Python object is email.mime.multipart.MIMEMultipart
   
   """
   MAIL_TEMPLATE = {'subject':None,'sender':None,'recipients':['recipient1'],'body':None}
   DEFAULT_SUBJECT=''
   
   """initialization"""
   def __init__(self, template=None, boundary=None):
      # message
      self.msg = MIMEMultipart(boundary=boundary)
      if template!=None:
          self.load(template)
      
   """property setters"""


   """class functions"""
   def get_template(self):
       #body         
       v=__copy__(self.MAIL_TEMPLATE)
       return(v)
       
   def load(self, template):
       try:
          # body
          self.template=template
          # the header
          self.msg['Subject'] = get_from_dict(template,'subject',self.DEFAULT_SUBJECT)
          self.msg['From'] = template['sender']
          self.msg['To'] = template['recipients'][0]
          # append the email body
          if 'body' in template:
              self.append_text(template['body'])
       except Exception as e:
          print('error in load')
          raise e
       #return value
       return(self)

   # attach (append) media to Email message: Text, html/text
   def append_text(self,s, subtype='plain'):
       try:
          #body
          self.msg.attach(MIMEText( s,subtype))
       except Exception as e:
          print('error in append_text')
          raise e
       #return value
       return(self)
       
   def append_html(self,html):
       self.append_text(html,'html')
       return(self)

   def append_html_table(self,data):
       try:
          #body
          html=build_html_table(data)
          self.append_text(html,'html')
       except Exception as e:
          print('error in append_html_table')
          raise e
       #return value
       return(self)
       
   # attach file to email         
   def add_attachment(self,fname,path=None):
       """ add a file as attachment to message """
       try:
          #body
          if os.path.exists(fname):
              attachment_file_path=fname 
              attachment_fname=last_itm(fname.split('/'))
          else:
              attachment_path=nvl(path,os.getcwd())
              attachment_fname=fname
              attachment_file_path=attachment_path+'/'+attachment_fname
          part = MIMEApplication(open(attachment_file_path, 'r').read())
          part.add_header('Content-Disposition', 'attachment', filename=attachment_fname)
          self.msg.attach(part)
       except Exception as e:
          print('error in add_attachment')
          raise e
       #return value
       return(self)

   def add_attachments(self,file_paths):
       #body         
       for fpath in file_paths:
           self.add_attachments(fname=fpath)
       return(self)
   
   # send the email using the (aws ses) mail client
   def send_email(self, mail_client):
       """ send msg as RawMessage using mail_client """
       try:
          #body
          msg=self.msg
          template=self.template
          recipients=template['recipients']
          RawMessage={
            'Data': msg.as_string()
          }
          r=mail_client.send_raw_email(RawMessage=RawMessage
          , Source=msg['From']
          , Destinations=recipients)
          print('email send to {0}'.format(recipients))
       except Exception as e:
          print('error in send_email')
          raise e
       #return value
       return(r)
       
"""class exceptions, inherit from Exception"""