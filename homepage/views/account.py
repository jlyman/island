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
      self.initial['field%s' % topic.id] = 'immediate'  # users don't necessarily have TopicNotification objects -- only if they have saved this form.  No object for a user means immediate.
      tn = tns.get(topic.id)
      if tn != None:
        self.initial['field%s' % topic.id] = tn.notification
  


#####################################################################
###   Unsubscription via links in emails
###   The user is likely not logged in for this, so we don't
###   use request.user anywhere, and we don't check permissions
###   beyond the hash.

@view_function
def unsubscribe(request):
  params = {}
  try:
      # get the thread
      try:
        thread = fmod.Thread.objects.get(id=request.urlparams[0])
      except (fmod.Thread.DoesNotExist, ValueError):
        raise AssertionError('The thread object (#%s) could not be found' % request.urlparams[0])

      # get the user object
      try:
        user = hmod.SiteUser.objects.get(id=request.urlparams[1])
      except (hmod.SiteUser.DoesNotExist, ValueError):
        raise AssertionError('The user object (#%s) could not be found' % request.urlparams[1])
  
      # check the hash - that's how we do security on these links since the user might not be logged in
      # this prevents hackers from spamming this endpoint and unsubscribing users - the thread.get_hash() can't be guessed because it contains the salt
      m = thread.get_hash()
      m.update((user.email or 'defaultemail').encode('utf8'))  # add some user info to it
      assert request.urlparams[2] == m.hexdigest(), 'The hash did not verify against the given user account'
  
      # get the topic the user wants to be unsubscribed from
      if not request.urlparams[3].strip():  # unsubscribe from all
        for topic in fmod.Topic.objects.order_by('sort_order'):
          tn, created = fmod.TopicNotification.objects.get_or_create(user=user, topic=topic)
          tn.notification = 'none'
          tn.save()
      
      else: # unsubscribe from a single topic
        try:
          topic = fmod.Topic.objects.get(key=request.urlparams[3])
          tn, created = fmod.TopicNotification.objects.get_or_create(user=user, topic=topic)
          tn.notification = 'none'
          tn.save()
        except (fmod.Topic.DoesNotExist, ValueError):
          raise AssertionError('The topic object (%s) could not be found' % request.urlparams[3])
          
  except AssertionError as e:      
    params['error_msg'] = str(e)
    
  # return the response
  return templater.render_to_response(request, 'account.unsubscribe.html', params)
