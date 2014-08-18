# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1406783749.016476
_enable_loop = True
_template_filename = '/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/scripts/location_service.jsm'
_template_uri = 'location_service.jsm'
_source_encoding = 'ascii'
import os, os.path, re
from decimal import Decimal
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('// Note: This example requires that you consent to location sharing when\n// prompted by your browser. If you see a blank space instead of the map, this\n// is probably because you have denied permission for location sharing.\n\n  var map;\n\n  function initialize() {\n    var mapOptions = {\n      zoom: 6\n    };\n    map = new google.maps.Map(document.getElementById(\'map-canvas\'),\n        mapOptions);\n\n    // Try HTML5 geolocation\n    if(navigator.geolocation) {\n      navigator.geolocation.getCurrentPosition(function(position) {\n        $.ajax({\n          type: "POST",\n          url: \'/homepage/location_service/\' + position.coords.latitude + \'/\' + position.coords.longitude,\n        });\n        var pos = new google.maps.LatLng(position.coords.latitude,\n                                         position.coords.longitude);\n\n        var infowindow = new google.maps.InfoWindow({\n          map: map,\n          position: pos,\n          content: \'You are here.\'\n        });\n\n        map.setCenter(pos);\n      }, function() {\n        handleNoGeolocation(true);\n      });\n    } else {\n      // Browser doesn\'t support Geolocation\n      handleNoGeolocation(false);\n    }\n  }\n\n  function handleNoGeolocation(errorFlag) {\n    if (errorFlag) {\n      var content = \'Error: The Geolocation service failed.\';\n    } else {\n      var content = \'Error: Your browser doesn\\\'t support geolocation.\';\n    }\n\n    var options = {\n      map: map,\n      position: new google.maps.LatLng(60, 105),\n      content: content\n    };\n\n    var infowindow = new google.maps.InfoWindow(options);\n    map.setCenter(options.position);\n  }\n\n  google.maps.event.addDomListener(window, \'load\', initialize);')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "/Users/thongpham/Desktop/Programming/Web/theCproject/homepage/scripts/location_service.jsm", "line_map": {"17": 0, "28": 22, "22": 1}, "source_encoding": "ascii", "uri": "location_service.jsm"}
__M_END_METADATA
"""
