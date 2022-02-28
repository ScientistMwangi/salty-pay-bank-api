from .common import *
import os

SECRET_KEY = os.environ['SECRETE_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['prod-domainname.com']

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# configure your db connections for prod
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'HOST': '',
        'USER': '',
        'PASSWORD': ''
    }
}
