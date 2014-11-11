from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django_mako_plus.controller import view_function, RedirectException
from . import templater
import re, os, os.path

########################################################################################
###  Help page for the programmers - shows all fonts in the iconset we're using


RE_ICON = re.compile('^\.(.*)\:before.*$')
RE_COLOR = re.compile('^\.icon_color_(\w+) {.*$')

@view_function
def process_request(request):
  params = {}
  
  # parse the font-awesome file
  icon_names = []
  f = open(os.path.join(settings.BASE_DIR, 'homepage', 'styles', 'icomoon-fonts', 'icomoon-iconset.css'))
  for line in f:
    match = RE_ICON.search(line)
    if match:
      icon_names.append(match.group(1))
  f.close()
  
  # render the signup page
  params['icon_names'] = icon_names
  return templater.render_to_response(request, 'iconset.html', params)   


 
 