# Django settings for bmed project.
import os
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Noel', 'salfetkaodua@gmail.com'),
)

MANAGERS = (
    ('Zakaz', 'medexsouth.com.ua@gmail.com'),
    ('Buhgalter', 'detskayaliniyal@mail.ru'),
    ('Manager', 'exxl.odessa@mail.ru'),
    ('Director', 'fishka_myv@mail.ru'),
)

EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[bmed]'
EMAIL_HOST_USER = 'info@bmed.com.ua'
EMAIL_HOST_PASSWORD = 'kbybzajhlf15'
DEFAULT_FROM_EMAIL = 'info@bmed.com.ua'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'medex',          # Or path to database file if using sqlite3.
        'USER': 'medex',                     # Not used with sqlite3.
        'PASSWORD': 'medex',                 # Not used with sqlite3.
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
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zmsa&5z8g(8rph%7ob4ghdxvc0^k&+sdg2*4$l-rd=_%tdwhpk'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.comments',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'django_extensions',
    'captcha',
    'captcha_comments',
    'tagging',
    'mptt',
    'eshop',
    'main',
    'gunicorn',
)

COMMENTS_APP = 'captcha_comments'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "eshop.context_processors.eshop",
    "main.context_processors.constants",
    )

CACHE_BACKEND = 'dummy://' if DEBUG else 'file://%s/cache?timeout=3000' % PROJECT_ROOT

MPTT_ADMIN_LEVEL_INDENT = 30

FILE_UPLOAD_PERMISSIONS = 0644

try:
    from local_settings import *
except ImportError:
    pass
