# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1406569501.010795
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/templates/cover1.html'
_template_uri = 'cover1.html'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = []


from django_mako_plus.controller import static_files 

from django_mako_plus.controller import static_files 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        request = context.get('request', UNDEFINED)
        form = context.get('form', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n')
        static_renderer = static_files.StaticRenderer(self) 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['static_renderer'] if __M_key in __M_locals_builtin_stored]))
        __M_writer('\n\n<!DOCTYPE html>\n<html>\n  <meta charset="UTF-8">\n  <head>\n    \n    <title>Homepage</title>\n    \n')
        __M_writer('    <script src="/static/homepage/scripts/jQuery.js"></script>\n    <script src="/static/homepage/scripts/bootstrap.js"></script>\n\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/bootstrap.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/bootstrap-theme.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/dashboard.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/cover.css">\n  \n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_css(request, context)  ))
        __M_writer('\n  \n  </head>\n  <body>\n    <div class="site-wrapper">\n\n      <div class="site-wrapper-inner">\n\n        <div class="cover-container">\n\n          <div class="masthead clearfix">\n            <div class="inner">\n              <h3 class="masthead-brand">BYU Information Systems</h3>\n              <ul class="nav masthead-nav">\n                <li class="active"><a href="#">Home</a></li>\n                <li><a href="#">Features</a></li>\n                <li><a href="#">Contact</a></li>\n              </ul>\n            </div>\n          </div>\n\n          <div class="inner cover">\n\n            <h1 class="cover-heading">Welcome to ISLand</h1>\n              <form class="form-horizontal signin-form" method="POST" action="/homepage/cover1/">\n                ')
        __M_writer(str( form.non_field_errors() ))
        __M_writer('\n')
        for field in form:
            __M_writer('                  <div class="form-group">\n                    <label class="col-md-2 control-label">')
            __M_writer(str(field.label))
            __M_writer('</label>\n                    <div class="col-md-5">\n                      ')
            __M_writer(str(field))
            __M_writer(' \n                      <div class="form-constrol" style="padding-left: 0px">')
            __M_writer(str(field.errors))
            __M_writer('</div>\n                    </div>\n                  </div>\n')
        __M_writer('                <div class="form-group col-md-9"> \n                  <button type="submit" class="btn btn-lg btn-default lead">Sign In</button>\n                </div>\n              </form>\n            \n\n          </div>\n\n          <div class="mastfoot">\n            <div class="inner">\n              <p><a href="#hello">Terms and Conditions</a></p>\n            </div>\n          </div>\n\n        </div>\n\n      </div>\n\n    </div>\n\n')
        __M_writer('\n')
        __M_writer('    ')
        __M_writer('\n    ')
        static_renderer = static_files.StaticRenderer(self) 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['static_renderer'] if __M_key in __M_locals_builtin_stored]))
        __M_writer('\n  \n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_js(request, context)  ))
        __M_writer('\n  \n  </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "cover1.html", "filename": "/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/templates/cover1.html", "line_map": {"67": 61, "17": 4, "19": 82, "21": 0, "29": 2, "30": 4, "31": 5, "35": 5, "36": 15, "37": 24, "38": 24, "39": 24, "40": 49, "41": 49, "42": 50, "43": 51, "44": 52, "45": 52, "46": 54, "47": 54, "48": 55, "49": 55, "50": 59, "51": 80, "52": 82, "53": 82, "54": 83, "58": 83, "59": 86, "60": 86, "61": 86}, "source_encoding": "ascii"}
__M_END_METADATA
"""
