# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1406788183.512502
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/theCproject/homepage/templates/profile.html'
_template_uri = 'profile.html'
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
        

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        __M_writer = context.writer()
        __M_writer('\n  <div style="width: 800px; margin: 0 auto; padding: 120px 0 40px;">\n        <ul class="tabs" data-persist="true">\n            <li><a href="#view1">Lorem</a></li>\n            <li><a href="#view2">Using other templates</a></li>\n            <li><a href="#view3">Advanced</a></li>\n        </ul>\n        <div class="tabcontents">\n            <div id="view1">\n                <b>Lorem Issum</b>\n                <p>Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...</p>\n                \n            </div>\n            <div id="view2">\n                <b>Switch to other templates</b>\n                <p>Open this page with Notepad, and update the CSS link to:</P>\n                <p>template1 ~ 6.</p>                \n            </div>\n            <div id="view3">\n                <b>Advanced</b>\n                <p>We have an advanced version, <a href="http://www.menucool.com/jquery-tabs">McTabs - jQuery Tabs</a>, that is the most feature-rich Tabs.</p>\n                <ul>\n                    <li>Ajax content</li>\n                    <li>Smooth transitional effect</li>\n                    <li>Auto advance</li>\n                    <li>Bookmark support: select a tab via bookmark anchor</li>\n                    <li>URL support: a hash id in the URL can select a tab</li>\n                    <li>Select tabs by mouse over</li>\n                    <li>... and more</li>                    \n                </ul>\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "profile.html", "source_encoding": "ascii", "line_map": {"51": 3, "35": 1, "28": 0, "45": 3, "57": 51}, "filename": "/Users/thongpham/Desktop/theCproject/homepage/templates/profile.html"}
__M_END_METADATA
"""
