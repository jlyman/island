from django.conf import settings
from django_mako_plus.controller.router import MakoTemplateRenderer
from django_mako_plus.controller import view_function
from management import models as mmod
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function

templater = MakoTemplateRenderer('homepage')

@view_function
def process_request(request):

  if not request.user.is_authenticated():
    return HttpResponseRedirect('/homepage/cover/')

  taskID = request.urlparams[0]
  task = mmod.Task.objects.get(id=taskID)
  try:
    ticket = mmod.TaskTicket.objects.get(user=request.user, task=task, start_time__isnull=False, end_time__isnull=True)
    in_progress = True
    template_vars = {
      'in_progress': in_progress
    }
  except:
    in_progress = False
    template_vars = {
      'in_progress': in_progress
    }

  return templater.render_to_response(request, 'detail.html', template_vars)