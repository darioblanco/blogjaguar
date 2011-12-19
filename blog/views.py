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
from darioblog.blog.models import Entry, Link, Comment, EntryVotes, CommentVotes
from darioblog.blog.blogpage import BlogPage
from darioblog.blog.votes import Votes
from darioblog.blog.categorylister import CategoryLister
from darioblog.blog.forms import SubmitCommentForm
from django.core.urlresolvers import reverse


# Post list by page
def bloglist_view(request, page_id):
    bp = BlogPage(request.LANGUAGE_CODE)
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/blog_view.html')

    nav_list = bp.getNavList(page_id)

    if not nav_list :
        return HttpResponse("FAIL")
    else :
        c = RequestContext(request, {
            'cat_list' : cl.getCategories(),
            'blog_list': bp.postsPage(page_id),
            'nav_list' : nav_list,
            'page' : int(page_id),
            'link_list' : Link.objects.all().order_by('order'),
        })

        return HttpResponse(t.render(c))


# Single post details: entire text and comments
def singlepost(request, post_id):
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/blog_singlepost.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'entry': Entry.objects.get(id = post_id),
        'link_list' : Link.objects.all().order_by('order'),
        'comments' : Comment.objects.filter(entry = post_id),
    })

    return HttpResponse(t.render(c))

# Post list of a single category
def category(request, cat_id):
    bp = BlogPage(request.LANGUAGE_CODE)
    cl = CategoryLister(request.LANGUAGE_CODE)
        
    t = loader.get_template('blog/blog_view.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'blog_list': Entry.objects.filter(cat__id = cat_id),
        'nav_list' : bp.getNavList(0),
        'page' : 0,
        'link_list' : Link.objects.all().order_by('order'),
    })

    return HttpResponse(t.render(c))

# Category list with its description
def catlist(request):
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/category_view.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'link_list' : Link.objects.all().order_by('order'),
    })

    return HttpResponse(t.render(c))

# Static page which explains
def aboutme(request):
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/aboutme_view.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'link_list' : Link.objects.all().order_by('order'),
    })

    return HttpResponse(t.render(c))


# Login out a user
def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))

#
def archive_view(request) :
    bp = BlogPage(request.LANGUAGE_CODE)
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/archives_view.html')

    c = RequestContext(request, {
        'cat_list'  : cl.getCategories(),                    # Alphabetic order
        'year_list' : bp.archivedYears(),                    # Year list
        'link_list' : Link.objects.all().order_by('order'), # Priority order
    })

    return HttpResponse(t.render(c))

#
def archive_year_request(request, year_id) :
    bp = BlogPage(request.LANGUAGE_CODE)
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/blog_view.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'blog_list': bp.postsYear(year_id),
        'link_list' : Link.objects.all().order_by('order'),
    })

    return HttpResponse(t.render(c))

#
def archive_month_request(request, month_id, year_id) :
    bp = BlogPage(request.LANGUAGE_CODE)
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/blog_view.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'blog_list': bp.postsMonth(month_id, year_id),
        'link_list' : Link.objects.all().order_by('order'),
    })

    return HttpResponse(t.render(c))


# Static page which expands the privacy policy
def privacy_policy(request):
    cl = CategoryLister(request.LANGUAGE_CODE)

    t = loader.get_template('blog/privacy_view.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'link_list' : Link.objects.all().order_by('order'),
    })

    return HttpResponse(t.render(c))

#
def comment_entry(request, post_id, user_id):
    bp = Entry.objects.get(id = post_id)

    if request.method == 'POST': # If the form has been submitted...
        form = SubmitCommentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            comment = Comment(
                                entry = bp,
                                author = User.objects.get(id = user_id),
                                text = request.POST['message'],
                                date = datetime.datetime.now(),
                                num = Comment.objects.filter(entry = post_id).count() + 1,
                                quote = 0
                              )

            comment.save()

            return HttpResponseRedirect(reverse("singlepost", args=(post_id,))) # Redirect after POST
    else:
        form = SubmitCommentForm() # An unbound form

    cl = CategoryLister(request.LANGUAGE_CODE)
    t = loader.get_template('blog/blog_singlepost.html')

    c = RequestContext(request, {
        'cat_list' : cl.getCategories(),
        'entry': Entry.objects.get(id = post_id),
        'link_list' : Link.objects.all().order_by('order'),
        'comments' : Comment.objects.filter(entry = post_id),
        'form' : form,
    })

    return HttpResponse(t.render(c))

#
def rate_entry(request, post_id, user_id):
    entry = Entry.objects.get(id = post_id)
    user = User.objects.get(id = user_id)
    positive = True

    if request.POST['like']:
        positive = True
    else :
        positive = False

    v = Votes()
    if v.validateEntryVote(user_id, post_id):
        vote = EntryVotes(
                        entry = entry,
                        user = user,
                        positive = positive,
        )
        vote.save()
        v.setEntryRate(post_id)

    return HttpResponseRedirect(reverse("singlepost", args=(post_id,))) # Redirect after POST

#
def rate_comment(request, post_id, comment_id, user_id):
    comment = Comment.objects.get(id = comment_id)
    user = User.objects.get(id = user_id)
    positive = True

    if request.POST['like']:
        positive = True
    else:
        positive = False

    v = Votes()
    if v.validateCommentVote(user_id, comment_id) :
        vote = CommentVotes(
                        comment = comment,
                        user = user,
                        positive = positive,
        )
        vote.save()
        v.setCommentRate(comment_id)

    return HttpResponseRedirect(reverse("singlepost", args=(post_id,))) # Redirect after POST



#############################
# OTHER VIEWS THAT CAN BE USEFUL
#############################

#def search_request(request):
#    keywords = request.POST['keywords']
#
#    bp = BlogPage(request.LANGUAGE_CODE)
#    cl = CategoryLister(request.LANGUAGE_CODE)
#
#    t = loader.get_template('blog/blog_view.html')
#
#    c = RequestContext(request, {
#        'cat_list' : cl.getCategories(),
#        'blog_list': bp.postsSearch(keywords),
#        'nav_list' : bp.getNavList(0),
#        'page' : 0,
#        'link_list' : Link.objects.all().order_by('order'),
#    })
#
#    return HttpResponse(t.render(c))

## Static page with a login request
#def login_view(request):
#    cl = CategoryLister(request.LANGUAGE_CODE)
#
#    t = loader.get_template('blog/login_view.html')
#
#    username = request.POST['username']
#    password = request.POST['password']
#    user = authenticate(username=username, password=password)
#
#    usererror = False
#    if user is not None:
#        if user.is_active:
#            login(request, user)
#            # Redirect to a success page
#            message = _('Login successful')
#        else:
#            # Return a disabled account message
#            usererror = True
#            message = _('The account is disabled ')
#    else :
#        # Return an invalid login error message
#        usererror = True
#        message = _('Invalid username and/or password')
#
#
#    c = RequestContext(request, {
#        'cat_list' : cl.getCategories(),
#        'link_list' : Link.objects.all().order_by('order'),
#        'usererror' : usererror,
#        'username' : username,
#        'message' : message,
#    })
#
#    return HttpResponse(t.render(c))


## Static page with a register request
#def register_view(request):
#    cl = CategoryLister(request.LANGUAGE_CODE)
#
#    t = loader.get_template('blog/register_view.html')
#
#    c = RequestContext(request, {
#        'cat_list' : cl.getCategories(),
#        'link_list' : Link.objects.all().order_by('order'),
#        'reg_pending' : False,
#    })
#
#    return HttpResponse(t.render(c))

#def register_request(request):
#    cl = CategoryLister(request.LANGUAGE_CODE)
#
#    user = User.objects.create_user(request.POST['username'],
#                                    request.POST['email'],
#                                    request.POST['password'])
#
#    user.save()
#
#    t = loader.get_template('blog/register_view.html')
#
#    c = RequestContext(request, {
#        'cat_list' : cl.getCategories(),
#        'link_list' : Link.objects.all().order_by('order'),
#        'reg_pending' : True,
#    })
#
#    return HttpResponse(t.render(c))

# Login complete view, displays user data
#@login_required
#def done(request):
#    cl = CategoryLister(request.LANGUAGE_CODE)
#
#    t = loader.get_template('blog/login_view.html')
#
#    c = RequestContext(request, {
#        'cat_list' : cl.getCategories(),
#        'link_list' : Link.objects.all().order_by('order'),
#        'version': version,
#        'last_login': request.session.get('social_auth_last_login_backend')
#    })
#
#    return HttpResponse(t.render(c))