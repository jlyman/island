# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1405971676.443423
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/templates/index.html'
_template_uri = 'index.html'
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
        tasks = context.get('tasks', UNDEFINED)
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
        tasks = context.get('tasks', UNDEFINED)
        def content():
            return render_content(context)
        __M_writer = context.writer()
        __M_writer('\n  <div id="image-container">\n    <ul id="tiles">\n\n')
        for task in tasks:
            __M_writer('        <li class="img-li"><a href="/homepage/detail/')
            __M_writer(str(task.id))
            __M_writer('">\n          <h2 style="text-align: center;">')
            __M_writer(str(task.name))
            __M_writer('</h2>\n          <img src="/static/homepage/media/image/task/task_')
            __M_writer(str(task.id))
            __M_writer('.png" width="210px" height="210px"/></a>\n          <div class="thumbnail-info"> \n            Desc: ')
            __M_writer(str(task.description))
            __M_writer('<br/>\n            Points: ')
            __M_writer(str(task.points))
            __M_writer('<br/>\n          </div>\n        </li>\n')
        __M_writer('\n    </ul>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"64": 12, "65": 13, "66": 13, "67": 17, "36": 1, "41": 20, "73": 67, "47": 3, "60": 9, "54": 3, "55": 7, "56": 8, "57": 8, "58": 8, "59": 9, "28": 0, "61": 10, "62": 10, "63": 12}, "uri": "index.html", "filename": "/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/templates/index.html"}
__M_END_METADATA
"""
