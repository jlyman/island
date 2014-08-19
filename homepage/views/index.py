from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.http import HttpRequest

templater = MakoTemplateRenderer('homepage')

@view_function
def process_request(request):

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')
  
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover1/')

  mytasks = mmod.TaskTicket.objects.filter(user=request.user).values_list('task_id', flat=True)
  tasks = mmod.Task.objects.exclude(repeatable=False, id__in=mytasks).order_by('name')
  
  template_vars = {
    'tasks' : tasks,
  }

  return templater.render_to_response(request, 'index.html', template_vars)