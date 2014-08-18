# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1408134291.774883
_enable_loop = True
_template_filename = '/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/templates/cover.html'
_template_uri = 'cover.html'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = []


from django_mako_plus.controller import static_files 

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\n')
        __M_writer('\n')
        static_renderer = static_files.StaticRenderer(self) 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['static_renderer'] if __M_key in __M_locals_builtin_stored]))
        __M_writer('\n\n<!DOCTYPE html>\n<html>\n  <meta charset="UTF-8">\n  <head>\n    \n    <title>Homepage</title>\n    \n')
        __M_writer('    <script src="/static/homepage/scripts/jQuery.js"></script>\n    <script src="/static/homepage/scripts/bootstrap.js"></script>\n    <script src="/static/homepage/superslider_resource/jquery.easing.1.3.js"></script>\n    <script src="/static/homepage/superslider_resource/jquery.animate-enhanced.min.js"></script>\n    <script src="/static/homepage/superslider_resource/hammer.min.js"></script>\n    <script src="/static/homepage/superslider_resource/jquery.superslides.js"></script>\n    <script src="/static/homepage/superslider_resource/application.js"></script>\n\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/bootstrap.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/bootstrap-theme.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/dashboard.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/custom.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/cover.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/superslider_resource/superslides.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/superslider_resource/normalize.css">\n    <link rel="stylesheet" type="text/css" href="/static/homepage/superslider_resource/layout.css">\n  \n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_css(request, context)  ))
        __M_writer('\n  \n  </head>\n  <body>\n\n  <div class="loading-container">\n    <div class="pulse"></div>\n  </div>\n\n  <div id="slides">\n    <ul class="slides-container">\n      <li>\n        <img src="/static/homepage/superslider_resource/people.jpeg" alt="">\n        <div class="container">\n          <h1>Superslides is a fullscreen slider for jQuery.</h1>\n          <p>\n          </p>\n        </div>\n      </li>\n      <li>\n        <img src="/static/homepage/superslider_resource/people.jpeg" alt="">\n        <div class="container">\n          <h1>It\'s responsive.</h1>\n          <div class="contrast">\n            <p>\n              Images are smartly centered in the viewport. Use your own media queries to control the layout of your content.\n            </p>\n          </div>\n        </div>\n      </li>\n      <li>\n        <img src="/static/homepage/superslider_resource/people.jpeg" alt="">\n        <div class="container">\n          <h1>It\'s hardware accelerated.</h1>\n          <div class="contrast">\n            <p>For browsers that support CSS hardware acceleration, tasks, such as animation, are processed by the GPU giving massive performance gains.</p>\n          </div>\n        </div>\n      </li>\n      <li>\n        <img src="/static/homepage/superslider_resource/people.jpeg" alt="">\n        <div class="container">\n          <h1>It\'s got a pretty sweet API.</h1>\n          <div class="contrast">\n            <p>The control API lets you start, stop, animate, and destroy instances of the slider. You can get the current, next, and previous slides programmatically. In fact, the slider uses the same API internally.</p>\n          </div>\n        </div>\n      </li>\n      <li>\n        <img src="/static/homepage/superslider_resource/people.jpeg" alt="">\n        <div class="container">\n          <h1>It\'s tested with QUnit.</h1>\n          <div class="contrast">\n            <p>\n              Version 0.5 was a ground up, TDD rebuild, fixing many quirky bugs and standardizing the event and control APIs.\n            </p>\n          </div>\n        </div>\n      </li>\n      <li>\n        <img src="/static/homepage/superslider_resource/people.jpeg" alt="">\n        <div class="container">\n          <h1>It\'s got popular buzzwords.</h1>\n          <div class="contrast">\n            <p>\n              Thanks for viewing! Read the docs, create an issue, or fix a bug on <a href="https://github.com/nicinabox/superslides/issues">Github</a>.\n            </p>\n            <p>\n              <a href="http://twitter.com/nicinabox">@nicinabox</a> made this. All these photos are by the amazing <a href="http://www.flickr.com/photos/x30mileswest/">Ryan Green</a>.\n            </p>\n          </div>\n        </div>\n      </li>\n    </ul>\n    <nav class="slides-navigation">\n      <a href="#" class="next">\n        <i class="icon-chevron-right"></i>\n      </a>\n      <a href="#" class="prev">\n        <i class="icon-chevron-left"></i>\n      </a>\n    </nav>\n  </div>\n  \n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_js(request, context)  ))
        __M_writer('\n  \n  </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "/Users/thongapham/Desktop/Aug_8_2014Mac/theCproject/homepage/templates/cover.html", "line_map": {"32": 5, "33": 15, "34": 33, "35": 33, "36": 33, "37": 118, "38": 118, "39": 118, "45": 39, "17": 4, "19": 0, "26": 2, "27": 4, "28": 5}, "uri": "cover.html", "source_encoding": "ascii"}
__M_END_METADATA
"""
