# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1408477609.793526
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
        __M_writer('$(function(){\n\n  String.prototype.toHHMMSS = function () {\n    var sec_num = parseInt(this, 10); // don\'t forget the second param\n    var hours   = Math.floor(sec_num / 3600);\n    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);\n    var seconds = sec_num - (hours * 3600) - (minutes * 60);\n\n    if (hours   < 10) {hours   = "0"+hours;}\n    if (minutes < 10) {minutes = "0"+minutes;}\n    if (seconds < 10) {seconds = "0"+seconds;}\n    var time    = hours+\':\'+minutes+\':\'+seconds;\n    return time;\n}\n\n  $(\'#start\').off(\'click.add\').on(\'click.add\', function(evt) {\n    var taskID = ')
        __M_writer(str( request.urlparams[0] ))
        __M_writer(';\n    $.ajax({\n      url: \'/homepage/task_ticket.create/\' + taskID,\n      success:function(result){\n        $(\'#detail_instructions\').html(result);\n        $(\'#start\').remove(); \n        var timing = $(\'#timing\').attr("timevalue");\n        console.log(timing);\n        window.setInterval(function() {\n          $(\'#timing\').text(timing.toHHMMSS());\n          timing = parseInt(timing);\n          timing = timing + 1;\n          timing = timing.toString();\n        }, 1000);\n    }});\n\n  });\n\n')
        if in_progress:
            __M_writer("    $('#start').trigger('click.add');\n")
        __M_writer('\n});')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "detail.jsm", "line_map": {"17": 0, "35": 29, "24": 1, "25": 17, "26": 17, "27": 35, "28": 36, "29": 38}, "source_encoding": "ascii", "filename": "/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/scripts/detail.jsm"}
__M_END_METADATA
"""
