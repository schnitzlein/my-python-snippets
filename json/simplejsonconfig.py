# SimpleJsonConfig
# TODO: add crypto
from sys import version_info
import urllib3
#import ssl
import getpass
import json


class SimpleJsonConfig():
   # class vars
   username = None
   password = None
   srv = None
   
   #
   # constructor
   #
   def __init__(self,  foobar1="bazzzz", cred={}):
      self.__foobar1 = foobar1
      self.cred = cred
      #self.connect()
      

   def connection_info(self):
      if self.srv:
         return self.srv.client_info()

   #
   # simpleJSON Reader
   #
   def readConfig(self):
      data = json.load(open('config.json'))

      if version_info >= (3, 0):
         self.username = data['username']
         self.password = data['password']
      else:
         self.username = data['username'].encode('ascii')
         self.password = data['password'].encode('ascii')