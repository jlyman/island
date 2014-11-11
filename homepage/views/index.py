from django.conf import settings
from . import templater
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.http import HttpRequest

#Hello
@view_function
def process_request(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')

  tasks = None
  if request.user.is_authenticated():
    mytasks = mmod.TaskTicket.objects.filter(user=request.user).values_list('task_id', flat=True)
    tasks = mmod.Task.objects.exclude(repeatable=False, id__in=mytasks).order_by('name')
  
  template_vars = {
    'tasks' : tasks,
  }

  return templater.render_to_response(request, 'index.html', template_vars)