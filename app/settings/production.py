# -*- coding: utf-8 -*-
from .base import *

SECRET_KEY = ')0*14wp#g8si#31c6&$)^(3n_$dc!jipnh79ql1tus!%(b9&o-'

DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'NAME': 'demo_db',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'USER': 'demo_user',
        'PASSWORD': 'demo_pass',
        'HOST': '127.0.0.1'
    },
   
}


STATIC_ROOT = '/var/www/static.example.dev/'
MEDIA_ROOT = '/var/www/media.example.dev/'

SITE_URL = 'http://example.dev'
MEDIA_URL = 'http://media.example.dev/'
STATIC_URL = 'http://static.example.dev/'

SITE_NAME = "http://example.dev"


# Hosts/domain names that are valid for this site; required if DEBUG is False
ALLOWED_HOSTS = ['example.dev',]