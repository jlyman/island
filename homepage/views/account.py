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
  
  # handle the form
  notification_form = NotificationForm(request)
  if request.method == 'POST':
    notification_form = NotificationForm(request, request.POST)
    if notification_form.is_valid():
      for topic in fmod.Topic.objects.order_by('sort_order'):
        tn, created = fmod.TopicNotification.objects.get_or_create(user=request.user, topic=topic)
        tn.notification = notification_form.cleaned_data.get('field%s' % topic.id, 'immediate')
        tn.save()
      return HttpResponseRedirect('/homepage/account/')
      
  # render the response
  params['notification_form'] = notification_form
  return templater.render_to_response(request, 'account.html', params)
  
  
class NotificationForm(forms.Form):
  '''Form to change notifications'''
  def __init__(self, request, *args, **kwargs):
    super().__init__(*args, **kwargs)
    tns = dict(( tn.topic.id, tn ) for tn in fmod.TopicNotification.objects.filter(user=request.user) )
    # add the topics as fields
    for topic in fmod.Topic.objects.order_by('sort_order'):
      self.fields['field%s' % topic.id] = forms.ChoiceField(label=topic.title, required=True, choices=fmod.NOTIFICATION_CHOICES, widget=lib.widgets.ButtonChoiceWidget(btn_class="btn btn-default btn-sm", attrs={ 'class': "btn-group", 'role': "group" }))
      self.initial['field%s' % topic.id] = 'immediate'
      tn = tns.get(topic.id)
      if tn != None:
        self.initial['field%s' % topic.id] = tn.notification
  