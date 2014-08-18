# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1406795484.567977
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/theCproject/homepage/templates/base.htm'
_template_uri = 'base.htm'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = ['content']


from django_mako_plus.controller import static_files 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n')
        static_renderer = static_files.StaticRenderer(self) 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['static_renderer'] if __M_key in __M_locals_builtin_stored]))
        __M_writer('\n\n<!DOCTYPE html>\n<html>\n  <meta charset="UTF-8">\n  <head>\n    \n    <title>Homepage</title>\n    \n')
        __M_writer('    <script src="/static/homepage/scripts/jQuery.js"></script>\n    <script src="/static/homepage/scripts/bootstrap.js"></script>\n    <script src="/static/homepage/scripts/jquery.woomark.js"></script>\n    \n    <script src="/static/homepage/scripts/jquery.classysocial.min.js"></script>\n    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>\n    <script src="/static/homepage/scripts/custom.js"></script>\n\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/bootstrap.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/bootstrap-theme.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/dashboard.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/top-menu.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/jquery.classysocial.min.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/custom.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/profile1/custom.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/font-awesome-4.1.0/css/font-awesome.min.css">\n    \n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_css(request, context)  ))
        __M_writer('\n  \n  </head>\n  <body>\n\n    <div id="main_content">\n      <nav>\n        <ul class="menu">\n          <li style="padding-top: 3px; text-align: center; background-color: white;"><img src="/static/homepage/media/image/task/logo.png" width="90%" height="100%" /></li>\n          <li class="home current"><a href="/homepage/index/"><span>Home</span></a></li>\n          <li><a href="#"><span>About</span></a></li>\n          <li><a href="#"><span>Service</span></a>\n            <ul class="sub-menu">\n              <li><a href="#">Sub-menu 1</a></li>\n              <li><a href="#">Sub-menu 2</a></li>\n              <li><a href="#">Sub-menu 3</a></li>\n            </ul>\n          </li>\n          <li><a href="#"><span>Application Form</span></a></li>\n          <li><a href="#"><span>Contacts</span></a></li>\n        </ul>\n      </nav>\n      <form class="navbar-form" role="search" style="width: 40%; float: right;">\n        <div class="input-group">\n            <input type="text" class="form-control" placeholder="Search" name="srch-term" id="srch-term">\n            <div class="input-group-btn">\n                <button class="btn btn-default" type="submit"><i class="glyphicon glyphicon-search"></i></button>\n            </div>\n        </div>\n      </form>\n\n      <br/>\n      <br/>\n      ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer('  \n      <br/>\n      <br/>\n      <div id="footer">\n        <div class="container">\n          <p class="text-muted">BYU Department of Information Systems</p>\n        </div>\n      </div>\n    </div>\n    \n    <div id="right_bar">\n')
        if request.user.is_authenticated():
            __M_writer('        <header style="height: 115px;">\n            <img src="/static/homepage/media/image/ironman.jpeg" height="40px"/>\n            <div class="btn btn-default" style="text-align: left; cursor: initial;">\n              ')
            __M_writer(str(request.user.username))
            __M_writer('\n              <br/>\n              <a href="/homepage/profile/">View Profile</a>\n              <br/>\n              <a href="/homepage/cover1/logout">Logout</a>\n            </div>\n        </header>\n')
        __M_writer('      <div style="background-color: #3E454D; border-top: 1px solid #ffffff;">\n        <br/>\n        <ul class="nav nav-sidebar">\n          <li style="text-align: center;"><a href="#">Job Postings</a></li>\n          <li><a href="#">Senior graphical engineer</a></li>\n          <li><a href="#">Django junior developer</a></li>\n          <li><a href="#">Java project manager</a></li>\n        </ul>\n        <ul class="nav nav-sidebar">\n          <li style="text-align: center;"><a href="">Hot Topics</a></li>\n          <li><a href="">How to navigate to django setting?</a></li>\n          <li><a href="">Does bitcoin shape the currency future?</a></li>\n          <li><a href="">Why do we code?</a></li>\n          <li><a href="">Tips and tricks for Twitter Bootstrap 3.0</a></li>\n        </ul>\n      </div>\n\n      <div class="classysocial"  style="position:absolute; bottom: 0px; left: 10%;"\n        data-orientation="line" \n        data-arc-length="360" data-image-type="picture" \n        data-picture="/static/homepage/media/image/classysocial/default/share_core_square.jpg" data-facebook-handle="picozu" \n        data-twitter-handle="picozu_editor" \n        data-email-handle="me@me.com"\n        data-networks="facebook,twitter,email">\n      </div>\n    </div>\n  \n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_js(request, context)  ))
        __M_writer('\n  \n  </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        __M_writer = context.writer()
        __M_writer('\n        Site content goes here in sub-templates.\n      ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "base.htm", "source_encoding": "ascii", "line_map": {"69": 63, "17": 4, "19": 0, "28": 2, "29": 4, "30": 5, "34": 5, "35": 15, "36": 33, "37": 33, "38": 33, "43": 68, "44": 79, "45": 80, "46": 83, "47": 83, "48": 91, "49": 119, "50": 119, "51": 119, "57": 66, "63": 66}, "filename": "/Users/thongpham/Desktop/theCproject/homepage/templates/base.htm"}
__M_END_METADATA
"""
