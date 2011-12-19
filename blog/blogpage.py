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
from darioblog.blog.models import Entry
from django.utils.translation import ugettext as _


# Lists 10 entries of the user's selected language for a concrete page
class BlogPage :

    def __init__(self, l):
        self.language = l

    # Returns the number of pages for a selected language (ej: 5 pages => 0-4)
    def __getNumPages(self):
        nPosts = Entry.objects.filter(lang=self.language, published=True).count()
        return (nPosts // 10) + 1

    # Returns an adequate navigation list for a page
    def getNavList(self, page):
        page = int(page)
        navList = []
        nPages = self.__getNumPages()

        if page < nPages :
            if page < 3 : # if page is in the first 5 elements
                if nPages > 4 :
                    navList = [0,1,2,3,4]
                elif nPages == 4 :
                    navList = [0,1,2,3]
                elif nPages == 3 :
                    navList = [0,1,2]
                elif nPages == 2:
                    navList = [0,1]
                elif nPages == 1:
                    navList = [0]
            elif page == (nPages - 1) : # if page is the last page
                navList = [page-4, page-3, page-2, page-1, page]
            elif page == (nPages - 2) : # if page is the second to last
                navList = [page-3, page-2, page-1, page, page+1]
            else : # if page is in the middle
                navList = [page-2, page-1, page, page+1, page+2]

            return navList
        else :
            return False


    # Returns the list of entries of a single page (only in the user's selected language)
    def postsPage(self, page):
        page = int(page)
        
        lowerBound = page * 10
        upperBound = (page + 1) * 10

        # Shows entries with id from lowerBound to upperBound-1 (including)
        entries = Entry.objects.filter( lang=self.language,
                                         published=True
                                       ).order_by('-date')[lowerBound:upperBound]

        return entries

    # Returns the list of entries of a selected year
    def postsYear(self, year) :
        return Entry.objects.filter(lang=self.language, published=True, date__year=year)

    # Returns the list of entries of a selected month and year
    def postsMonth(self, month, year) :
        return Entry.objects.filter(lang=self.language, published=True, date__year=year, date__month=month)

    # Returns the list of archived years (years which have entries)
    def archivedYears(self):
        yearList = []

        now = datetime.now()
        actualYear = now.year
        entry = Entry.objects.all().order_by('date')[0:1] # Getting the oldest entry
        oldestYear = entry[0].date.year

        y = oldestYear
        yearObject = Year(y, self.language)
        yearList.append(yearObject)
        while y != actualYear :
            y += 1
            yearObject = Year(y, self.language)
            yearList.append(yearObject)

        return yearList

    
class Year :

    def __init__(self, year_id, l):
        self.months = []
        self.language = l
        self.year = year_id

        # Calculate the month list
        for m in range(1,13) : # for each month from 1-12
            if Entry.objects.filter(lang = self.language,
                                       date__year = self.year,
                                       date__month = m).count() > 0 :
                month = Month()
                month.year = year_id
                month.language = l
                month.month = m
                self.months.append(month) # Adds the month number

    # Return the total number of entries which belongs to this year
    def numberEntriesYear(self):
        return Entry.objects.filter(lang=self.language, date__year=self.year).count()


class Month :

    def __init(self, m, y, l):
        self.language = l
        self.month = m
        self.year = y

    # Return the total number of entries which belongs to this year
    def numberEntriesMonth(self):
        return Entry.objects.filter(lang=self.language,
                                       date__year=self.year,
                                       date__month = self.month).count()
    
    #
    def translateMonth(self):
        d = date(self.year, self.month, 1)
        mString = _(d.strftime("%B"))

        return mString.capitalize() # Translates the month number to string