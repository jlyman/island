from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser     
from django.http import HttpResponse, HttpResponseRedirect, Http404
from lib.filters import *
from jsonfield import JSONField
from homepage import models as hmod
import hashlib

######################################################################
###   Threads and comments - this is kept simple on purpose.
###   Threads are top-level items, comments are single level items on threads (no comments on comments).
###   The number of topics should be kept short.

class Topic(models.Model):
  '''Top-level topic.  We only want a few of these.  They are not created by users.  We want to force
     users to put their threads into only a few topics or it gets too combersome for users to select
     the topics they want filtered.'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  sort_order = models.IntegerField(blank=True, null=True)
  title = models.TextField(blank=True, null=True)
  key = models.TextField(blank=True, null=True)   # a shortened version of the title (without spaces, uppercase, etc.)
  icon = models.TextField(blank=True, null=True)
  starter = models.TextField(blank=True, null=True)  # used when creating new threads
  
  def __str__(self):
    return '%s: %s' % (self.id, self.title)
    
    

NOTIFICATION_CHOICES = (
  ( 'none',        'No Email' ),
  ( 'immediate',   'Immediate Email' ),
  ( 'daily',       'Daily Batch Email' ),
  ( 'weekly',      'Weekly Batch Email' ),
)    

class TopicNotification(models.Model):
  '''Contains how a user is notified when a new comment is posted to a topic.  If an object doesn't exist, it means the user is subscribed for all content.'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(hmod.SiteUser)
  topic = models.ForeignKey(Topic)
  notification = models.TextField(blank=True, null=True, default=NOTIFICATION_CHOICES[1][0])  # defaults to immediate
  
  class Meta:
    unique_together = (
      ( 'user', 'topic' ),  # prevents more than one of these records ever occuring
    )

  
    
class Thread(models.Model):    
  '''A discussion thread within a topic'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(hmod.SiteUser)
  topic = models.ForeignKey(Topic)
  title = models.TextField(blank=True, null=True) 
  options = JSONField(blank=True, null=True)             # Artibrary options - these will never be queryable, but it 
                                                         # keeps us from constantly changing the database just to store a new option.
                                                         # See set_option and get_option below.
  
  def __str__(self):
    return '%s: %s' % (self.id, self.title)
    
  def get_option(self, name, default=None):
    '''Retrieves the value of the given option'''
    if isinstance(self.options, dict):
      return self.options.get(name, default)
    return default
  
  def set_option(self, name, value):
    '''Sets the given option - does not save the contribution, so be sure to call .save() as well.'''
    if not isinstance(self.options, dict):  # force a dictionary
      self.options = {}
    self.options[name] = value
    
  def get_hash(self):
    '''Returns the hash for this thread. The hash is a stable value across time, and it includes a salt to make it nearly impossible to guess.
       The return is an md5 hash object, so call thread.get_hash().hexdigest() to get a string.
    '''
    m = hashlib.md5()
    m.update(self.created.isoformat().encode('utf8'))
    m.update(self.get_option('salt', 'somedefault').encode('utf8'))
    # returning the md5 object allows the caller to update() more stuff to it
    return m
    
    
MAX_COMMENT_FILE_SIZE = 10 * 1024 * 1024  # 10 mb   
MAX_NUM_COMMENT_FILES = 4  # 4 files per comment
    
class Comment(models.Model):
  '''A comment on a thread'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(hmod. SiteUser)
  thread = models.ForeignKey(Thread, related_name='comments')
  comment = models.TextField(blank=True, null=True)
  vote = models.IntegerField(default=0)
  files = models.ManyToManyField('homepage.UploadedFile')
  options = JSONField(blank=True, null=True)             # Artibrary options - these will never be queryable, but it 
                                                         # keeps us from constantly changing the database just to store a new option.
                                                         # See set_option and get_option below.
  
  def __str__(self):
    return '%s: %s...' % (self.id, self.comment[:20])
    
  def get_option(self, name, default=None):
    '''Retrieves the value of the given option'''
    if isinstance(self.options, dict):
      return self.options.get(name, default)
    return default
  
  def set_option(self, name, value):
    '''Sets the given option - does not save the contribution, so be sure to call .save() as well.'''
    if not isinstance(self.options, dict):  # force a dictionary
      self.options = {}
    self.options[name] = value
    
    
    

class VoteTicket(models.Model):
  '''A ticket for each thread vote'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(hmod.SiteUser)
  comment = models.ForeignKey(Comment)
  points = models.IntegerField(default=0)
