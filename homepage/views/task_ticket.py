from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
import datetime

templater = MakoTemplateRenderer('homepage')

@view_function
def create(request):
  '''Create a task ticket'''

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover1/')

  # CHECK TO SEE IF TASK TICKET ALREADY EXISTS
  taskID = request.urlparams[0]
  task = mmod.Task.objects.get(id=taskID)
  try:
    ticket = mmod.TaskTicket.objects.get(user=request.user, task=task, start_time__isnull=False, end_time__isnull=True)

  except mmod.TaskTicket.DoesNotExist:
    ticket = mmod.TaskTicket()
    ticket.user = request.user
    ticket.task = task
    ticket.start_time = datetime.datetime.now()
    ticket.points = mmod.Task.objects.get(id=taskID).points
    ticket.save()

  template_vars = {
    'ticket': ticket,
  }

  return templater.render_to_response(request, 'create_task_ticket.html', template_vars)

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
  return HttpResponseRedirect('/homepage/profile1/')