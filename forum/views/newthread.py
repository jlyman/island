from django import forms
from django.conf import settings
from django_mako_plus.controller import view_function, RedirectException
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.safestring import mark_safe
from homepage import models as hmod
from lib.filters import *
import lib.widgets
from forum import models as fmod
from . import templater, prepare_params



@view_function
def process_request(request):
  # check user permissions and prepare the params
  params = prepare_params(request)
  
  # handle the form
  form = ThreadForm(request)
  if request.method == 'POST':
    form = ThreadForm(request, request.POST)
    if form.is_valid():
      thread, comment = create_thread(request.user, form.cleaned_data['topic'], form.cleaned_data['title'], form.cleaned_data['comment'])
      return HttpResponseRedirect('/forum/thread/%s/' % thread.pk)

  # render the template
  params['form'] = form
  return templater.render_to_response(request, 'newthread.html', params)
  
  
  
class ThreadForm(forms.Form):
  '''Form to post new thread'''
  topic = forms.ChoiceField() # recreated with choices in constructor
  title = forms.CharField(label="Title:", max_length=250, required=True, widget=forms.TextInput(attrs={ 'class': 'form-control' }))
  comment = forms.CharField(label="Comment:", max_length=4000, required=True, widget=forms.Textarea(attrs={  'class': 'form-control', 'style': 'width: 100%; height: 94px;'}))

  def __init__(self, request, *args, **kwargs):
    super().__init__(*args, **kwargs)
    choices = []
    for topic in fmod.Topic.objects.order_by('sort_order'):
      choices.append(( topic.id, mark_safe('<div class="icon %s"></div><div class="topic_title">%s</div>' % (topic.icon, topic.title)) ))
      if topic.title == request.urlparams[0]:
        self.initial['topic'] = topic.id
    self.fields['topic'] = forms.ChoiceField(label="Topic:", required=True, choices=choices, widget=lib.widgets.ButtonChoiceWidget())
    if not self.initial.get('topic'):
      self.initial['topic'] = choices[0][0]
    
  def clean_topic(self):
    try:
      return fmod.Topic.objects.get(pk=self.cleaned_data['topic'])
    except fmod.Topic.DoesNotExist:
      raise forms.ValidationException('Please select a valid topic.')
      
      
def create_thread(user, topic, thread_title, first_comment):
  '''Creates a new thread.  This method is called by the view above as well as the settings/exim4_island_transport_handler.py file.'''
  thread = fmod.Thread(user=user)
  thread.topic = topic
  thread.title = thread_title
  thread.save()
  comment = fmod.Comment(user=user, thread=thread)
  comment.comment = first_comment
  comment.save()  
  return thread, comment