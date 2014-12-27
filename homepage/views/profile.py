from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller import view_function
from homepage import models as hmod
from . import templater, prepare_params


@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)

  finishedTasks = hmod.TaskTicket.objects.filter(user=request.user, start_time__isnull=False, end_time__isnull=False).count()
  inProgressTasks = hmod.TaskTicket.objects.filter(user=request.user, start_time__isnull=False, end_time__isnull=True).count()
  mytasks = hmod.TaskTicket.objects.filter(user=request.user).values_list('task_id', flat=True)
  remainingTasks = hmod.Task.objects.exclude(repeatable=False, id__in=mytasks).order_by('name').count()

  params.update({
    'finishedTasks': finishedTasks,
    'inProgressTasks': inProgressTasks,
    'remainingTasks': remainingTasks,
  })

  return templater.render_to_response(request, 'profile.html', params)