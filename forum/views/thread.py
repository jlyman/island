from django.conf import settings
from django.db.models import Count, Min, Max
from django_mako_plus.controller import view_function
from django.http import HttpResponse, HttpResponseRedirect, Http404
from management import models as mmod
from lib.filters import *
from forum import models as fmod
from . import templater, prepare_params



@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)
  
  # get the thread the user is after
  try:
    thread = fmod.Thread.objects.get(pk=request.urlparams[0])
  except (fmod.Thread.DoesNotExist, ValueError, TypeError):
    raise RedirectException('/forum/')
  
  # render the template
  params['thread'] = thread
  return templater.render_to_response(request, 'thread.html', params)
  
  
