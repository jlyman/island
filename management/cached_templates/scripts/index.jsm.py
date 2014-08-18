# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1396239747.025071
_enable_loop = True
_template_filename = '/Users/ThongPham/Desktop/theCproject/homepage/scripts/index.jsm'
_template_uri = 'index.jsm'
_source_encoding = 'ascii'
import os, os.path, re
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(" $(function() {\n  // update the time every 1 seconds\n  window.setInterval(function() {\n    $('.browser-time').text('The current browser time is ' + new Date() + '.');\n  }, ")
        # SOURCE LINE 5
        __M_writer(str( request.urlparams[1]))
        __M_writer(");\n\n  // update server time button\n  $('#server-time-button').click(function() {\n    $('.server-time').load('/homepage/index.gettime');\n  });\n});")
        return ''
    finally:
        context.caller_stack._pop_frame()


