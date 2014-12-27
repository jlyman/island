from django import forms
from django.conf import settings
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
from homepage import models as hmod
from forum import models as fmod
import lib.widgets
from . import templater, prepare_params


@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)
  
  # get the current user subscriptions
  params['topics'] = fmod.Topic.objects.order_by('sort_order')
  params['optout'] = fmod.TopicOptOut.objects.filter(user=request.user).values_list('topic_id', flat=True)

  return templater.render_to_response(request, 'account.html', params)
  
  

  