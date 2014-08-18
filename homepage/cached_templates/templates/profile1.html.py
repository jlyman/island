# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1406795300.699209
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/theCproject/homepage/templates/profile1.html'
_template_uri = 'profile1.html'
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
        __M_writer('\n  <div id="page-inner">\n\n    <div class="row">\n      <div class="col-md-12">\n        <h2>Admin Dashboard</h2>   \n        <h5>Welcome Jhon Deo , Love to see you back. </h5>\n      </div>\n    </div>              \n    <!-- /. ROW  -->\n\n    <hr />\n\n    <div class="row">\n      <div class="col-md-3 col-sm-6 col-xs-6">           \n        <div class="panel panel-back noti-box">\n          <span class="icon-box bg-color-red set-icon">\n            <i class="fa fa-envelope-o"></i>\n          </span>\n          <div class="text-box" >\n            <p class="main-text">120 New</p>\n            <p class="text-muted">Messages</p>\n          </div>\n        </div>\n      </div>\n      <div class="col-md-3 col-sm-6 col-xs-6">           \n        <div class="panel panel-back noti-box">\n          <span class="icon-box bg-color-green set-icon">\n            <i class="fa fa-bars"></i>\n          </span>\n          <div class="text-box" >\n            <p class="main-text">30 Tasks</p>\n            <p class="text-muted">Remaining</p>\n          </div>\n        </div>\n      </div>\n      <div class="col-md-3 col-sm-6 col-xs-6">           \n        <div class="panel panel-back noti-box">\n          <span class="icon-box bg-color-blue set-icon">\n            <i class="fa fa-bell-o"></i>\n          </span>\n          <div class="text-box" >\n            <p class="main-text">240 New</p>\n            <p class="text-muted">Notifications</p>\n          </div>\n        </div>\n      </div>\n      <div class="col-md-3 col-sm-6 col-xs-6">           \n        <div class="panel panel-back noti-box">\n          <span class="icon-box bg-color-brown set-icon">\n            <i class="fa fa-rocket"></i>\n          </span>\n          <div class="text-box" >\n            <p class="main-text">3 Orders</p>\n            <p class="text-muted">Pending</p>\n          </div>\n        </div>\n      </div>\n    </div>\n    <!-- /. ROW  -->\n\n    <hr />                \n\n    <div class="row">\n      <div class="col-md-6 col-sm-12 col-xs-12">           \n        <div class="panel panel-back noti-box">\n          <span class="icon-box bg-color-blue">\n            <i class="fa fa-warning"></i>\n          </span>\n          <div class="text-box" >\n            <p class="main-text">52 Important Issues to Fix </p>\n            <p class="text-muted">Please fix these issues to work smooth</p>\n            <p class="text-muted">Time Left: 30 mins</p>\n            <hr />\n            <p class="text-muted">\n            <span class="text-muted color-bottom-txt"><i class="fa fa-edit"></i>\n            Lorem ipsum dolor sit amet, consectetur adipiscing elit gthn. \n            Lorem ipsum dolor sit amet, consectetur adipiscing elit gthn. \n            </span>\n            </p>\n          </div>\n        </div>\n      </div>\n      <div class="col-md-3 col-sm-12 col-xs-12">\n        <div class="panel back-dash">\n          <i class="fa fa-dashboard fa-3x"></i><strong> &nbsp; SPEED</strong>\n          <p class="text-muted">Lorem ipsum dolor sit amet, consectetur adipiscing sit ametsit amet elit ftr. Lorem ipsum dolor sit amet, consectetur adipiscing elit. </p>\n        </div>\n      </div>\n      <div class="col-md-3 col-sm-12 col-xs-12 ">\n        <div class="panel ">\n          <div class="main-temp-back">\n            <div class="panel-body">\n              <div class="row">\n                <div class="col-xs-6"> <i class="fa fa-cloud fa-3x"></i> Newyork City </div>\n                <div class="col-xs-6">\n                  <div class="text-temp"> 10 </div>\n                </div>\n              </div>\n            </div>\n          </div>\n        </div>\n        <div class="panel panel-back noti-box">\n          <span class="icon-box bg-color-green set-icon">\n            <i class="fa fa-desktop"></i>\n          </span>\n          <div class="text-box" >\n            <p class="main-text">Display</p>\n            <p class="text-muted">Looking Good</p>\n          </div>\n        </div>\n      </div>\n    </div>\n    <!-- /. ROW  -->\n\n    <hr/>\n\n    <div class="row" >\n      <div class="col-md-3 col-sm-12 col-xs-12">\n        <div class="panel panel-primary text-center no-boder bg-color-green">\n          <div class="panel-body">\n            <i class="fa fa-comments-o fa-5x"></i>\n            <h4>200 New Comments </h4>\n            <h4>See All Comments  </h4>\n          </div>\n          <div class="panel-footer back-footer-green">\n            <i class="fa fa-rocket fa-5x"></i>\n            Lorem ipsum dolor sit amet sit sit, consectetur adipiscing elitsit sit gthn ipsum dolor sit amet ipsum dolor sit amet\n\n          </div>\n        </div>\n      </div>\n      <div class="col-md-9 col-sm-12 col-xs-12">\n        <div class="panel panel-default">\n          <div class="panel-heading">\n            Responsive Table Example\n          </div>\n          <div class="panel-body">\n            <div class="table-responsive">\n              <table class="table table-striped table-bordered table-hover">\n                <thead>\n                  <tr>\n                    <th>#</th>\n                    <th>First Name</th>\n                    <th>Last Name</th>\n                    <th>Username</th>\n                    <th>User No.</th>\n                  </tr>\n                </thead>\n                <tbody>\n                  <tr>\n                    <td>1</td>\n                    <td>Mark</td>\n                    <td>Otto</td>\n                    <td>@mdo</td>\n                    <td>100090</td>\n                  </tr>\n                  <tr>\n                    <td>2</td>\n                    <td>Jacob</td>\n                    <td>Thornton</td>\n                    <td>@fat</td>\n                    <td>100090</td>\n                  </tr>\n                  <tr>\n                    <td>3</td>\n                    <td>Larry</td>\n                    <td>the Bird</td>\n                    <td>@twitter</td>\n                    <td>100090</td>\n                  </tr>\n                  <tr>\n                    <td>1</td>\n                    <td>Mark</td>\n                    <td>Otto</td>\n                    <td>@mdo</td>\n                    <td>100090</td>\n                  </tr>\n                  <tr>\n                    <td>2</td>\n                    <td>Jacob</td>\n                    <td>Thornton</td>\n                    <td>@fat</td>\n                    <td>100090</td>\n                  </tr>\n                  <tr>\n                    <td>3</td>\n                    <td>Larry</td>\n                    <td>the Bird</td>\n                    <td>@twitter</td>\n                    <td>100090</td>\n                  </tr>\n                </tbody>\n              </table>\n            </div>\n          </div>\n        </div>\n      </div>\n    </div>\n    <!-- /. ROW  -->\n  </div>\n  \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "profile1.html", "source_encoding": "ascii", "line_map": {"51": 3, "35": 1, "28": 0, "45": 3, "57": 51}, "filename": "/Users/thongpham/Desktop/theCproject/homepage/templates/profile1.html"}
__M_END_METADATA
"""
