# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1404700418.824627
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/styles/cover1.cssm'
_template_uri = 'cover1.cssm'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('html { \n  background: no-repeat center center fixed; \n  -webkit-background-size: cover;\n  -moz-background-size: cover;\n  -o-background-size: cover;\n  background-size: cover;\n}')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"17": 0, "28": 22, "22": 1}, "uri": "cover1.cssm", "filename": "/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/styles/cover1.cssm"}
__M_END_METADATA
"""
