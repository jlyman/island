from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import RedirectException
from homepage import models as hmod
from forum import models as fmod

###################################################
###   Create the emplater for this app once
templater = MakoTemplateRenderer('homepage')


###################################################
###   Helper functions used throughout the app

def prepare_params(request, require_authenticated=True):
  '''Creates a parameters dictionary for the current request.'''
  params = {}
  
  # users have to be logged in to be anywhere in this app
  if require_authenticated and not request.user.is_authenticated():
    raise RedirectException('/homepage/cover/')

  # get the latest job postings and latest topics
  params['latest_jobs'] = fmod.Thread.objects.filter(topic__title='Jobs').order_by('-created')
  params['latest_threads'] = fmod.Thread.objects.exclude(topic__title='Jobs').order_by('-created')

  # return the parameters
  return params
  