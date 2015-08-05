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



def get_next():
  i = 0
  while True:
    i += 1
    yield i
  
generator = get_next()
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))
print(next(generator))