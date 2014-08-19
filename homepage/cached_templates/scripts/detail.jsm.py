# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1408397780.314174
_enable_loop = True
_template_filename = '/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/scripts/detail.jsm'
_template_uri = 'detail.jsm'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        in_progress = context.get('in_progress', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer("$(function(){\n\n  $('#start').off('click.add').on('click.add', function(evt) {\n    var taskID = ")
        __M_writer(str( request.urlparams[0] ))
        __M_writer(";\n    $.ajax({\n      url: '/homepage/task_ticket.create/' + taskID,\n      success:function(result){\n        $('#detail_instructions').html(result);\n        $('#start').remove();\n    }});\n  });\n\n")
        if in_progress:
            __M_writer("    $('#start').trigger('click.add');\n")
        __M_writer('\n});')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"line_map": {"17": 0, "35": 29, "24": 1, "25": 4, "26": 4, "27": 13, "28": 14, "29": 16}, "filename": "/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/scripts/detail.jsm", "uri": "detail.jsm", "source_encoding": "ascii"}
__M_END_METADATA
"""
