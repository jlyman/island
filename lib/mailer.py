from django_mako_plus.controller.router import get_renderer
from django.core.mail import EmailMultiAlternatives
import types, mimetypes
from lib.filters import *
from lib import get_fake_request, prepare_fake_meta
from homepage import models as hmod
from email.mime.base import MIMEBase
import lxml.html
  

####################################################################################################
###   Wrapper for sending HTML email that automatically converts the html to a text alternative.
###   Sends the email offline using the Celery framework. 

MAIL_REPLACEMENTS = [
  ( '</p>', '&#xa;&#xa;</p>' ),
  ( '<br>', '&#xa;<br>' ),
  ( '<li>', '<li>- ' ),
  ( '</li>', '&#xa;</li>' ),
]

def send_html_mail(meta, app, template, upload_file_ids, params_list, email_headers={}):
  '''This method is meant to be called through celery -- thus the meta instead of request.
     It sends html mail, creating the text content manually if not specified.  
     
     The template is the template to render.  It must have def's named:
       email_from_block
       email_to_block
       email_subject_block
       email_html_block
       email_text_block
     
     The params_list is a list of parameters sent into the template.  These are used as 
     variables in the template.  Each dictionary should represent one email to be sent:
     [
        {
            'to_address': 'someone@somewhere.com,
            'from_address': 'learning@myeducator.com', # optional (default in base_email_template is learning@myeducator.com)
            'text_body': 'Text version of message',    # optional
            # any other parameters used in your template
        },
        # more dictionaries here
     ]
     
     Attachments must be in template blocks named attachment1_block, attachment2_block, etc.
     Inside the block, it should be filename:base64 encoded file bytes
     Convert files to base64 here: http://base64converter.com/      
  '''
  # prepare a fake request   
  request = get_fake_request(meta)
  templater = get_renderer(app)
     
  # loop through all the recipients
  for params in params_list:
    # render the template to get the parts of the email
    from_address = templater.render(request, template, params, def_name='email_from_block').strip()
    to_address = templater.render(request, template, params, def_name='email_to_block').strip()
    subject = templater.render(request, template, params, def_name='email_subject_block').strip()
    html_body = templater.render(request, template, params, def_name='email_html_block').strip()
    text_body = templater.render(request, template, params, def_name='email_text_block').strip()
    
    # if the text_body is empty, created it from the html_body
    if not text_body:
      text = html_body
      for orig, repl in MAIL_REPLACEMENTS:
        text = text.replace(orig, repl)
      text_body = lxml.html.fromstring(text).text_content()
      
    # create the mail message object
    msg = EmailMultiAlternatives(subject, text_body, from_address, [ to_address ], headers=email_headers)
    msg.mixed_subtype = 'related'  # tells mail clients to not show attachments if they are referenced inline (otherwise we see double images)
    msg.attach_alternative(html_body, 'text/html')
      
    # add any attachments
    for upload_file_id in upload_file_ids:
      try:
        uf = hmod.UploadedFile.objects.get(id=upload_file_id)
      except hmod.UploadedFile.DoesNotExist:
        continue
        
      major, minor = uf.contenttype.split('/')
      attachment = MIMEBase(major, minor)
      attachment.add_header('Content-ID', '<attachment%i>' % uf.id)
      attachment.add_header('Content-Transfer-Encoding', 'base64')
      attachment.add_header('Content-Disposition', 'inline', filename=uf.filename)
      attachment.set_payload(encode64(bytes(uf.filebytes)))  
      msg.attach(attachment)
      
    # send the mail
    try:
      msg.send()
    except Exception as e:
      print('Error sending email to %s: %s' % (to_address, e))
     
  