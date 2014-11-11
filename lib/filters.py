###
###  Note:
###
###  This module is imported *really* early on because it is imported in settings/__init..py.
###  Because of this, it shouldn't have any significant dependencies on other modules.  Keep
###  the import list minimal.
###
from django.conf import settings
import django.utils.translation 
import mako.filters
import base64, re, decimal, rjsmin, datetime


# so we can "from filters import *" and specify which names are returned to the global space
__all__ = (
  'html_escape',
  'url_escape',
  'xss_escape',
  'quote_escape',
  'split_paras',
  'check_ellipses',
  'commafy',
  'strip_whitespace',
  'scriptify',
  'pretty_decimal', 'format_number',
  'seconds_to_dhms', 'seconds_to_dhm', 'datetime_to_millis', 'millis_to_datetime', 
  'pretty_file_size',
  'force_int', 'force_float', 'force_decimal',
  'encode64', 'decode64', 'urlsafe_encode64', 'urlsafe_decode64',
  'toBase10', 'toBaseB',
)


# these functions actually come from Mako's built-in filters, but I've included them here so we don't need an extra import everywhere
html_escape = mako.filters.html_escape
url_escape = mako.filters.url_escape


# disallowed patterns used to xss_escape strings
disallowed_html_patterns = [
  ( re.compile('<(\s*)(script)', re.IGNORECASE | re.DOTALL),                       '&lt;\g<1>\g<2>' ),       # <script...
  ( re.compile('<(\s*)(style)', re.IGNORECASE | re.DOTALL),                        '&lt;\g<1>\g<2>' ),       # <style...
  ( re.compile('(javascript):', re.IGNORECASE | re.DOTALL),                        '\g<1>&#58;' ),           # javascript:
  ( re.compile('(vbscript):', re.IGNORECASE | re.DOTALL),                          '\g<1>&#58;'),            # vbscript:
  ( re.compile('(data):', re.IGNORECASE | re.DOTALL),                              '\g<1>&#58;' ),           # data:
  ( re.compile('-(moz)-(binding)', re.IGNORECASE | re.DOTALL),                     '&#45;\g<1>&#45;\g<2>'),  # -moz-binding...
  ( re.compile('(<\s*\w+[^>]+\s+on\w+\s*)=(\s*[\'"])', re.IGNORECASE | re.DOTALL), '\g<1>&#61;\g<2>' )       # <tag on*='...  (onChange, onClick, etc.)
]

def xss_escape(text):
  '''A Mako filter that can be used in templates, such as ${ myvar | xss_escape }.
     Using the regular HTML filter, such as ${ myvar | h }, is a stronger way to prevent XSS.
     However, you can't use it when you need to let HTML tags through the filter.
     The method uses a number of regular expressions to allow regular HTML through, but still disable XSS attacks.
     This function is automatically imported in all Mako templates by MakoTemplateRenderer below.
  '''
  if not text:
    return text
  for regex, repl in disallowed_html_patterns:
    text = regex.sub(repl, text)
  return text
    
    
def quote_escape(text):
  '''A Mako filter that escapes quotes and double quotes.  When quotes exist in variables in JavaScript,
     they usually mess up the code.  This places a backslash before them.
     This function is automatically imported in all Mako templates by MakoTemplateRenderer below.
  '''
  if not text:
    return text
  return text.replace('"', '\\"').replace("'", "\\'")


def split_paras(text):
  '''A Mako filter that turns all \n into <br>, splitting paragraphs nicely.
     Note that you must run the html filter before this one, or the <br>'s this 
     function adds will be esacped.
  '''
  if not text:
    return text
  return str(text).replace('\n', '<br>')


def check_ellipses(s, length):
  '''Limits the given string s to the length, adding ellipses (...) if needed'''
  if s == None:
    s = ''
  elif not isinstance(s, str):
    s = str(s)
  if len(s) > length:
    return '%s&hellip;' % s[:length]
  return s


def commafy(d):
  '''Makes a number human readable with commas'''
  s = '%0.2f' % d
  a,b = s.split('.')
  l = []
  while len(a) > 3:
      l.insert(0,a[-3:])
      a = a[0:-3]
  if a:
      l.insert(0,a)
  return ','.join(l)
  
  
RE_STRIP_WHITESPACE = re.compile('>\s+<')
def strip_whitespace(html):
  '''Removes all white space between html tags'''
  return RE_STRIP_WHITESPACE.sub('><', html)


RE_STRIP_SCRIPT = re.compile('^\s*<script[^>]*>(.*)</script>\s*$', re.IGNORECASE | re.DOTALL)
# the NAMESPACE_FIX is to bring our two global namespace variables into the current context
# this is needed when we return via ajax and JQuery executes code before it gets into the DOM.
#NAMESPACE_FIX = ''.join([
#  '$ = top.$;',
#  'jQuery = top.jQuery;',
#])
def scriptify(js_text):
  '''Surrounds the text with <script></script> (if needed) and minifies the javascript'''
  # I leave the <script> tags in all the html templates so our editors color them right
  # get the text between <script> and </script>, if it exists
  match = RE_STRIP_SCRIPT.search(js_text)
  if match:
    js_text = match.group(1)
  # minify on the fly - rjsmin is really fast, and it decreases download time
  if not settings.DEBUG:
    js_text = rjsmin.jsmin(js_text)
  # return the javascript
  return '<script>%s</script>' % (js_text)
#  return '<script>%s\n%s</script>' % (NAMESPACE_FIX, js_text)
  
  

###########################################################################################
###   Forces values to given types

def __force_type__(obj, default, types_to_force, conv_func, excs_to_catch):
  '''Internal method that forces the type'''
  # if already the type, just return
  if isinstance(obj, types_to_force):
    return obj
  # try to convert
  try:
    return conv_func(obj)
  except excs_to_catch:
    pass
  # return the default if we get here
  if isinstance(default, types_to_force):
    return default
  return conv_func(default)
  
  
def force_int(obj, default):
  '''Forces the given obj to an int, or assigns the required default value if an exception occurs.'''
  return __force_type__(obj, default, int, int, (TypeError, ValueError))
    
    
def force_decimal(obj, default):
  '''Forces the given obj to a decimal.Decimal, or assigns the required default value if an exception occurs.'''
  return __force_type__(obj, default, decimal.Decimal, decimal.Decimal, (TypeError, decimal.InvalidOperation))
    

def force_float(obj, default):
  '''Forces the given obj to a float, or assigns the required default value if an exception occurs.'''
  return __force_type__(obj, default, float, float, (TypeError, ValueError))


  

  
######################################################################################
###   Base64 encoding and decoding - Py3's base64 library returns byte strings, not
###   unicode strings.  Our code (including Django, Mako, etc.) works with Unicode strings.
###   These common functions take a Unicode string, convert to bytes, run base64,
###   then convert the bytes back into Unicode.  Unicode in, Unicode out.  Easier programming for all.
###   By making these central methods, we ensure all Base64 conversion happen
###   using the same byte encodings (utf8, ascii) all over our code.


def encode64(st, return_bytes=False):
  '''Encodes the given string to base64.'''
  return _b64encoder(st, base64.b64encode, return_bytes)

def decode64(b64_st, return_bytes=False):
  '''Decodes the given base64-encoded string.'''
  return _b64decoder(b64_st, base64.b64decode, return_bytes)

def urlsafe_encode64(st, return_bytes=False):
  '''Encodes the given string to base64.'''
  return _b64encoder(st, base64.urlsafe_b64encode, return_bytes)

def urlsafe_decode64(b64_st, return_bytes=False):
  '''Decodes the given base64-encoded string.'''
  return _b64decoder(b64_st, base64.urlsafe_b64decode, return_bytes)

def _b64encoder(st, b64_encoding_func, return_bytes=False):
  '''Does the actual encoding'''
  if not isinstance(st, bytes):
    st = st.encode('utf8')              # we now have a byte string rather than the original unicode text
  b64_byte_st = b64_encoding_func(st)   # we now have a base64-encoded byte string representing the text
  if return_bytes:
    return b64_byte_st
  return b64_byte_st.decode('ascii')    # we're now back to Unicode (using ascii decoding since base64 is all ascii characters)
    
def _b64decoder(b64_st, b64_decoding_func, return_bytes=False):
  '''Does the actual decoding'''
  if not isinstance(b64_st, bytes):
    b64_st = b64_st.encode('ascii')     # we now have a byte string of the base64-encoded text instead of the Unicode base64-encoded b64_st
  byte_st = b64_decoding_func(b64_st)   # we now have a byte string of the original text
  if return_bytes:
    return byte_st
  return byte_st.decode('utf8')         # we now have a Unicode string of the original text
  
  
  
  

####################################################################
###   Our number compressor - takes any int and makes it smaller
###   by converting to number base 64 using a custom alphabet
###   Note that converting a number base is different than
###   the base64 algorithm, which encodes a *string*.
###
###   This is used to make unique web ids, signup ids, etc.
###

def _toDigits(n, b=64):
    """Convert a positive number n to its digit representation in base b."""
    # Thanks to Andrej Bauer on stack overflow for this function
    digits = []
    while n > 0:
        digits.insert(0, n % b)
        n  = n // b
    return digits

def _fromDigits(digits, b=64):
    """Compute the number given by digits in base b."""
    # Thanks to Andrej Bauer on stack overflow for this function
    n = 0
    for d in digits:
        n = b * n + d
    return n
    

BASE_ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-'

BASE_ALPHABET_MAP = dict([ (BASE_ALPHABET[i], i) for i in range(len(BASE_ALPHABET)) ])

def toBaseB(n, b=64):
  '''Encode the base-10 int 'n' to base 'b' using our custom alphabet.'''
  assert b <= 64, 'Our custom alphabet only supports up to base 64 numbers.'
  return ''.join([ BASE_ALPHABET[d] for d in _toDigits(n, b) ])
  
def toBase10(n_st, b=64):
  '''Decode the number 'n_st' which is encoded in our custom alphabet back to a regular base-10 int'''
  assert b <= 64, 'Our custom alphabet only supports up to base 64 numbers.'
  try:
    return _fromDigits([ BASE_ALPHABET_MAP[d] for d in n_st ], b)
  except KeyError as e:
    raise KeyError('Invalid alphabet character for base-%s: %s' % (b, e.args[0]))




############################################################################################
###   Number "prettyfiers"

ONE = decimal.Decimal(1)
def pretty_decimal(d):
  '''Normalizes the decimal.Decimal to the fewest number of decimal places that accurately represent the number'''
  # see the decimal python documentation examples for this recipe
  if isinstance(d, decimal.Decimal):
    return d.quantize(ONE) if d == d.to_integral() else d.normalize()  
  return d
  

def format_number(n):
  '''Formats a number with commas as separators for thousands, etc.'''
  return "{:,}".format(n)



############################################################################################
###   Date "prettyfiers"

def seconds_to_dhms(seconds, labels=[ ' day', ' days', ' hour', ' hours', ' minute', ' minutes', ' second', ' seconds' ], delimiter=', '):
  '''Converts the given seconds into "w days, x hours, y minutes, z seconds".'''
  m, s = divmod(int(round(seconds)), 60)
  h, m = divmod(m, 60)
  d, h = divmod(h, 24)
  ret = []
  if d > 0:
    ret.append('%s%s' % (d, labels[0] if d == 1 else labels[1]))
  if h > 0:
    ret.append('%s%s' % (h, labels[2] if h == 1 else labels[3]))
  if m > 0:
    ret.append('%s%s' % (m, labels[4] if m == 1 else labels[5]))
  if s > 0:
    ret.append('%s%s' % (s, labels[6] if s == 1 else labels[7]))
  if len(ret) == 0:
    return '0%s' % (labels[6] if ret == 1 else labels[7])
  return delimiter.join(ret)


def seconds_to_dhm(seconds, labels=[ ' day', ' days', ' hour', ' hours', ' minute', ' minutes' ], delimiter=', '):
  '''Converts the given seconds into "w days, x hours, y minutes, z seconds".'''
  m = round(seconds / 60.0)
  h, m = divmod(m, 60)
  d, h = divmod(h, 24)
  ret = []
  if d > 0:
    ret.append('%s%s' % (d, labels[0] if d == 1 else labels[1]))
  if h > 0:
    ret.append('%s%s' % (h, labels[2] if h == 1 else labels[3]))
  if m > 0:
    ret.append('%s%s' % (m, labels[4] if m == 1 else labels[5]))
  if len(ret) == 0:
    return '0%s' % (labels[4] if ret == 1 else labels[5])
  return delimiter.join(ret)


EPOCH = datetime.datetime(1970, 1, 1)     

def datetime_to_millis(dt):
  '''Converts a datetime object to milliseconds'''
  return (dt - EPOCH).total_seconds()


def millis_to_datetime(millis):
  '''Converts milliseconds to a datetime object'''
  return datetime.datetime.fromtimestamp(millis / 1000.0)

      
##################################################################################
###  File size "prettyfiers"

def pretty_file_size(num):
  '''Displays a file size in human readable terms'''
  num = num / 1024.0
  for x in [ 'KB', 'MB', 'GB' ]:
    if num < 1024.0:
      return "%.1f %s" % (num, x)
    num /= 1024.0
  return "%.1f %s" % (num, 'TB')   
        
        
