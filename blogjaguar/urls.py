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

from blog.rssfeeder import LatestEntriesFeed
from blogjaguar.settings import DEBUG, STATIC_ROOT, MEDIA_ROOT


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'blog.views.blog_entries_view', name="index"),
    (r'^blog/', include('blog.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),  # Multilanguage
    url(r'^feed/$', LatestEntriesFeed(), name="feed"),
    url(r'^facebook/login/$', 'facebook.views.login', name="facebook_login"),
    url(r'^facebook/authentication_callback/$',
        'facebook.views.authentication_callback', name="facebook_callback"),
    url(r'^admin/', include(admin.site.urls), name="admin"),
)

urlpatterns += patterns(
    'blog.views',
    url(r'^categories/', 'blog_category_view', name="categories"),
    url(r'^about/', 'aboutme_view', name="about"),
    url(r'^privacy_policy/', 'privacy_view', name="privacy_policy"),
    url(r'^logout/', 'logout_request', name="logout"),
)

# static urls will be disabled in production mode,
# forcing user to configure httpd
if DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^static/(.*)$', 'django.views.static.serve',
            {'document_root': STATIC_ROOT,
             'show_indexes': True}),
        url(r'^media/(.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT,
             'show_indexes': True}),
        url(r'^admin-media/(.*)$', 'django.views.static.serve',
            {'document_root': join(dirname(admin.__file__), 'media')}),
    )
