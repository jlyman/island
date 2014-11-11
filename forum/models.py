from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser     
from jsonfield import JSONField
from management import models as mmod


######################################################################
###   Threads and comments - this is kept simple on purpose.
###   Threads are top-level items, comments are single level items on threads (no comments on comments).
###   The number of topics should be kept short.

class Topic(models.Model):
  '''Top-level topic.  We only want a few of these.  They are not created by users.  We want to force
     users to put their threads into only a few topics or it gets too combersome for users to select
     the topics they want filtered.'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  title = models.TextField(blank=True, null=True)
  
  def __str__(self):
    return '%s: %s' % (self.id, self.title)
    
    
class Thread(models.Model):    
  '''A discussion thread within a topic'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(mmod. SiteUser)
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
    
    
    
class Comment(models.Model):
  '''A comment on a thread'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(mmod. SiteUser)
  thread = models.ForeignKey(Thread, related_name='comments')
  comment = models.TextField(blank=True, null=True)
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
    