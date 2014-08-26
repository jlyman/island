# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1408477502.127008
_enable_loop = True
_template_filename = '/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/templates/detail.html'
_template_uri = 'detail.html'
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
    return runtime._inherit_from(context, 'base.htm', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def content():
            return render_content(context._locals(__M_locals))
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
        def content():
            return render_content(context)
        __M_writer = context.writer()
        __M_writer('\n  <br/>\n  <div class="container">\n    <div class="jumbotron" style="padding-top: 10px; padding-bottom: 10px;">\n      <h2>Resume</h2>\n      <div style="float: right;"><img src="/static/homepage/media/image/task/task_1.png" height="200px"/></div>\n      <p class="lead" style="text-align: left; font-size: 12pt;">\n        <b>Expiration Time: </b>#att<br/><br/>\n        <b>Points: </b>100pts<br/><br/>\n        <b>Description: </b>orem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. <br/><br/>\n      </p>\n      <a class="btn btn-lg btn-success" id="start" role="button">START</a>\n    </div>\n  </div>\n  \n  <div id="detail_instructions">\n  </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "detail.html", "line_map": {"35": 1, "52": 3, "40": 21, "58": 52, "28": 0, "46": 3}, "source_encoding": "ascii", "filename": "/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/templates/detail.html"}
__M_END_METADATA
"""
