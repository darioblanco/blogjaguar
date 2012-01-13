from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blog.models import Entry
from settings import SITE_URL


class LatestEntriesFeed(Feed):
	title = "The soft jaguar"
	link = "/siteentries/"
	description = "Blog RSS Feed"
	
	def items(self):
		return Entry.objects.filter(published = True).order_by('-date');
		
	def item_title(self, item):
		return item.title
		
	def item_description(self, item):
		return item.post[0:200]
		
	def item_link(self, item):
		return SITE_URL+reverse('blog.views.single_entry_view', args=(item.id,))