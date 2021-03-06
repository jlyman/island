#!/usr/bin/env python3

__doc__ = '''
  Initializes tables with debugging data.
'''

# initializes django
import init_django
init_django.initialize()

# ensure we are in debug mode
from django.conf import settings
if not settings.DEBUG:
  raise Exception('Error: you can only run this script in a debugging environment.')


# imports
from lib.filters import *
from homepage import models as hmod
from forum import models as fmod
import random, datetime, sys

# add a few test users
for info in [
  ( 'user1', 'doconix@gmail.com', 'Conan2 Albrecht' ),
  ( 'user2', 'conan_albrecht@byu.edu', 'Conan3 Albrecht'),
]:
  user = hmod.SiteUser()
  user.username = info[0]
  user.email = info[1]
  user.fullname = info[2]
  user.save()

# ensure the main user (Conan or Thong) is a staff and superuser
user = hmod.SiteUser.objects.get(email='doconix@gmail.com')
user.is_staff = True
user.is_superuser = True
user.save()

# remove the topics and threads (careful!)
fmod.Comment.objects.all().delete()
fmod.Thread.objects.all().delete()
fmod.Topic.objects.all().delete()


SALE_STARTER = '''
<p>Item:</p>

<p>Price:</p>

<p>Description:</p>

<p>Contact Name:</p>

<p>Contact Number:</p>

<p>Contact Email:</p>
'''.strip()

JOBS_STARTER = '''
<p>Type: (part-time / consulting / full-time career)</p>

<p>Wage: (also specify whether hourly/salary/etc.)</p>

<p>Description:</p>

<p>Company:</p>

<p>Contact Name:</p>

<p>Contact Number:</p>

<p>Contact Email:</p>
'''.strip()


# add the topics
for i, (key, title, icon, starter) in enumerate([
  ( 'tech', 'Tech', 'icon_archive', '' ),
  ( 'nontech', 'Non-Tech', 'icon_bubble13', '' ),
  ( 'iscore', 'IS Core', 'icon_library2', '' ),
  ( 'help', 'Help',  'icon_support', '' ),
  ( 'sale', 'Sale', 'icon_tag7', SALE_STARTER ),
  ( 'jobs', 'Jobs', 'icon_coins', JOBS_STARTER ),
]):
  topic = fmod.Topic()
  topic.sort_order = i
  topic.key = key
  topic.title = title
  topic.icon = icon
  topic.starter = starter
  topic.save()

sys.exit(0)

# add new threads and comments
print('Adding new threads and comments.')
topic = fmod.Topic.objects.get(title='Tech')
now = datetime.datetime.now() - datetime.timedelta(days=5)
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