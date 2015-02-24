"""
WSGI config for subzeromedia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, site, sys

base = os.path.dirname(os.path.dirname(__file__))
base_parent = os.path.dirname(base)
sys.path.append(base)
sys.path.append(base_parent)

site.addsitedir('/home/socialnetworkstarter_env/lib/python2.7/site-packages/')
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings.production"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
