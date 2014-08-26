from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
import datetime
from django.utils.timezone import utc
import time

templater = MakoTemplateRenderer('homepage')

@view_function
def create(request):
  '''Create a task ticket'''

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')

  # CHECK TO SEE IF TASK TICKET ALREADY EXISTS
  taskID = request.urlparams[0]
  task = mmod.Task.objects.get(id=taskID)
  try:
    ticket = mmod.TaskTicket.objects.get(user=request.user, task=task, start_time__isnull=False, end_time__isnull=True)

  except mmod.TaskTicket.DoesNotExist:
    ticket = mmod.TaskTicket()
    ticket.user = request.user
    ticket.task = task
    ticket.points = mmod.Task.objects.get(id=taskID).points
    ticket.save()

  now = datetime.datetime.now()
  timediff = now - ticket.start_time
  
  # print(ticket.start_time.strftime('%d-%m-%Y %H:%M:%S'))

  template_vars = {
    'ticket': ticket,
    'timediff_at_page_load': timediff.total_seconds(),
  }

  return templater.render_to_response(request, 'task_ticket.create.html', template_vars)


@view_function
def finish(request):
  '''Mark the task ticket as completed'''
  ticketID = request.urlparams[0];
  ticket = mmod.TaskTicket.objects.get(id=ticketID)
  ticket.end_time = datetime.datetime.now()
  ticket.save()
  user = request.user
  user.total_points = user.total_points + ticket.points
  user.save()
  return HttpResponseRedirect('/homepage/profile/')