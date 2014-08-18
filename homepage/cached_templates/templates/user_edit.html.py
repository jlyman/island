# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1405363482.291226
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/templates/user_edit.html'
_template_uri = 'user_edit.html'
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
        __M_writer('\n  <div class="container">\n    <br/>\n    <div class="jumbotron" style="padding-top: 10px; padding-bottom: 10px;">\n      <h2>Edit Information</h2>\n      <br/>\n      <form class="form-horizontal" role="form">\n        <div class="form-group">\n          <label for="inputEmail3" class="col-sm-3 control-label">Email</label>\n          <div class="col-sm-9">\n            <input type="email" class="form-control" id="inputEmail3" placeholder="Email">\n          </div>\n        </div>\n        <div class="form-group">\n            <label for="inputPassword3" class="col-sm-3 control-label">Password</label>\n          <div class="col-sm-9">\n            <input type="password" class="form-control" id="inputPassword3" placeholder="Password">\n          </div>\n        </div>\n        <br/>\n        <div class="form-group">\n          <div class="col-sm-12">\n            <button type="submit" class="btn btn-default">Sign in</button>\n          </div>\n        </div>\n      </form>\n    </div>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/templates/user_edit.html", "source_encoding": "ascii", "uri": "user_edit.html", "line_map": {"35": 1, "52": 3, "40": 31, "58": 52, "28": 0, "46": 3}}
__M_END_METADATA
"""
