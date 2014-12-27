from django.conf import settings
from django_mako_plus.controller import view_function
from homepage import models as hmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
from . import templater, prepare_params
import datetime
from django.utils.timezone import utc

@view_function
def process_request(request):

  # check user permissions and prepare the params
  params = prepare_params(request)

  taskID = request.urlparams[0]
  task = hmod.Task.objects.get(id=taskID)
  try:
    ticket = hmod.TaskTicket.objects.get(user=request.user, task=task, start_time__isnull=False, end_time__isnull=True)
  except hmod.TaskTicket.DoesNotExist:
    ticket = None
    
  params['ticket'] = ticket
  return templater.render_to_response(request, 'detail.html', params)