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


class ContentTest(TestCase):

    def setUp(self):
        dc = DummyCreator()
        dc.create_all()

    # TODO Create further tests to verify the data created


class DummyCreator():
    """ Creates dummy categories, entries and links, for testing the blog in
    non production environment
    """
    title_text = {
        0: "Nullam euismod lacinia ultrices. Integer.",
        1: "Ut sapien ante, volutpat sit amet posuere consequat",
        2: "Ut eget quam vitae velit ornare adipiscing.",
        3: "Cras erat sapien, faucibus blandit mattis a, dignissim eget metus.",
        4: "Nunc sagittis velit tortor."
    }
    lorenipsum_text = {
        0: "Vivamus sit amet tellus a nulla iaculis ultricies semper pellentesque tellus. Praesent nec lacus eu ipsum pulvinar accumsan. Morbi vitae ante nunc, a fringilla risus. Maecenas at leo tellus. In hac habitasse platea dictumst. Proin sapien massa, egestas nec vehicula sit amet, porttitor at leo. Suspendisse potenti. Praesent purus massa, ultrices non lobortis vel, fermentum sit amet diam. Aliquam vel lacus dolor, sed pellentesque eros.",
        1: "Curabitur ac elit et libero ornare adipiscing a nec leo. Vestibulum ornare, odio sed vulputate porttitor, lorem dolor molestie ligula, ut aliquet purus metus nec ligula. Nunc leo nunc, interdum consectetur ullamcorper vitae, varius id velit. Praesent tempus lacinia quam vitae pellentesque. Aenean at nunc elit. Pellentesque vehicula luctus urna at mollis. Aliquam ligula sapien, facilisis id cursus ut, molestie in lorem. Maecenas laoreet feugiat nunc quis dapibus. Phasellus imperdiet imperdiet vulputate. Etiam eu felis nunc. Morbi vitae magna augue, nec dictum neque. Quisque egestas ultrices venenatis.",
        2: "Cras rutrum dignissim tristique. Suspendisse at blandit mi. Maecenas suscipit dui et nibh accumsan tempus. Integer sed metus elit. Sed vel nulla justo, egestas vulputate tellus. Nulla rutrum tincidunt tincidunt. Phasellus vehicula lorem quis ante aliquet eu gravida mauris rhoncus. Sed sed erat massa. In in enim eros, sit amet tincidunt diam. Phasellus ac magna vel arcu mollis convallis quis vel ante. Pellentesque tortor tortor, pretium a volutpat sit amet, consectetur vel diam.",
        3: "In odio ante, commodo sit amet condimentum ac, semper id eros. Nulla orci nibh, adipiscing eu lacinia sed, condimentum vitae sem. Suspendisse et mi a felis euismod iaculis non a arcu. Quisque ipsum odio, elementum quis interdum posuere, feugiat non nisi. Nam arcu nisi, eleifend at sollicitudin sit amet, mattis blandit lacus. Praesent dignissim tortor et est accumsan eget pellentesque massa pellentesque. Quisque nec urna eu lacus suscipit fringilla. Maecenas malesuada posuere pulvinar. Duis adipiscing.",
        4: "Pellentesque vel nisl risus. Praesent erat justo, venenatis et condimentum in, porttitor sed odio. Aenean quis nunc dapibus eros fermentum rhoncus. Phasellus elementum felis eu lorem gravida pharetra. Vivamus feugiat risus at lorem sodales id iaculis tellus dignissim. Praesent ullamcorper nibh rutrum nisl rutrum vel varius justo mattis. Proin convallis laoreet nulla, a imperdiet risus porta eget. Sed eros sem, pretium blandit volutpat rhoncus, placerat eget metus. Suspendisse vitae velit magna, consequat volutpat massa. Nullam sed augue lacus, at condimentum odio. Nulla facilisi. Aliquam vel laoreet felis. Aliquam erat volutpat. Nullam sagittis malesuada turpis. Fusce."
    }

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
            loren_id = random.randint(0, 4)
            title_id = random.randint(0, 4)

            print "Category: {} | Loren: {} | Title: {}".format(
                cat_id, loren_id, title_id)

            self.__create_entry(lang,
                                user,
                                Category.objects.get(id=cat_id),
                                self.title_text[title_id],
                                self.lorenipsum_text[loren_id],
                                self.__random_date())

    def create_links(self):
        self.__create_link("Dummy link", "dummy.com", 0)
        self.__create_link("Foo", "foo.com", 2)
        self.__create_link("Testing and testing", "testing.org", 1)

    def create_all(self):
        self.create_categories()
        self.create_entries(1000)
        self.create_links()
