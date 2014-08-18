from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.http import HttpRequest

templater = MakoTemplateRenderer('homepage')

@view_function
def process_request(request):

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover1/')

  SESSION_SAVE_EVERY_REQUEST=True

  if ('coor') not in (request.session):
    request.session.update({'coor': {}})

  if request.urlparams[0] == 'update':
    request.session['coor'].update({'lat': request.urlparams[1], 'long': request.urlparams[2]})
    request.session.save()  
  
  template_vars = {
  }

  return templater.render_to_response(request, 'location_service.html', template_vars)