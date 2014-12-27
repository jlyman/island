#!/usr/bin/env python3

__doc__ = '''
  Initializes tables with debugging data.
'''

# initializes django
import init_django
init_django.initialize()


# imports
from lib.filters import *
from management import models as mmod
from forum import models as fmod
import random, datetime

# ensure the user is a staff and superuser
user = mmod.SiteUser.objects.get(mail='ca@byu.edu')
user.is_staff = True
user.is_superuser = True
user.save()

# add the topics
for i, (title, icon) in enumerate([
  ( 'Tech', 'icon_archive' ),
  ( 'Non-Tech', 'icon_bubble13' ),
  ( 'IS Core', 'icon_library2' ),
  ( 'Help',  'icon_support' ),
  ( 'Sale', 'icon_tag7' ),
  ( 'Jobs', 'icon_coins' ),
]):
  topic = fmod.Topic()
  topic.sort_order = i
  topic.title = title
  topic.icon = icon
  topic.save()

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