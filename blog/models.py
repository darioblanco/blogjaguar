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

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import ugettext as _
from darioblog.settings import LANGUAGES



# Class for implementing the Dojo WYSIWYG Editor in the admin panel
class CommonMedia:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    'js/editor.js',
  )
  css = {
    'all': ('css/editor.css',),
  }


################
# Model classes
################

class Category(models.Model):
    lang = models.CharField(max_length=2, choices=LANGUAGES)
    title = models.CharField(max_length=100)
    desc = models.TextField()

    def __unicode__(self):
        return _(self.title)
    
    class Meta:
        verbose_name_plural = _("Categories")


class Entry(models.Model):
    lang = models.CharField(max_length=2, choices=LANGUAGES)
    author = models.ForeignKey(User)
    cat = models.ManyToManyField(Category)  # A post can have many categories
    title = models.CharField(max_length=100)
    post = models.TextField()
    date = models.DateTimeField()
    mod_date = models.DateTimeField(null = True)
    published = models.BooleanField()
    rate = models.IntegerField(null = True)

    def __unicode__(self):
        return self.title

    # Gives a preview of the entire text
    def preview(self):
        if len(self.post) > 1000 :
            return self.post[0:1000] + '  [...]'
        else :
            return self.post

    class Meta:
        ordering = ["date"]
        verbose_name_plural = _("Entries")


class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    author = models.ForeignKey(User)
    text = models.TextField()
    date = models.DateTimeField()
    num = models.IntegerField()
    quote = models.IntegerField(null = True)
    rate = models.IntegerField(null = True)

    def __unicode__(self):
        return _(self.entry.title)


class Votes(models.Model):
    user = models.ForeignKey(User)
    positive = models.BooleanField() # If positive = True => +1, if not => -1


class CommentVotes(Votes):
    comment = models.ForeignKey(Comment)

    class Meta:
        ordering = ["comment"]
        verbose_name_plural = _("CommentVotes")


class EntryVotes(Votes):
    entry = models.ForeignKey(Entry)

    class Meta:
        ordering = ["entry"]
        verbose_name_plural = _("EntryVotes")


class Link(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name


##################################
# For editing the admin interface
##################################

class BlogPostAdmin(admin.ModelAdmin):
    #fields = ('title', 'post', 'lang', 'author', 'cat', 'date') # Fields to display
    list_display = ('title', 'author', 'date', 'lang', 'published')
    Media = CommonMedia # For Dojo Rich Text Editor

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'lang')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry', 'author', 'text')

class EntryVotesAdmin(admin.ModelAdmin):
    list_display = ('entry', 'user', 'positive')

class CommentVotesAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'positive')

class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order')
    

admin.site.register(Entry, BlogPostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(EntryVotes, EntryVotesAdmin)
admin.site.register(CommentVotes, CommentVotesAdmin)
admin.site.register(Link, LinkAdmin)


