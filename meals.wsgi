#!/usr/bin/python

import os
import sys

sys.path.append('/home/meals/django/')
sys.path.append('/home/meals/django/django_randommeal/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_randommeal.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
