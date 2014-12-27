#!/usr/bin/env python3

import os, os.path, sys

###   This script is imported into many of the scripts in this directory. 
###   It initializes django and makes the script appear as if it were in the 
###   root project directory.  By chdir'ing to the project root, we can 
###   keep these scripts in a subdirectory and keep the root dir cleaner.

def initialize():
  '''Initializes the django system for a command-line script'''  
  # add the myeducator project root to the system path
  rootdir = os.path.dirname(os.path.abspath(__file__))
  while not os.path.exists(os.path.join(rootdir, 'manage.py')):  
    rootdir = os.path.dirname(rootdir)
    if rootdir == '/':
      print('Could not find project directory.  Aborting.')
      sys.exit(1)
  sys.path.insert(0, rootdir)
  
  # change to the root project dir so the script appears to be running there
  os.chdir(rootdir)

  # initialize the django environment
  os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
  import django
  django.setup()
  
  # return the project root, if the calling script needs it
  return rootdir



