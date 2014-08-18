# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1407781904.132813
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
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer("$(function(){\n\n  $('#start').off('click.add').on('click.add', function(evt) {\n    var taskID = ")
        __M_writer(str( request.urlparams[0] ))
        __M_writer(";\n    $.ajax({\n      url: '/homepage/task_ticket.create/' + taskID,\n      success:function(result){\n        $('#detail_instructions').html(result);\n        $('#start').remove();\n    }});\n  });\n\n\n\n});")
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"line_map": {"24": 4, "17": 0, "31": 25, "25": 4, "23": 1}, "source_encoding": "ascii", "uri": "detail.jsm", "filename": "/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/scripts/detail.jsm"}
__M_END_METADATA
"""
