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
from management import models as mmod
from forum import models as fmod
import random, datetime

# main code
user = mmod.SiteUser.objects.get(email='ca@byu.edu')
topic = fmod.Topic.objects.get(pk=1)

# clear out the tables for debugging - careful!
print('Clearing old data.')
fmod.Comment.objects.all().delete()
fmod.Thread.objects.all().delete()

now = datetime.datetime.now() - datetime.timedelta(days=5)

# add new threads and comments
print('Adding new threads and comments.')
for thread_i in range(1, 50):
  thread = fmod.Thread(user=user, topic=topic, title='Thread %s' % thread_i)
  thread.save()
  thread.created = now
  thread.save()
  for comment_i in range(1, random.randint(2, 20)):
    comment = fmod.Comment(user=user, thread=thread, comment='Comment %s. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' % comment_i)
    comment.save()
    comment.created = now
    comment.save()
    
    now += datetime.timedelta(minutes=random.randint(1, 10))