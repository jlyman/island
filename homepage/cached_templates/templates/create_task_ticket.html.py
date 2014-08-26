# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1408478117.689634
_enable_loop = True
_template_filename = '/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/templates/create_task_ticket.html'
_template_uri = 'create_task_ticket.html'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = ['content']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, 'base_ajax.htm', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        timer = context.get('timer', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        ticket = context.get('ticket', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer('\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        timer = context.get('timer', UNDEFINED)
        def content():
            return render_content(context)
        ticket = context.get('ticket', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n\n  <h4><div class="label label-danger" id="timing" timevalue="')
        __M_writer(str(timer))
        __M_writer('" style="position: fixed; left:0px; top: 50%;"></div></h4>\n  \n  <div class="container">\n    <div class="image"><img src="/static/homepage/media/image/no1.png" height="80px"/></div>\n    <div class="jumbotron step">    \n      Go to www.byu.edu\n    </div>\n  </div>\n\n  <div class="container">\n    <div class="image"><img src="/static/homepage/media/image/no2.png" height="80px"/></div>\n    <div class="jumbotron step">    \n      Go to www.byu.edu\n    </div>\n  </div>\n\n  <div class="container">\n    <div class="image"><img src="/static/homepage/media/image/no3.png" height="80px"/></div>\n    <div class="jumbotron step">    \n      Go to www.byu.edu\n    </div>\n  </div>\n\n  <div class="container">\n    <div class="image"><img src="/static/homepage/media/image/no4.png" height="80px"/></div>\n    <div class="jumbotron step">    \n      Go to www.byu.edu\n    </div>\n  </div>\n\n  <br/>\n\n  <div class="container">\n    <div class="jumbotron" style="padding-top: 15px; padding-bottom: 15px;">    \n      <a id="finish" class="btn btn-lg btn-success" href="/homepage/task_ticket.finish/')
        __M_writer(str( ticket.id ))
        __M_writer('" role="button">FINISH</a>\n    </div>\n  </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "create_task_ticket.html", "line_map": {"48": 3, "66": 60, "37": 1, "56": 3, "57": 5, "42": 43, "59": 39, "28": 0, "58": 5, "60": 39}, "source_encoding": "ascii", "filename": "/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/templates/create_task_ticket.html"}
__M_END_METADATA
"""
