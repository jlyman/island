from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser     
from polymorphic import PolymorphicModel

class Level(models.Model):
  name = models.TextField(blank=False, null=False)
  description = models.TextField(blank=True, null=True)
  points_required = models.IntegerField(max_length=200, blank=False, null=False)
  def __str__(self):
    return str(self.id) + ' ' + self.name

class UserType(models.Model):
  name = models.TextField(blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  def __str__(self):
    return str(self.id) + ' ' + self.name

class SiteUser(AbstractUser):
  level = models.ForeignKey(Level, blank=True, null=True)
  user_type = models.ForeignKey(UserType, blank=True, null=True)
  fullname = models.TextField(blank=True, null=True)
  mail = models.TextField(blank=True, null=True)
  phone = models.TextField(blank=True, null=True)
  BYU_status = models.TextField(blank=True, null=True)
  total_points = models.IntegerField(max_length=200, blank=True, null=True, default=0)
  def __str__(self):
    return str(self.id) + ' ' + self.username

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
    return str(self.id) + ' ' + self.name

class TaskStep(models.Model):
  task = models.ForeignKey(Task)
  sort_order = models.IntegerField(max_length=200, blank=True, null=True)
  description = models.TextField(blank=True, null=True)

class TaskTicket(models.Model):
  user = models.ForeignKey(SiteUser)
  task = models.ForeignKey(Task)
  start_time = models.DateTimeField(auto_now_add=True)
  end_time = models.DateTimeField(blank=True, null=True)
  rating = models.IntegerField(max_length=200, blank=True, null=True)
  comments = models.TextField(blank=True, null=True)
  points = models.IntegerField(max_length=200, blank=True, null=True)
  def __str__(self):
    return str(self.id)