#   Copyright 2011 Dario Blanco Iturriaga
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from os.path import join, dirname
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from darioblog import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'darioblog.blog.views.bloglist_view', {'page_id': 0}, name="index"),
    (r'^blog/', include('darioblog.blog.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')), # Multilanguage
    url(r'^categories/', 'darioblog.blog.views.catlist', name="categories"),
    url(r'^about/', 'darioblog.blog.views.aboutme', name="about"),
    url(r'^privacy_policy/', 'darioblog.blog.views.privacy_policy', name="privacy_policy"),
    url(r'^facebook/login/$', 'darioblog.facebook.views.login', name="facebook_login"),
    url(r'^facebook/authentication_callback/$', 'darioblog.facebook.views.authentication_callback', name="facebook_callback"),
    url(r'^logout/', 'darioblog.blog.views.logout_view', name="logout"),
    url(r'^admin/', include(admin.site.urls), name="admin"),
)


# static urls will be disabled in production mode,
# forcing user to configure httpd
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,
            'show_indexes' : True
            }),
        url(r'^static/(.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT,
             'show_indexes' : True
            }),
        url(r'^admin-media/(.*)$', 'django.views.static.serve',
            {'document_root': join(dirname(admin.__file__), 'media')}),
        )

