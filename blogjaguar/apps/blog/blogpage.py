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

from datetime import date, datetime
from blog.models import Entry
from django.utils.translation import ugettext as _


class BlogPage():
    """ Refers to a page which lists 10 entries of the user's selected language
    """

    def __init__(self, l):
        self.language = l

    def __get_num_pages(self):
        """ Returns the number of pages for a selected language
        (ej: 5 pages => 0-4).
        """
        nposts = Entry.objects.filter(
            lang=self.language, published=True).count()
        return (nposts // 10) + 1

    def get_nav_list(self, page):
        """ Returns an adequate navigation list for a page
        """
        page = int(page)
        nav_list = []
        npages = self.__get_num_pages()

        if page < npages:
            if page < 3:  # if page is in the first 5 elements
                if npages > 4:
                    nav_list = [0, 1, 2, 3, 4]
                elif npages == 4:
                    nav_list = [0, 1, 2, 3]
                elif npages == 3:
                    nav_list = [0, 1, 2]
                elif npages == 2:
                    nav_list = [0, 1]
                elif npages == 1:
                    nav_list = [0]
            elif page == (npages - 1):  # if page is the last page
                nav_list = [page - 4, page - 3, page - 2, page - 1, page]
            elif page == (npages - 2):  # if page is the second to last
                nav_list = [page - 3, page - 2, page - 1, page, page + 1]
            else:  # if page is in the middle
                nav_list = [page - 2, page - 1, page, page + 1, page + 2]
            return nav_list
        else:
            return False

    def posts_page(self, page):
        """ Returns the list of entries of a single page
        (only in the user's selected language).
        """
        page = int(page)

        lower_bound = page * 10
        upper_bound = (page + 1) * 10

        # Shows entries with id from lower_bound to upper_bound-1 (including)
        entries = Entry.objects.filter(
            lang=self.language, published=True).order_by(
                '-date')[lower_bound:upper_bound]

        return entries

    def posts_year(self, year):
        """ Returns the list of entries of a selected year.
        """
        return Entry.objects.filter(
            lang=self.language, published=True, date__year=year)

    def posts_month(self, month, year):
        """ Returns the list of entries of a selected month and year.
        """
        return Entry.objects.filter(
            lang=self.language, published=True, date__year=year,
            date__month=month)

    def archived_years(self):
        """ Returns the list of archived years (years which have entries).
        """
        year_list = []

        now = datetime.now()
        actual_year = now.year
        # Getting the oldest entry
        entry = Entry.objects.all().order_by('date')[0:1]
        oldest_year = entry[0].date.year

        y = oldest_year
        object_year = Year(y, self.language)
        year_list.append(object_year)
        while y != actual_year:
            y += 1
            object_year = Year(y, self.language)
            year_list.append(object_year)

        return year_list


class Year():
    """ Manages entries for a specific year and language.
    """

    def __init__(self, year_id, l):
        self.months = []
        self.language = l
        self.year = year_id

        # Calculate the month list
        for m in range(1, 13):  # for each month from 1-12
            if Entry.objects.filter(lang=self.language,
                                    date__year=self.year,
                                    date__month=m
                                    ).count() > 0:
                month = Month()
                month.year = year_id
                month.language = l
                month.month = m
                self.months.append(month)  # Adds the month number

    def number_entries_year(self):
        """ Return the total number of entries which belongs to this year.
        """
        return Entry.objects.filter(
            lang=self.language, date__year=self.year).count()

    def __unicode__(self):
        return str(self.year)


class Month():
    """ Manage entries for a specific month, year and language.
    """

    def __init(self, m, y, l):
        self.language = l
        self.month = m
        self.year = y

    def number_entries_month(self):
        """ Return the total number of entries which belongs to this year.
        """
        return Entry.objects.filter(lang=self.language,
                                    date__year=self.year,
                                    date__month=self.month).count()

    def __unicode__(self):
        """ Translates the month number to string.
        """
        d = date(self.year, self.month, 1)
        mString = _(d.strftime("%B"))
        # This string will be automatically translated to the desired language
        return mString.capitalize()
