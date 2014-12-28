import django.forms # can't do from django import forms because this class has the same name
import django.forms.widgets
from django.forms.util import flatatt
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.utils.safestring import mark_safe
from lib.filters import *
import decimal, re, json, os, os.path


TOOLBARS = {
  'be_normal': json.dumps([
    	{ 'name': 'clipboard', 'items': [ 'Cut', 'Copy', 'Paste', '-', 'Undo', 'Redo' ] },
    	{ 'name': 'styles', 'items': [ 'Format', 'Font', 'FontSize' ] },
    	{ 'name': 'colors', 'items': [ 'TextColor', 'BGColor' ] },
    	{ 'name': 'editing', 'items': [ 'Find', 'Replace', ] },
    	'/',
    	{ 'name': 'basicstyles', 'items': [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ] },
      { 'name': 'paragraph2', 'items': [ 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',  ] },
    	{ 'name': 'paragraph', 'items': [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'  ] },
    	{ 'name': 'links', 'items': [ 'Link', 'Unlink' ] },
    	{ 'name': 'source', 'items': [ 'Source' ] },
  ]),
  'be_tiny': json.dumps([
    	{ 'name': 'basicstyles', 'items': [ 'Bold', 'Italic', 'Underline', ] },
    	{ 'name': 'paragraph', 'items': [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent' ] },
  ]),
  'be_small': json.dumps([
    	{ 'name': 'styles', 'items': [ 'Format', 'Font', 'FontSize' ] },
    	{ 'name': 'basicstyles', 'items': [ 'Bold', 'Italic', 'Underline', ] },
    	{ 'name': 'paragraph', 'items': [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent' ] },
    	{ 'name': 'source', 'items': [ 'Source' ] },
  ]),
  'be_book_editor': json.dumps([
    	{ 'name': 'basicstyles', 'items': [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'Undo', 'Redo' ] },
  ]),
}
    
    
####################################################
###   ckEditor rich text editor


class ckEditorWidget(django.forms.Widget):
  '''A TextArea control that has the ckEditor rich text enabled on it.'''
  def __init__(self, request, *args, **kwargs):
    self.request = request
    # set the toolbar
    self.toolbar = 'be_normal'
    if 'toolbar' in kwargs:
      self.toolbar = kwargs['toolbar']
      del kwargs['toolbar']
    # call the super's constructor
    super().__init__(*args, **kwargs)    
    
    
  def value_from_datadict(self, data, files, name):
      """
      Given a dictionary of data and this widget's name, returns the value
      of this widget. Returns None if it's not provided.
      """
      value = data.get(name, None)
      return value
      

  def render(self, name, value, attrs=None):
    uniqueid = self.request.generate_webid()
    html = []

    # textarea with the value
    if value is None:
      value = ''
    final_attrs = self.build_attrs(attrs, name=name)
    html.append('<span id="%s"><textarea%s>%s</textarea></span>' % (uniqueid, flatatt(final_attrs), html_escape(value)))
    
    # infer the height and width
    styles = parse_style(final_attrs.get('style', ''))
    height = final_attrs.get('height') or styles.get('height') or '250px'
    width = final_attrs.get('width') or styles.get('width') or '100%'

    # add the ckEditor to it
    html.append(scriptify('''
        $(function() {
          var container = $("#%(uniqueid)s");
          var textarea = container.find('textarea');

          // initialize the ckeditor component and get the editor component
          var editor = textarea.ckeditor({
            height: "%(height)s",
            width: "%(width)s",
            toolbar: %(toolbar)s,
            extraAllowedContent: 'img[src,alt,width,height]',
          }).editor;
          
          // replicate a few events on the editor to the textarea behind it
          editor.on('blur', function() {
            textarea.trigger('blur');
          });//blur
          editor.on('focus', function() {
            textarea.trigger('focus');
          });//blur
          editor.on('change', function() {
            textarea.trigger('change');
          });//blur
          
          // destroy the editor when the textarea is removed from the DOM (this is needed by essay.py widget); this is an event in "jquery ui"
          textarea.on('remove', function() {
            editor.destroy();
          });
          
        });//ready
    ''' % {
      'uniqueid': uniqueid,
      'height': height,
      'width': width,
      'toolbar': TOOLBARS.get(self.toolbar) or TOOLBARS['be_normal'],
    }))
    
    # return the html
    return '\n'.join(html)



def parse_style(style):
  '''Parses an html style="foo: bar; foo2: bar2;" attribute into a dict.
     The style parameter should be something like "foo: bar; foo2: bar2;"
     This is not perfectly robust, but will do most styles and is good enough to be used above since we control the book XML.
  '''
  
  ret = {}
  for item in style.split(';'):
    colonpos = item.find(':')
    if colonpos > 0:
      ret[item[:colonpos].strip()] = item[colonpos+1:].strip()
  return ret
  