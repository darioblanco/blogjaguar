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

import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse

from blog.models import Entry, Link, Comment, EntryVotes, CommentVotes, AboutMe
from blog.blogpage import BlogPage
from blog.votes import Votes
from blog.categorylister import CategoryLister
from blog.forms import SubmitCommentForm

# TODO: generic views
# (https://docs.djangoproject.com/en/1.3/topics/class-based-views/)


################
# Own template generators
################


def _staticpage_template_gen(request, template_path):
    """Generates simple templates."""
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template(template_path)

    c = RequestContext(request, {
        'cat_list': cl.get_categories(),
        'link_list': Link.objects.all().order_by('order'),
    })

    return t.render(c)


def _entrypage_template_gen(request, template_path, entry_list):
    """Generates templates related to entries list."""
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template(template_path)

    paginator = Paginator(entry_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        blog_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blog_list = paginator.page(paginator.num_pages)

    c = RequestContext(request, {
        'cat_list': cl.get_categories(),
        'blog_list': blog_list,
        'link_list': Link.objects.all().order_by('order'),
    })

    return t.render(c)


def _singleentry_template_gen(request, template_path, entry, comment_list,
                              form):
    """Generates templates related to a single entry."""
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template(template_path)

    template_datadict = {
        'cat_list': cl.get_categories(),
        'entry': entry,
        'link_list': Link.objects.all().order_by('order'),
        'comments': comment_list,
    }

    if form is not None:  # If form is needed, it adds it
        template_datadict[form] = form

    c = RequestContext(request, template_datadict)

    return t.render(c)


def _archivepage_template_gen(request, template_path, entry_list):
    """Generates templates related to entries archives."""
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template(template_path)

    paginator = Paginator(entry_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        blog_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blog_list = paginator.page(paginator.num_pages)

    c = RequestContext(request, {
        'cat_list': cl.get_categories(),
        'blog_list': blog_list,
        'link_list': Link.objects.all().order_by('order'),
    })

    return t.render(c)


################
# Views
################


def blog_entries_view(request):
    """Entries list by page (0 is the first and more recent page)"""
    return HttpResponse(
        _entrypage_template_gen(
            request, 'blog/main.html',
            Entry.objects.filter(
                lang=request.LANGUAGE_CODE,
                published=True).order_by('-date')))


def single_entry_view(request, post_id):
    """Single entry details: entire text and comments"""
    return HttpResponse(
        _singleentry_template_gen(
            request, 'blog/singlepost.html',
            Entry.objects.get(id=post_id),
            Comment.objects.filter(entry=post_id), None))


def single_category_view(request, cat_id):
    """Entries list of a single category"""
    return HttpResponse(
        _entrypage_template_gen(
            request, 'blog/main.html',
            Entry.objects.filter(
                lang=request.LANGUAGE_CODE,
                cat__id=cat_id,
                published=True).order_by('-date')))


def blog_category_view(request):
    """The entire blog category list with its description per category"""
    return HttpResponse(_staticpage_template_gen(
        request, 'blog/categories.html'))


def aboutme_view(request):
    """About me static page"""
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/aboutme.html')

    c = RequestContext(request, {
        'cat_list': cl.get_categories(),
        'link_list': Link.objects.all().order_by('order'),
        'about_text': AboutMe.objects.all()[0]
    })

    return HttpResponse(t.render(c))


def privacy_view(request):
    """Static page which expands the privacy policy"""
    return HttpResponse(_staticpage_template_gen(
        request, 'blog/privacy.html'))


def logout_request(request):
    """Login out with an user. When completed, redirects to the index page
    (blog list page 0)
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def archive_view(request):
    """List of year and months with the number of entries related.
    """
    bp = BlogPage(request.LANGUAGE_CODE)
    return HttpResponse(_archivepage_template_gen(
        request, 'blog/archives.html', bp.archived_years()))


def archive_year_request(request, year_id):
    """List of entries related to a specific year"""
    bp = BlogPage(request.LANGUAGE_CODE)
    return HttpResponse(_archivepage_template_gen(
        request, 'blog/main.html', bp.posts_year(year_id)))


def archive_month_request(request, month_id, year_id):
    """List of entries related to a specific year and month"""
    bp = BlogPage(request.LANGUAGE_CODE)
    return HttpResponse(_archivepage_template_gen(
        request, 'blog/main.html', bp.posts_month(month_id, year_id)))


def comment_entry_request(request, post_id, user_id):
    """Triggered when a user inserts a comment in an specific entry"""
    bp = Entry.objects.get(id=post_id)
    # Form management
    if request.method == 'POST':  # If the form has been submitted...
        form = SubmitCommentForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            comment = Comment(entry=bp,
                              author=User.objects.get(id=user_id),
                              text=request.POST['message'],
                              date=datetime.datetime.now(),
                              num=Comment.objects.filter(
                                  entry=post_id).count() + 1,
                              quote=0)

            comment.save()

            return HttpResponseRedirect(reverse("singlepost", args=(post_id,)))
    else:
        form = SubmitCommentForm()  # An unbound form

    return HttpResponse(
        _singleentry_template_gen(
            request, 'blog/singlepost.html',
            Entry.objects.get(id=post_id),
            Comment.objects.filter(entry=post_id), form))


def rate_entry_request(request, post_id, user_id):
    """Triggered when a user rates a specific entry"""
    entry = Entry.objects.get(id=post_id)
    user = User.objects.get(id=user_id)
    positive = True

    if request.POST['like']:
        positive = True
    else:
        positive = False

    v = Votes()
    if v.validate_entry_vote(user_id, post_id):
        vote = EntryVotes(entry=entry,
                          user=user,
                          positive=positive)
        vote.save()
        v.set_entry_rate(post_id)

    return HttpResponseRedirect(reverse("singlepost", args=(post_id,)))


def rate_comment_request(request, post_id, comment_id, user_id):
    """Triggered when an user rates a specific comment
    from a specific entry
    """
    comment = Comment.objects.get(id=comment_id)
    user = User.objects.get(id=user_id)
    positive = True

    if request.POST['like']:
        positive = True
    else:
        positive = False

    v = Votes()
    if v.validate_comment_vote(user_id, comment_id):
        vote = CommentVotes(comment=comment,
                            user=user,
                            positive=positive)
        vote.save()
        v.set_comment_rate(comment_id)

    return HttpResponseRedirect(reverse("singlepost", args=(post_id,)))
