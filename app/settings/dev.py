# -*- coding: utf-8 -*-
from .base import *

SECRET_KEY = ')0*14wp#g8si#31c6&$)^(3n_$dc!jipnh79ql1tus!%(b9&o-'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
