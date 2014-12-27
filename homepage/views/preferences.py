from django import forms
from django.conf import settings
from django_mako_plus.controller import view_function, RedirectException
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.safestring import mark_safe
from homepage import models as hmod
from forum import models as fmod
from lib.filters import *
from lib.tables import TableHeader, ClientSideTable
from . import templater, prepare_params



@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)
  
  # prepare the table
  table = NotificationTable(request)
  topics = fmod.Topic.objects.order_by('sort_order')
  
  # render the template
  params['table'] = table
  return templater.render_to_response(request, 'preferences.html', params)
  
  
  
  
class NotificationTable(ClientSideTable):
  '''Our table of threads to display'''
  headings = [ 
    TableHeader('', 'col_name'),
    TableHeader('Immediate Email', 'col_immediate'), 
    TableHeader('Batched, Daily Email', 'col_batched'), 
    TableHeader('No Email', 'col_unsubscribed'), 
  ]
  css_class = 'customtable table table-hover'
  sortable = False
  
  
