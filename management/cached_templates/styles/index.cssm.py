# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1396237902.590313
_enable_loop = True
_template_filename = '/Users/ThongPham/Desktop/theCproject/homepage/styles/index.cssm'
_template_uri = 'index.cssm'
_source_encoding = 'ascii'
import os, os.path, re
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        timecolor = context.get('timecolor', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('.server-time {\n  font-size: 2em;\n  color: ')
        # SOURCE LINE 3
        __M_writer(str( timecolor ))
        __M_writer(';\n}\n\nhtml, body {\n  margin: 0;\n  padding: 0;\n}\n\nheader {\n  padding: 36px 0;\n  text-align: center;\n  font-size: 2.5em;\n  color: #F4F4F4;\n  background-color: #0088CC;\n}  ')
        return ''
    finally:
        context.caller_stack._pop_frame()


