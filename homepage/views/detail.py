from django.conf import settings
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
from . import templater
import datetime
from django.utils.timezone import utc

@view_function
def process_request(request):

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')

  taskID = request.urlparams[0]
  task = mmod.Task.objects.get(id=taskID)
  try:
    ticket = mmod.TaskTicket.objects.get(user=request.user, task=task, start_time__isnull=False, end_time__isnull=True)
  except mmod.TaskTicket.DoesNotExist:
    ticket = None
    
  template_vars = {
    'ticket': ticket,
  }
  return templater.render_to_response(request, 'detail.html', template_vars)