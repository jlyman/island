import shortuuid

__doc__ = '''
  Middleware classes for our site.  We shouldn't have too many of these, so I'm just creating one file for all of them.
'''



###################################################
###   GUIDs to be used as unique ids in different
###   elements on the page.

class WebGuidMiddleware:
  '''Attaches a web-valid guid generator to each request'''
  def process_request(self, request):
    # add the generator to the request
    request.generate_webid = WebIdGenerator()


class WebIdGenerator(object):
  '''A callable class that returns the next web-valid guid in the sequence for the given request.
     Don't use this class directly.  Instead, call this with something like:
     
       wid = request.get_unique_id()
     
    I purposely didn't use a generator for this because I want a normal method call syntax
    to be consistent with the rest of the class.
  '''
  def __init__(self):
    # a base_guid and a counter ensures 1) speed and 2) unique guids are created throughout the request
    self.counter = 0
    self.base_guid = None  
  
  def __call__(self):
    # we generate the guid late because many requests don't need one
    if self.base_guid == None:
      self.base_guid = shortuuid.uuid()  
    self.counter += 1
    return 'g%s%x' % (self.base_guid, self.counter)  # start with arbitrary letter g because element ids must start with a letter


