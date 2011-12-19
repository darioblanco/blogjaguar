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

from django import forms
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

class SubmitCommentForm(forms.Form):
    message = forms.CharField(min_length=10, max_length=400)


# If you want to include TinyMCE
#
#class FlatPageForm(forms.ModelForm):
#    title = forms.CharField(max_length = 100)
#    #content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
#    categories = forms.SelectMultiple()
#    lang = forms.Select()
#
#    class Meta:
#        model = FlatPage
#
#    class Media:
#        js = ('js/tiny_mce/tiny_mce.js',
#              'js/tiny_mce/textareas.js',)
#
#
#
#class FlatPageAdmin(FlatPageAdminOld):
#    class Media:
#        js = ('js/tiny_mce/tiny_mce.js',
#              'js/tiny_mce/textareas.js',)
#
## We have to unregister it, and then reregister
#admin.site.unregister(FlatPage)
#admin.site.register(FlatPage, FlatPageAdmin)