from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h6kr51&!17jz68pkc-r)2vj*195r+)9^ry97o@*fpp16y6l1)n'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bankingapp3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': ''
    }
}
