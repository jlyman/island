from django.core.mail import send_mail
from django.core.handlers.base import BaseHandler  
from django.test.client import RequestFactory, FakePayload  
import collections


#####################################################
###   Utility functions

def flat_attr(attrs, level=0):
  '''Flattens the attribute map to a string ready to be put into a start tag.  The map can have embedded maps and/or lists, such as a style attribute with multiple items.'''
  if attrs == None:
    return ''
  elif isinstance(attrs, str):
    return attrs
  elif isinstance(attrs, collections.Mapping) and level == 0:  # dict
    return ' '.join( '%s="%s"' % (k, flat_attr(v, level+1)) for k, v in attrs.items() if v )
  elif isinstance(attrs, collections.Mapping) and level > 0:  # dict
    return ' '.join( '%s: %s;' % (k, flat_attr(v, level+1)) for k, v in attrs.items() if v )
  elif isinstance(attrs, collections.Iterable):  # list
    return ' '.join( flat_attr(v, level+1) for v in attrs if v )
  else:
    return str(attrs)
 
 
 
########################################################
###   Helper methods for running celery tasks

JSON_SERIALIZABLE = ( dict, list, tuple, str, bytes, int, float, bool, type(None) )
BODY_KEY = 'island_body_cached'
    
def get_fake_request(meta):
  '''Retrieves a fake request using the given request.META.  This allows celery tasks to have a "request" to use in code.'''
  # if the body was cached in the meta, put it back as the wsgi.input
  if BODY_KEY in meta:
    meta['wsgi.input'] = FakePayload(meta[BODY_KEY])
  
  # create a basic request using the Django testing framework
  request = RequestFactory().request(**meta)
  
  # run middleware on it
  handler = BaseHandler()  
  handler.load_middleware()  
  for middleware_method in handler._request_middleware:  
    response = middleware_method(request)
    if response:
      raise Exception("Middleware cannot return a response with a FakeRequest.")  
      
  # return the request
  return request   
  
  
def prepare_fake_meta(request, include_body=False):
  '''Removes any values in the dictionary that can't be serialized.  This is done in preparation for sending
     the request.META to a celery task.'''
  if request == None:
    return {}
    
  meta = dict([ (k,v) for k,v in request.META.items() if isinstance(v, JSON_SERIALIZABLE) ])
     
  # save the body so we can make it the input when getting the fake request
  if include_body and request.body:
    meta[BODY_KEY] = request.body
     
  return meta
     