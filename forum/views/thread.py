from django import forms
from django.conf import settings
from django.db.models import Sum
from django_mako_plus.controller import view_function, RedirectException
from django.http import HttpResponse, HttpResponseRedirect, Http404
from management import models as mmod
from lib.filters import *
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
  comment_form = CommentForm()
  if request.method == 'POST':
    comment_form = CommentForm(request.POST, request.FILES)
    if comment_form.is_valid():
      comment = fmod.Comment(user=request.user, thread=thread)
      comment.comment = comment_form.cleaned_data['comment'].replace('\r\n', '<br/>').replace('\n', '<br/>')
      comment.save()
      if comment_form.cleaned_data['file1']:
        cf = fmod.CommentFile(comment=comment)
        cf.filename = comment_form.cleaned_data['file1'].name
        cf.contenttype = comment_form.cleaned_data['file1'].content_type
        cf.size = comment_form.cleaned_data['file1'].size
        cf.filebytes = comment_form.cleaned_data['file1'].read()
        cf.save()
      return HttpResponseRedirect('/forum/thread/%s#comment_%s' % (thread.pk, comment.pk))  # redirect so the user doesn't accidentally post again by hitting refresh
  
  # render the template
  params['comment_form'] = comment_form
  params['thread'] = thread
  params['comments'] = thread.comments.order_by('created')
  return templater.render_to_response(request, 'thread.html', params)
  
  
class CommentForm(forms.Form):
  '''Form to post new comment'''
  comment = forms.CharField(label="", max_length=4000, required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 100%; height: 94px;'}))
  file1 = forms.FileField(label="Attach a File:", required=False)

  
  
  
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
    cf = fmod.CommentFile.objects.get(id=request.urlparams[0])
  except (ValueError, fmod.CommentFile.DoesNotExist):
    raise Http404
    
  # return the response
  return cf.get_response(attachment=request.urlparams[1] != 'inline')
