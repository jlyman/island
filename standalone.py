#!/usr/bin/env python3

__doc__ = '''
  Script to run within Django from the command line.
'''

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'theCproject.settings'
import django
django.setup()

# imports
from lib.filters import *
from homepage import models as hmod
from forum import models as fmod

pwd = input('cca password: ')
pwd = pwd.strip()


iscore = fmod.Topic.objects.get(key='iscore')



# ldap
from ldap3 import Server, Connection, LDAPException, AUTH_SIMPLE, STRATEGY_SYNC, GET_ALL_INFO, SEARCH_SCOPE_WHOLE_SUBTREE
s = Server('ldap.byu.edu', port = 636, get_info = GET_ALL_INFO, use_ssl = True)
c = Connection(s, auto_bind = True, client_strategy = STRATEGY_SYNC, user="uid=cca, ou=people, o=byu.edu", password=pwd, authentication=AUTH_SIMPLE) 
for line in open('/Users/conan/Desktop/ryids.txt'):
  line = line.strip()
  if line.find('\t') > 0:
    ryid, email = line.split('\t')
  else:
    ryid, email = line, ''
  ryid = ryid.strip()
  email = email.strip()
  print(ryid)
  search_tree = c.search('uid=' + ryid +', ou=people, o=byu.edu','(objectClass=*)', SEARCH_SCOPE_WHOLE_SUBTREE, attributes=['cn', 'sn', 'preferredfirstname', 'permanentPhone', 'mail', 'employeeType'])
  user, created = hmod.SiteUser.objects.get_or_create(username=ryid)
  if len(c.response) > 0:
    attributes = c.response[0].get('attributes')
    user.first_name = attributes.get('preferredfirstname')[0] if attributes.get('preferredfirstname') else ''
    user.last_name = attributes.get('sn')[0] if attributes.get('sn') else ''
    user.fullname = attributes.get('cn')[0] if attributes.get('cn') else ''
    user.email = attributes.get('mail')[0] if attributes.get('mail') else ''
    user.phone = attributes.get('permanentPhone')[0] if attributes.get('permanentPhone') else ''
    user.BYU_status = ','.join(attributes.get('employeeType')) if attributes.get('employeeType') else ''
    user.save()  
  else:
    user.first_name = ''
    user.last_name = email
    user.fullname = ''
    user.email = email
    user.phone = ''
    user.BYU_status = ''
    user.save()

  print('\t', user.first_name, user.last_name, user.email)
    

  tn, created = fmod.TopicNotification.objects.get_or_create(user=user, topic=iscore)
  if not tn.notification:
    tn.notification = 'none'
    tn.save()      

