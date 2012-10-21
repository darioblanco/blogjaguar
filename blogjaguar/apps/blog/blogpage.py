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

from django.utils.translation import ugettext as _

from blog.models import Entry


class BlogPage():
    """ Refers to a page which lists diferent entries
    with the user's selected language
    """

    def __init__(self, l):
        self.language = l

    def posts_year(self, year):
        """ Returns the list of entries from a selected year.
        """
        return Entry.objects.filter(
            lang=self.language, published=True, date__year=year)

    def posts_month(self, month, year):
        """ Returns the list of entries from a selected month and year.
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
