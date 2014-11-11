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
 