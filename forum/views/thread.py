from django import forms
from django.conf import settings
from django.db.models import Sum
from django.db.models import Q
from django_mako_plus.controller import view_function, RedirectException
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage import models as hmod
from lib.filters import *
from lib import get_fake_request, prepare_fake_meta
from lib.mailer import send_html_mail
from lib.ckeditor import ckEditorWidget
from forum import models as fmod
from . import templater, prepare_params



@view_function
def process_request(request):
  '''Main thread view'''
  # check user permissions and prepare the params
  params = prepare_params(request)
  
  # get the thread the user is after
  try:
    thread = fmod.Thread.objects.get(pk=request.urlparams[0])
  except (fmod.Thread.DoesNotExist, ValueError, TypeError):
    raise RedirectException('/forum/')

  # handle the form
  comment_form = CommentForm(request)
  if request.method == 'POST':
    comment_form = CommentForm(request, request.POST, request.FILES)
    if comment_form.is_valid():
      # create the comment, and add any files
      comment = fmod.Comment(user=request.user, thread=thread)
      comment.comment = comment_form.cleaned_data['comment']
      comment.save()
      if comment_form.cleaned_data['file1']:
        cf = hmod.UploadedFile()
        cf.filename = comment_form.cleaned_data['file1'].name
        cf.contenttype = comment_form.cleaned_data['file1'].content_type
        cf.size = comment_form.cleaned_data['file1'].size
        cf.filebytes = comment_form.cleaned_data['file1'].read()
        cf.save()
        comment.files.add(cf)
        
      # send the emails
      send_comment_email_immediate(request, comment)
      
      # forward to the comment so we don't get a double post on reload
      return HttpResponseRedirect('/forum/thread/%s#comment_%s' % (thread.pk, comment.pk))  # redirect so the user doesn't accidentally post again by hitting refresh
  
  # render the template
  params['comment_form'] = comment_form
  params['thread'] = thread
  params['comments'] = thread.comments.order_by('created')
  return templater.render_to_response(request, 'thread.html', params)
  
  
class CommentForm(forms.Form):
  '''Form to post new comment'''
  comment = forms.CharField()  # recreated in __init__ below
  file1 = forms.FileField(label="Attach a File:", required=False)
  
  def __init__(self, request, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['comment'] = forms.CharField(label="", max_length=4000, required=True, widget=ckEditorWidget(request, toolbar='be_small', attrs={ 'style': 'height: 250px;' }))

  

  
#####################################################
###   Ajax endpoint to vote on a comment
  
@view_function
def vote(request):
  # check user permissions and prepare the params
  params = prepare_params(request)

  # handle vote button
  comment = fmod.Comment.objects.get(id=request.REQUEST.get('id'))
  
  # create/modify the vote ticket
  vt, created = fmod.VoteTicket.objects.get_or_create(user=request.user, comment=comment)
  vt.points = 1 if request.REQUEST.get('vote') == 'up' else 0
  vt.save()
  
  # recalculate the total votes on the item by doing a sum query
  comment.vote = fmod.VoteTicket.objects.filter(comment=comment).aggregate(Sum('points'))['points__sum']
  comment.save()
  
  # return the comment vote
  return HttpResponse(comment.vote)
  




###################################################
###   Downloads/views an attachment to a comment

@view_function
def attachment(request):
  # check user permissions and prepare the params
  params = prepare_params(request)

  # get the cf
  try:
    cf = hmod.UploadedFile.objects.get(id=request.urlparams[0])
  except (ValueError, hmod.UploadedFile.DoesNotExist):
    raise Http404
    
  # return the response
  return cf.get_response(attachment=request.urlparams[1] != 'inline')






#############################################
###   Sends notifications for new comments
  
def send_comment_email_immediate(request, comment):
  '''Sends email out for a given comment'''
  # we pull anyone without a TN object or those with explicit "immediate" for this topoic
  params_list = []
  for user in hmod.SiteUser.objects.filter(Q(topicnotification__isnull=True) | Q(topicnotification__topic=comment.thread.topic, topicnotification__notification='immediate')):
    params_list.append({
      'to_name': user.fullname,
      'to_email': user.email,
      'subject': comment.thread.title,
      'comment': comment.comment,
      'topic_title': comment.thread.topic.title,
      'topic_key': comment.thread.topic.key,
    })
    
  # create the unique message id
  headers = {}
  headers['Message-ID'] = '<comment%i@island.byu.edu>' % comment.id
  
  # reference it to the first comment in the thread
  first_comment = fmod.Comment.objects.filter(thread=comment.thread).order_by('created')[0]
  if first_comment != comment:
    headers['References'] = '<comment%i@island.byu.edu>' % first_comment.id
  
  # call the html mailer with the params list and our email template
  # this needs to be switched to a celery call so it runs offline
  send_html_mail(prepare_fake_meta(request), 'forum', 'comment.email.immediate.htm', [ cf.id for cf in comment.files.all() ], params_list, headers)
    
  
    
  