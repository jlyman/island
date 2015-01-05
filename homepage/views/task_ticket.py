from django.conf import settings
from . import templater, prepare_params
from django_mako_plus.controller import view_function
from homepage import models as hmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
import datetime
from django.utils.timezone import utc
import time
from django import forms


@view_function
def create(request):
  '''Create a task ticket'''
  # check user permissions and prepare the params
  params = prepare_params(request)

  # CHECK TO SEE IF TASK TICKET ALREADY EXISTS
  taskID = request.urlparams[0]
  task = hmod.Task.objects.get(id=taskID)

  try:
    taskSteps = hmod.TaskStep.objects.filter(task=task).order_by('sort_order')
  except hmod.TaskStep.DoesNotExist:
    taskSteps = []

  try:
    ticket = hmod.TaskTicket.objects.get(user=request.user, task=task, start_time__isnull=False, end_time__isnull=True)
  except hmod.TaskTicket.DoesNotExist:
    ticket = hmod.TaskTicket()
    ticket.user = request.user
    ticket.task = task
    ticket.points = hmod.Task.objects.get(id=taskID).points
    ticket.save()

  now = datetime.datetime.now()
  timediff = now - ticket.start_time
  
  params['ticket'] = ticket
  params['timediff_at_page_load'] = timediff.total_seconds()
  params['taskSteps'] = taskSteps
  return templater.render_to_response(request, 'task_ticket.create.html', params)


@view_function
def pre_finish(request):
  # check user permissions and prepare the params
  params = prepare_params(request)

  ticketID = request.urlparams[0]
  ticket = hmod.TaskTicket.objects.get(id=ticketID)
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/login/')
  form = RatingForm(request.POST or None)
  if request.method == 'POST':
    form = RatingForm(request.POST)
    if form.is_valid():
      ticket.comment = form.cleaned_data['comment']
      ticket.rating = form.cleaned_data['rating']
      ticket.save()
      return HttpResponseRedirect('/homepage/task_ticket.finish/' + str(ticketID))

  params.update({
    'form': form,
    'ticketID': ticketID,
  })

  return templater.render_to_response(request, 'rating.html', template_vars)

class RatingForm(forms.Form):
  '''This is a Django login form'''
  comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
  rating = forms.ChoiceField(required=True, choices=[(x, x) for x in range (1, 6)], widget=forms.Select(attrs={'class':'form-control'}))

@view_function
def finish(request):
  # check user permissions and prepare the params
  params = prepare_params(request)

  ticketID = request.urlparams[0];
  ticket = hmod.TaskTicket.objects.get(id=ticketID)
  ticket.end_time = datetime.datetime.now()
  ticket.save()
  user = request.user
  user.total_points = user.total_points + ticket.points
  user.save()
  return HttpResponseRedirect('/homepage/profile/')