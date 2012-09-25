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

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blog.models import Entry
from settings import SITE_URL


class LatestEntriesFeed(Feed):
    """ Creates a RSS feed of the latest blog posts"""

    title = "The soft jaguar"
    link = "/siteentries/"
    description = "Blog RSS Feed"

    def items(self):
        return Entry.objects.filter(published=True).order_by('-date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.post[0:200]

    def item_link(self, item):
        return SITE_URL + reverse(
            'blog.views.single_entry_view', args=(item.id,))
