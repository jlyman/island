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
import random

# main code
user = mmod.SiteUser.objects.get(email='ca@byu.edu')
topic = fmod.Topic.objects.get(pk=1)

# clear out the tables for debugging - careful!
print('Clearing old data.')
fmod.Comment.objects.all().delete()
fmod.Thread.objects.all().delete()

# add new threads and comments
print('Adding new threads and comments.')
for thread_i in range(1, 50):
  thread = fmod.Thread(user=user, topic=topic, title='Thread %s' % thread_i)
  thread.save()
  for comment_i in range(1, random.randint(2, 20)):
    comment = fmod.Comment(user=user, thread=thread, comment='Comment %s' % comment_i)
    comment.save()