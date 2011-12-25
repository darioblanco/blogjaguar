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

import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# For holding the different apps in the apps folder
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
#USE_L10N = True

ADMINS = (
    #('sharker', 'dblancoit@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/Users/sharker/Programacion/darioblog/darioblog.db',         # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# Para evitar import circular de django.utils.translation se hace de esta manera
ugettext = lambda s: s
LANGUAGES = (
  ('es', ugettext('Spanish')),
  ('en', ugettext('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Path de la raiz del proyecto
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory dariomedia files should be collected to.
# Don't put anything in this directory yourself; store your dariomedia files
# in apps' "dariomedia/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/dariomedia/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for dariomedia files.
STATIC_URL = '/static/'

# URL prefix for admin dariomedia files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Additional locations of dariomedia files
#STATICFILES_DIRS = (
#    os.path.join(PROJECT_ROOT, 'media', 'dariomedia'),  # /blog/dariomedia
#)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

# Make this unique, and don't share it with anybody.
if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            import string, random
            SECRET_KEY = ''.join(random.choice(string.printable) for i in xrange(50))
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters to set your secret key' % SECRET_FILE)
# SECRET_KEY = 'qc#7l9jt2h@zk=hl6f(#s0miv^i_59)b%2b(xubs_(-yx#vc2$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# Si se usa CacheMiddleware, se debe poner LocaleMiddleware detras de el
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'darioblog.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'blog',
    'facebook',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# For 'facebook' app
AUTHENTICATION_BACKENDS = (
    'facebook.backend.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend'
)
AUTH_PROFILE_MODULE = 'facebook.FacebookProfile'

# Fill the app id and app secret key according to your facebook developer profile
FACEBOOK_SCOPE = 'email,publish_stream'
FACEBOOK_APP_ID = '237060613017863'
FACEBOOK_APP_SECRET = 'debd206e9fd73bd9ad95bdaa647dafdc'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}