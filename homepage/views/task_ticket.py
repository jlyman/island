from django.conf import settings
from . import templater
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
import datetime
from django.utils.timezone import utc
import time
from django import forms


@view_function
def create(request):
  '''Create a task ticket'''
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')

  # CHECK TO SEE IF TASK TICKET ALREADY EXISTS
  taskID = request.urlparams[0]
  task = mmod.Task.objects.get(id=taskID)

  try:
    taskSteps = mmod.TaskStep.objects.filter(task=task).order_by('sort_order')
  except mmod.TaskStep.DoesNotExist:
    taskSteps = []

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
  
  template_vars = {
    'ticket': ticket,
    'timediff_at_page_load': timediff.total_seconds(),
    'taskSteps': taskSteps,
  }

  return templater.render_to_response(request, 'task_ticket.create.html', template_vars)


@view_function
def pre_finish(request):
  ticketID = request.urlparams[0]
  ticket = mmod.TaskTicket.objects.get(id=ticketID)
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')
  form = RatingForm(request.POST or None)
  if request.method == 'POST':
    form = RatingForm(request.POST)
    if form.is_valid():
      ticket.comment = form.cleaned_data['comment']
      ticket.rating = form.cleaned_data['rating']
      ticket.save()
      return HttpResponseRedirect('/homepage/task_ticket.finish/' + str(ticketID))

  template_vars = {
    'form': form,
    'ticketID': ticketID,
  }

  return templater.render_to_response(request, 'rating.html', template_vars)

class RatingForm(forms.Form):
  '''This is a Django login form'''

  comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
  rating = forms.ChoiceField(required=True, choices=[(x, x) for x in range (1, 6)], widget=forms.Select(attrs={'class':'form-control'}))

@view_function
def finish(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')

  '''Mark the task ticket as completed'''
  ticketID = request.urlparams[0];
  ticket = mmod.TaskTicket.objects.get(id=ticketID)
  ticket.end_time = datetime.datetime.now()
  ticket.save()
  user = request.user
  user.total_points = user.total_points + ticket.points
  user.save()
  return HttpResponseRedirect('/homepage/profile/')