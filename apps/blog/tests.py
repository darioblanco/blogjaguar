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

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import random
from datetime import timedelta, datetime
from random import randrange
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Entry, Link, Category
from blog.fixtures import BLOGPOST_CONTENTS, BLOGPOST_TITLES


class ContentTest(TestCase):

    def setUp(self):
        dc = DummyCreator()
        dc.create_all()

    # TODO Create further tests to verify the data created


class DummyCreator():
    """ Creates dummy categories, entries and links, for testing the blog in
    non production environment
    """

    def __create_category(self, lang, title, desc):
        cat = Category(lang=lang, title=title, desc=desc)

        cat.save()
        print(
            "Created category : {} | {} | {} | ".format(lang, title, desc))

        return cat

    def __create_entry(self, lang, author, cat, title, post, date):
        entry = Entry(lang=lang, author=author, title=title, post=post,
                      date=date, mod_date=date, published=True)

        entry.save()
        entry.cat.add(cat)

        print "Created entry : {} | {} | ".format(lang, title)

        return entry

    def __create_link(self, name, url, order):
        link = Link(name=name, url=url, order=order)

        link.save()
        print "Created link : {} | {}".format(name, url)

        return link

    def __random_date(self):
        # Random date between two date objects

        start = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
        end = datetime.strptime('1/1/2012 4:50 AM', '%m/%d/%Y %I:%M %p')

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def create_categories(self):
        self.__create_category('es', "Software", "Todo sobre software")
        self.__create_category('es', "Deportes", "Haced deporte")
        self.__create_category('en', "Software", "All about software")
        self.__create_category('en', "Sports", "Soccer or football?")

    def create_entries(self, num_entries):
        cat_id = 0
        loren_id = 0
        title_id = 0
        lang = 'es'
        user = User.objects.get(id=1)

        for i in range(num_entries):
            if random.randint(0, 1):
                lang = 'en'
            else:
                lang = 'es'
            cat_id = random.randint(1, 4)
            blogpost_content = random.choice(BLOGPOST_CONTENTS)
            blogpost_title = random.choice(BLOGPOST_TITLES)
            loren_id = random.randint(0, 4)
            title_id = random.randint(0, 4)

            print "Category: {} | Loren: {} | Title: {}".format(
                cat_id, loren_id, title_id)

            self.__create_entry(lang, user, Category.objects.get(id=cat_id),
                                blogpost_title, blogpost_content,
                                self.__random_date())

    def create_links(self):
        self.__create_link("Dummy link", "dummy.com", 0)
        self.__create_link("Foo", "foo.com", 2)
        self.__create_link("Testing and testing", "testing.org", 1)

    def create_all(self):
        self.create_categories()
        self.create_entries(1000)
        self.create_links()
