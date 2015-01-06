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

