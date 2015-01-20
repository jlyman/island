#!/usr/bin/python3

__doc__ = '''
  Called by Exim4 when a new email is received.  Exim is set to pipe emails
  to this script when they are received by the system.
  
  In other words, this script is not meant to be called from the command line.
  It is called directly from exim4, which pipes the email body to stdin.
'''

import sys, os, re, email.parser

# initializes django
import init_django
init_django.initialize()

# regular imports
from homepage import models as hmod
from forum import models as fmod
from forum.views.newthread import create_thread
from forum.views.thread import send_comment_email_immediate, RE_MESSAGE_ID
from lxml import etree

# see settings.py for this logger setup
import logging
log = logging.getLogger('exim4_island_transport_handler')


# helper functions
SURROUNDS = (
  re.compile('<(.+)>'),
  re.compile('&lt;(.+)&gt;'),
)
def remove_surrounds(st):
  if not st:
    return ''
  for surround in SURROUNDS:  
    match = surround.search(st)
    if match:
      st = match.group(1)
  return st

# get the message information
msg_str = sys.stdin.read()
topic_key = os.environ.get('LOCAL_PART')

try:
  # parse the parts of the email
  try:
    msg = email.parser.Parser().parsestr(msg_str)
  except Exception as ex:
    raise Exception('Error parsing your email: %s' % ex)
  sender = remove_surrounds(msg['from'])
  assert sender, "Error: Could not parse the sending email address."
  title = msg['subject']
  assert title, "Error: Could not parse the title of your new thread."

  # check whether it's a bounce
  # right now we're just ignoring these, but we should disable bad emails after a few bounces come in.
  if topic_key.lower() == 'bounce':
    log.warning('Warning: Ignoring bounce on email: %s' % sender)
    sys.exit(0)

  # get the user object for this sender
  user = hmod.SiteUser.objects.filter(email__iexact=sender).first()
  assert user != None, 'Error: the email %s is not authenticated to post to this system. It must match whatever email is registered on the main BYU system.  Once you set your email with BYU, logout and re-login to island.byu.edu to update your information here.  This usually fixes any email issues.' % sender

  # get the topic object
  topic = fmod.Topic.objects.filter(key__iexact=topic_key).first()
  assert topic != None, 'Error: %s@island.byu.edu is an invalid topic. Please see the web site for valid topic names.' % topic_key
  
  # determine if this is a new thread or an existing thread
  thread_comment = None
  match = RE_MESSAGE_ID.search(msg['References'] or msg['In-Reply-To'] or '')
  if match:
    try:
      thread_comment = fmod.Comment.objects.get(id=match.group(1))
    except fmod.Comment.DoesNotExist:
      raise Exception('Error: The Island thread this email references could not be located.  It may have been deleted.')
    # check the hash
    assert match.group(2) == thread_comment.thread.get_hash().hexdigest(), 'Invalid hash on the email Message-ID header.'
    
  # get the first comment from the email body
  first_comment = ''
  charset = 'ascii'
  contenttype = ''
  attachments = []  # attached files
  # switch depending on whether we have a multipart message
  if not msg.is_multipart():
    first_comment = msg.get_payload(decode=True)
    charset = msg.get_charsets()[0]
    contenttype = msg.get_content_type()
  else:
    for part in msg.walk():  # walk through the parts and look for the html and plain parts
      if part.get_content_type() == 'text/html':  # html wins over plain text
        first_comment = part.get_payload(decode=True)
        charset = part.get_charsets()[0]
        contenttype = part.get_content_type()
      elif not first_comment and part.get_content_type() == 'text/plain':  # text/plain section
        first_comment = part.get_payload(decode=True)
        charset = part.get_charsets()[0]
        contenttype = part.get_content_type()
      elif part.get_filename():  # a file attachment
        filename = part.get_filename()
        filebytes = part.get_payload(decode=True)
        assert len(filebytes) < fmod.MAX_COMMENT_FILE_SIZE, 'The attachment named %s is above the limit of %s KB.' % (filename, fmod.MAX_COMMENT_FILE_SIZE / 1024)
        attachments.append((part['Content-Id'], filename, part.get_content_type(), filebytes))
        assert len(attachments) <= fmod.MAX_NUM_COMMENT_FILES, 'A maximum of %s attachments are allowed per comment.' % fmod.MAX_NUM_COMMENT_FILES

  assert first_comment, 'Error: the message part of your email appears to be empty.'
  # decode to unicode if we have bytes
  if isinstance(first_comment, bytes):
    first_comment = first_comment.decode(charset)

  # formatting if text/plain
  if contenttype == 'text/plain':
    # remove any lines that start with '>' - these are forwarded email text lines
    first_comment = re.sub('^>.*$\r?\n?', '', first_comment, flags=re.MULTILINE)
    # remove any email signature
    first_comment = re.split('^--\s$', first_comment or '', maxsplit=1, flags=re.MULTILINE)[0]
    # add some HTML to split lines (we have html within the system)
    for delim in ( '\r\n', '\n' ): # windows and unix line endings
      first_comment = first_comment.replace(delim, '<br/>')
    
  # formatting if text/html 
  if contenttype == 'text/html':
    root = etree.HTML(first_comment)
    # remove any <* type="cite"> tags - these are referenced messages (supposedly the standard way to include referenced messages)
    for node in root.xpath("//*[@type='cite']"):
      node.getparent().remove(node)
    # the gmail way to include referenced messages
    for node in root.xpath("//*[@class='gmail_extra']"):
      node.getparent().remove(node)
    # another gmail way to include referenced messages
    for node in root.xpath("//*[@class='gmail_quote']"):
      node.getparent().remove(node)
    # remove any inline graphics - we don't support this right now, but we could at some point - we just show icons for any attachments at the end of the post
    for node in root.xpath('//img'):
      node.getparent().remove(node)
    # remove any email signature by searching for "-- " in any text node
    for node in root.xpath("//*[re:match(text(), '^--\s$')]", namespaces={"re": "http://exslt.org/regular-expressions"}):
      while node != None:  # remove all remaining siblings
        temp_node = node
        node = node.getnext()
        temp_node.getparent().remove(temp_node)
    # step down to the body tag
    for node in root.xpath('//body'):
      root = node
    # convert the body tag to a div tag so we can put it in our html pages
    root.tag = 'div'
    # assign the string back to the first comment
    first_comment = etree.tostring(root, encoding='unicode')

  # create a new thread or add to an existing thread, depending on whether we found a references header
  if thread_comment:  # existing thread
    thread = thread_comment.thread
    comment = fmod.Comment(user=user, thread=thread)
    comment.comment = first_comment
    comment.save()  
    
  else:  # new thread
    thread, comment = create_thread(user, topic, title, first_comment)
  
  # add any attachments
  for cid, filename, contenttype, filebytes in attachments:
    cf = hmod.UploadedFile()
    cf.filename = filename
    cf.contenttype = contenttype
    cf.size = len(filebytes)
    cf.filebytes = filebytes
    cf.save()
    comment.files.add(cf)
    
  # prepare some fake meta
  meta = {
   'HTTP_HOST': 'island.byu.edu',
   'QUERY_STRING': '',
   'REMOTE_ADDR': '127.0.0.1',
   'REMOTE_PORT': '0',
   'REQUEST_METHOD': 'GET',
  }
    
  # send the emails
  log.warning('Sending email for comment: %s > %s' % (comment.id, comment.comment))
  send_comment_email_immediate(meta, comment)
  
  # signal to exim that we have success
  sys.exit(0)

except Exception as exc:
  exc_info = (type(exc), exc, exc.__traceback__)
  log.warning('Error: %s' % exc, exc_info=exc_info)
  print(str(exc))  # exim accepts this as the error to send back to the user
  sys.exit(1)