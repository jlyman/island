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
import re


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

  def clean_file1(self):
    if self.cleaned_data['file1']:
      if self.cleaned_data['file1'].size > fmod.MAX_COMMENT_FILE_SIZE:
        raise forms.ValidationError('The attached file is above the limit of %.1f KB.' % (fmod.MAX_COMMENT_FILE_SIZE / 1024))
    return self.cleaned_data['file1']
  

  
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
  
# parses the message id created in the method below
RE_MESSAGE_ID = re.compile('c(\d+)_([^@]+)@island.byu.edu')


def send_comment_email_immediate(request, comment):
  '''Sends email out for a given comment'''
  thread = comment.thread
  
  # create the unique message id
  headers = {}
  headers['Message-ID'] = '<c%i_%s@island.byu.edu>' % (comment.id, thread.get_hash().hexdigest())  # if we change this, we need to change the regex above
  subject = thread.title
  
  # reference it to the first comment in the thread.  Some email clients use References, some use In-Reply-To
  first_comment = fmod.Comment.objects.filter(thread=thread).order_by('created')[0]
  if first_comment != comment:
    subject = 'Re: %s' % subject
    headers['References'] = '<c%i_%s@island.byu.edu>' % (first_comment.id, thread.get_hash().hexdigest())
    headers['In-Reply-To'] = headers['References']
    
  # I'm doing this with SQL because I don't know how to make Django do it with the either-or situation
  # It's also more explicit this way so we know exactly who will be getting emails
  # Here's who gets emails here:
  #   1. Users with a TopicNotification record for the thread.topic set to 'immediate'.
  #   2. Users without a Topic Notification record for the thread.topic - i.e. NOT EXISTS.
  #
  params_list = []
  for user in hmod.SiteUser.objects.raw("""
    SELECT u.* 
    FROM homepage_siteuser AS u 
    WHERE EXISTS (
        SELECT * 
        FROM forum_topicnotification AS tn 
        WHERE tn.user_id=u.id 
          AND tn.topic_id=%s
          AND tn.notification='immediate'
    ) OR NOT EXISTS (
        SELECT notification 
        FROM forum_topicnotification AS tn2 
        WHERE tn2.user_id=u.id 
          AND tn2.topic_id=%s
    )
  """, (thread.topic.id, thread.topic.id)):
    # create a unique unsubscribe hash for this thread and user - this prevents hackers from unsubscribing people without the link
    m = thread.get_hash()
    m.update((user.email or 'defaultemail').encode('utf8'))  # add some user info to it
    
    # add parameters for this email
    params_list.append({
      'to_name': user.get_full_name(),
      'to_email': user.email,
      'to_id': user.id,
      'subject': subject,
      'comment': comment.comment,
      'comment_name': comment.user.get_full_name(),
      'comment_email': comment.user.email,
      'topic_title': thread.topic.title,
      'topic_key': thread.topic.key,
      'thread_id': thread.id,
      'unsubscribe_hash': m.hexdigest(),
    })
    
  # create the fake meta for celery
  if isinstance(request, dict):  # this occurs when called from the exim4 handler script
    meta = request
  else:
    meta = prepare_fake_meta(request)
    
  # call the html mailer with the params list and our email template
  # this needs to be switched to a celery call so it runs offline
  send_html_mail(meta, 'forum', 'comment.email.immediate.htm', [ cf.id for cf in comment.files.all() ], params_list, headers)
    
  
    
  