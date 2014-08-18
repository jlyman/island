# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1405806396.377982
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/Programming/Web/thecproject/homepage/scripts/index.jsm'
_template_uri = 'index.jsm'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer("$(function(){\n  $('#tiles .img-li').wookmark({\n    autoResize: true, // This will auto-update the layout when the browser window is resized.\n    container: $('#image-container'), // Optional, used for some extra CSS styling\n    offset: 20, // Optional, the distance between grid items\n    itemWidth: 250 // Optional, the width of a grid item\n  });\n});")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"line_map": {"17": 0, "28": 22, "22": 1}, "source_encoding": "ascii", "uri": "index.jsm", "filename": "/Users/thongpham/Desktop/Programming/Web/thecproject/homepage/scripts/index.jsm"}
__M_END_METADATA
"""
