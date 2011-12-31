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

from django.conf.urls.defaults import *
from blog.models import Entry

urlpatterns = patterns('blog.views',
    url(r'^post(?P<post_id>\d+)/$', 'single_entry_view', name="singlepost"),
    url(r'^cat(?P<cat_id>\d+)/$', 'single_category_view', name="category_entries"),
    url(r'^page(?P<page_id>\d+)/$', 'blog_entries_view', name="blogpage"),
    url(r'^archives/', 'archive_view', name="archives"),
    url(r'^archives-(?P<year_id>\d+)/$', 'archive_year_request', name="year_archives"),
    url(r'^archives-(?P<month_id>\d+)-(?P<year_id>\d+)/$', 'archive_month_request', name="month_archives"),
    url(r'^post(?P<post_id>\d+)/comment_(?P<user_id>\w+)/$', 'comment_entry_request', name="comment_entry"),
    url(r'^post(?P<post_id>\d+)/entryrate-(?P<user_id>\d+)/$', 'rate_entry_request', name="rate_entry"),
    url(r'^post(?P<post_id>\d+)/commentrate-(?P<comment_id>\d+)-(?P<user_id>\d+)/$',
        'rate_comment_request', name="rate_comment"),
)
