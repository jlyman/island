from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Admin site
    url(r'^admin/', include(admin.site.urls)),

   # CAS (see django_cas_ng)
   url(r'^homepage/login.*$', 'django_cas_ng.views.login'),
   url(r'^homepage/logout.*$', 'django_cas_ng.views.logout'),
   
   # the django_mako_plus controller handles every request - this line is the glue that connects Mako to Django
   url(r'^.*$', 'django_mako_plus.controller.router.route_request' ),
   
)
