from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import RedirectException


###################################################
###   Create the emplater for this app once
templater = MakoTemplateRenderer('forum')


###################################################
###   Helper functions used throughout the app

def prepare_params(request):
  '''Creates a parameters dictionary for the current request.'''
  # users have to be logged in to be anywhere in this app
  if not request.user.is_authenticated():
    raise RedirectException('/homepage/cover/')

  # return the parameters
  return {}
  