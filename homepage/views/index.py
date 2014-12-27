from django.conf import settings
from django_mako_plus.controller import view_function
from homepage import models as hmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from . import templater, prepare_params


@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)

  tasks = None
  if request.user.is_authenticated():
    mytasks = hmod.TaskTicket.objects.filter(user=request.user).values_list('task_id', flat=True)
    tasks = hmod.Task.objects.exclude(repeatable=False, id__in=mytasks).order_by('name')
  
  params['tasks'] = tasks

  return templater.render_to_response(request, 'index.html', params)