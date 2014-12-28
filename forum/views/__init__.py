from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import RedirectException
from homepage.views import prepare_params as homepage_prepare_params

###################################################
###   Create the emplater for this app once
templater = get_renderer('forum')


###################################################
###   Helper functions used throughout the app

def prepare_params(request):
  '''Creates a parameters dictionary for the current request.'''
  # call the main prepare_params
  params = homepage_prepare_params(request, require_authenticated=True)
  
  # we can add more stuff here when needed

  # return the parameters
  return params
  
  
  