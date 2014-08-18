from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function

templater = MakoTemplateRenderer('homepage')

@view_function
def process_request(request):

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover1/')

  template_vars = {

    }

  return templater.render_to_response(request, 'detail.html', template_vars)