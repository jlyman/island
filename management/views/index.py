from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from datetime import datetime
import random 

templater = MakoTemplateRenderer('homepage')

@view_function
def process_request(request):
  
  template_vars = {
    'now': datetime.now().strftime(request.urlparams[0] if request.urlparams[0] else '%H:%M'),
    'timecolor': random.choice([ 'red', 'blue', 'green', 'brown' ]),
  }
  return templater.render_to_response(request, 'index.html', template_vars)

@view_function
def gettime(request):
  
  template_vars = {
    'now': datetime.now(),
  }
  return templater.render_to_response(request, 'index_time.html', template_vars)  