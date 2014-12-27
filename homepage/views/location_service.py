from django.conf import settings
from . import templater, prepare_params
from django_mako_plus.controller import view_function
from homepage import models as hmod
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.http import HttpRequest


@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)

  SESSION_SAVE_EVERY_REQUEST=True

  if ('coor') not in (request.session):
    request.session.update({'coor': {}})

  if request.urlparams[0] == 'update':
    request.session['coor'].update({'lat': request.urlparams[1], 'long': request.urlparams[2]})
    request.session.save()  
  
  return templater.render_to_response(request, 'location_service.html', params)