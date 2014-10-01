from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.http import HttpRequest

templater = MakoTemplateRenderer('homepage')

@view_function
def process_request(request):

  finishedTasks = mmod.TaskTicket.objects.filter(user=request.user, start_time__isnull=False, end_time__isnull=False).count()
  inProgressTasks = mmod.TaskTicket.objects.filter(user=request.user, start_time__isnull=False, end_time__isnull=True).count()
  mytasks = mmod.TaskTicket.objects.filter(user=request.user).values_list('task_id', flat=True)
  remainingTasks = mmod.Task.objects.exclude(repeatable=False, id__in=mytasks).order_by('name').count()

  template_vars = {
    'finishedTasks': finishedTasks,
    'inProgressTasks': inProgressTasks,
    'remainingTasks': remainingTasks,
  }

  return templater.render_to_response(request, 'profile.html', template_vars)