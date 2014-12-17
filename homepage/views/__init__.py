from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import RedirectException


###################################################
###   Create the emplater for this app once
templater = MakoTemplateRenderer('homepage')


###################################################
###   Helper functions used throughout the app

def prepare_params(request, require_authenticated=True):
  '''Creates a parameters dictionary for the current request.'''
  # users have to be logged in to be anywhere in this app
  if require_authenticated and not request.user.is_authenticated():
    raise RedirectException('/homepage/cover/')

  # we can add more stuff here when needed

  # return the parameters
  return {}
  