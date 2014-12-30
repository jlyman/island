#!/usr/bin/env python3
import sys, os, os.path, glob, shutil
import subprocess, argparse
import getpass
import datetime


RSYNC_OPTIONS = [
  '-e "ssh"',
#  '--verbose',
  '--stats',
  '--delete',
  '--links',
  '--checksum',
  '--recursive',
  '--compress',
  '--perms',
  '--owner',
  '--group',
  '--times',
]


# set up the destination
DEST_USER = 'root'
DEST_HOST = 'island.byu.edu'
DEST_DIR = '/var/island/thecproject/'

# ensure the user really wants to do this
areyousure = input("Are you sure you are ready to upload to the live site? (y/n) ")

if areyousure.lower() != 'y':
  print('Canceled.')
  sys.exit(0)


# initialize django so we can use the settings and anything else
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'theCproject.settings')
import manage  # sets up the settings environment var
from django.conf import settings


######################################################################################################################
###   Function the settings file between debug and non-debug mode

def replace_in_file(filepath, old_st, new_st):
  contents = open(filepath, 'r').read()
  assert contents.find(old_st) >= 0, 'Could not find the %s line in settings.  Aborting.' % old_st
  f = open(filepath, 'w')
  f.write(contents.replace(old_st, new_st))
  f.close()
  


######################################################################################################################
###   Collect and minify the static files

print('Collecting and minifying static files...')
# delete the minified directory
if os.path.exists(settings.STATIC_ROOT):
  shutil.rmtree(settings.STATIC_ROOT)
# run the collect static command
os.system('python3 manage.py dmp_collectstatic')




#####################################################
###  Upload to the server

# erase the local template cache and *.pyc files
print('Removing temporary files...')
for cmd in [
  "find . -name 'cached_templates' -exec /bin/rm -rf {} \;",
  "find . -name '__pycache__' -exec /bin/rm -rf {} \;",
]:
  os.system(cmd)
 
# stop the web server
print("Stopping web server...")
os.system('''ssh %s@%s "/etc/init.d/nginx stop; /etc/init.d/uwsgi stop;"''' % (DEST_USER, DEST_HOST))

# switch the settings file to non-debug mode
settings_path = os.path.join(settings.BASE_DIR, 'theCproject', 'settings.py')
replace_in_file(settings_path, 'DEBUG = True', 'DEBUG = False')

# copy over everything
print('Comparing and copying files to the server...')
cmd = 'rsync %s %s %s@%s:%s' % (' '.join(RSYNC_OPTIONS), os.path.join(settings.BASE_DIR, '*'), DEST_USER, DEST_HOST, DEST_DIR)
print(cmd)
os.system(cmd)

# switch settings back to debug mode
replace_in_file(settings_path, 'DEBUG = False', 'DEBUG = True')

# erase the *.pyc files and template_cache so python/Mako recompiles everything on the web site
print('Emptying the dev server caches...')
rmcmds = [ 'rm -rf %s;' % os.path.join(DEST_DIR, appname, 'cached_templates') for appname in settings.CUSTOM_APPS ]
os.system('''ssh %s@%s "%s"''' % (DEST_USER, DEST_HOST, ' '.join(rmcmds)))
os.system('''ssh %s@%s "find %s -name '*.pyc' -exec rm -rf {} \;"''' % (DEST_USER, DEST_HOST, DEST_DIR))

# change user permissions
print('Settings permissions...')
os.system('''ssh %s@%s "chown -R www-data:www-data %s;"''' % (DEST_USER, DEST_HOST, DEST_DIR))

# reboot the web server
print("Restarting web server")
os.system('''ssh %s@%s "cd %s; /etc/init.d/uwsgi restart; /etc/init.d/nginx restart;"''' % (DEST_USER, DEST_HOST, DEST_DIR))


