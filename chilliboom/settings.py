import os
from getenv import env


ROOT = os.path.dirname(os.path.abspath(__file__))
cd = lambda *a: os.path.join(ROOT, *a)
PROJECT = os.path.basename(ROOT)

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN'),
}

SECRET_KEY = env('SECRET_KEY', '#b7&!k2cxgw5+s$%s&p#+!_8=*lo9mv-3*p0gsozvs3%myb(=k')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'products',
    'south',
    'registration',
    'easy_thumbnails',
    'haystack',
    'bootstrap3',
    'braces',
    'disqus',

)
DISQUS_WEBSITE_SHORTNAME = 'chilliboom'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
    #'django.middleware.transaction.TransactionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "products.context_processors.featured_liked",
    "products.context_processors.search_form",
)
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


ROOT_URLCONF = '%s.urls' % PROJECT

WSGI_APPLICATION = '%s.wsgi.application' % PROJECT

# BOOTSTRAP3 = {
#     'jquery_url': '//code.jquery.com/jquery.min.js',
#     'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.1.1/',
#     'css_url': None,
#     'theme_url': None,
#     'javascript_url': None,
#     'horizontal_label_class': 'col-md-3',
#     'horizontal_field_class': 'col-md-9',
#     'set_required': True,
# }

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=env('DATABASE_URL', 'sqlite:////Users/annalopatinski/DJANGO/chilliboom/chilliboomdb.sqlite3')),
    #'ATOMIC_REQUESTS': True
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
# for django-registration
from django.core.urlresolvers import reverse_lazy

LOGIN_URL=reverse_lazy('shop_login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL=reverse_lazy('shop_logout')
MAX_USER_SHOPS = 1

#haystack search
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': cd('whoosh_index'),
    },
}

THUMBNAIL_ALIASES = {
    '': {
        'small': {'size' : (150, 150), 'crop': 'smart'},
        'middle': {'size' : (300, 300), 'crop': 'smart'},
        'large': {'size' : (500, 500), 'crop': 'smart'},


        }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#MEDIA_ROOT = cd('media')
#MEDIA_URL = '/media/'
#STATIC_ROOT = cd('static')
#STATIC_URL = '/static/'

MEDIA_ROOT = cd('public/uploads')
MEDIA_URL = '/uploads/'
STATIC_ROOT = cd('public/assets')
STATIC_URL = '/assets/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_DIRS = (
    cd('templates'),
)

# if DEBUG:
#     INSTALLED_APPS += (
#         'debug_toolbar',
#     )
#     DEBUG_TOOLBAR_PATCH_SETTINGS = False
#     MIDDLEWARE_CLASSES += (
#         'debug_toolbar.middleware.DebugToolbarMiddleware',
#     )
#     INTERNAL_IPS = (
#         '127.0.0.1',
#     )
#     DEBUG_TOOLBAR_CONFIG = {
#         'INTERCEPT_REDIRECTS': False,
#         'RENDER_PANELS': True,
#     }
