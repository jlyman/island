from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser     
from django.http import HttpResponse, HttpResponseRedirect, Http404
from lib.filters import *

#####################################################################
###   User models

class Level(models.Model):
  name = models.TextField(blank=False, null=False)
  description = models.TextField(blank=True, null=True)
  points_required = models.IntegerField(max_length=200, blank=False, null=False)

  def __str__(self):
    return '%s: %s' % (self.id, self.name)


class UserType(models.Model):
  name = models.TextField(blank=True, null=True)
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return '%s: %s' % (self.id, self.name)


class SiteUser(AbstractUser):
  level = models.ForeignKey(Level, blank=True, null=True)
  user_type = models.ForeignKey(UserType, blank=True, null=True)
  fullname = models.TextField(blank=True, null=True)
  phone = models.TextField(blank=True, null=True)
  byu_status = models.TextField(blank=True, null=True)
  total_points = models.IntegerField(max_length=200, blank=True, null=True, default=0)

  def __str__(self):
    return '%s: %s' % (self.id, self.fullname)


  def get_full_name(self):
    if self.first_name and self.last_name:
      return '%s %s' % (self.first_name, self.last_name)
    return self.fullname

    
######################################################################
###   Tasks    

class Task(models.Model):
  user_type = models.ForeignKey(UserType)
  name = models.TextField(blank=True, null=True)
  expected_time = models.TextField(blank=True, null=True)
  url = models.TextField(blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  image = models.TextField(blank=True, null=True)
  importance = models.IntegerField(max_length=200, blank=True, null=True)
  points = models.IntegerField(max_length=200, blank=True, null=True)
  repeatable = models.NullBooleanField()

  def __str__(self):
    return '%s: %s' % (self.id, self.name)


class TaskStep(models.Model):
  task = models.ForeignKey(Task)
  sort_order = models.IntegerField(max_length=200, blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  def __str__(self):
    return '%s: %s, step %s' % (self.id, self.name, self.sort_order)


class TaskTicket(models.Model):
  user = models.ForeignKey(SiteUser)
  task = models.ForeignKey(Task)
  start_time = models.DateTimeField(auto_now_add=True)
  end_time = models.DateTimeField(blank=True, null=True)
  rating = models.IntegerField(max_length=200, blank=True, null=True)
  comment = models.TextField(blank=True, null=True)
  points = models.IntegerField(max_length=200, blank=True, null=True)

  def __str__(self):
    return '%s: %s' % (self.id)




#####################################################################
###   File Uploads

class UploadedFile(models.Model):
  '''A file stored in the DB. We are storing files directly in the database because it's much simpler
     (conceptually) that way.  This is not a high-traffic site, and it doesn't need the higher throughput of
     storing the files on the filesystem.  Very few comments have files attached, so we're doing what most would 
     say is a bad idea. :)  We can always switch it in the future if it becomes an issue.'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  filename = models.TextField(blank=True, null=True)
  contenttype = models.TextField(blank=True, null=True)
  size = models.IntegerField()
  filebytes = models.BinaryField(blank=True, null=True)
  
  def __str__(self):
    return 'DatabaseFile: %s (%s), %s bytes' % (self.filename, self.contenttype, self.size)

  def get_response(self, attachment=True):
    '''Returns an HttpResponse that downloads this file.'''   
    response = HttpResponse(content_type=self.contenttype)
    if attachment:
      response['Content-Disposition'] = 'attachment; filename="%s"' % url_escape(self.filename)
    response.write(self.filebytes)
    return response
 