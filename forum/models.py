from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser     
from django.http import HttpResponse, HttpResponseRedirect, Http404
from lib.filters import *
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
  sort_order = models.IntegerField(blank=True, null=True)
  title = models.TextField(blank=True, null=True)
  icon = models.TextField(blank=True, null=True)
  
  def __str__(self):
    return '%s: %s' % (self.id, self.title)
    
    
class Thread(models.Model):    
  '''A discussion thread within a topic'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(mmod.SiteUser)
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
  vote = models.IntegerField(default=0)
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
    
    
MAX_COMMENT_FILE_SIZE = 10 * 1024 * 1024  # 10 mb   
MAX_NUM_COMMENT_FILES = 4  # 4 files per comment
    
class CommentFile(models.Model):
  '''A file attached to a Comment. We store attached files directly in the database because it's much simpler
     (conceptually) that way.  This is not a high-traffic site, and it doesn't need the higher throughput of
     storing the files on the filesystem.  Very few comments have files attached, so we're doing what most would 
     say is a bad idea. :)  We can always switch it in the future if it becomes an issue.'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  comment = models.ForeignKey(Comment)
  filename = models.TextField(blank=True, null=True)
  contenttype = models.TextField(blank=True, null=True)
  size = models.IntegerField()
  filebytes = models.BinaryField(blank=True, null=True)
  
  def __str__(self):
    return 'CommentFile: %s (%s), %s bytes' % (self.filename, self.contenttype, self.size)
    

  def get_response(self, attachment=True):
    '''Returns an HttpResponse that downloads this file.'''   
    response = HttpResponse(content_type=self.contenttype)
    if attachment:
      response['Content-Disposition'] = 'attachment; filename="%s"' % url_escape(self.filename)
    response.write(self.filebytes)
    return response
    

class VoteTicket(models.Model):
  '''A ticket for each thread vote'''
  created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  user = models.ForeignKey(mmod.SiteUser)
  comment = models.ForeignKey(Comment)
  points = models.IntegerField(default=0)
