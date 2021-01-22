from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['api.cupponpro.com', 'stagingapi.cupponpro.com', '157.245.103.32', '127.0.0.1', 'localhost']

DATABASES = {
    'default':{
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('STAGING_DATABASE_NAME'),
        'USER': config('STAGING_DATABASE_USER'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'PASSWORD':config('STAGING_DATABASE_PASSWORD'),
    }
}

try:
    from .local_settings import *
except Exception as e:
    pass
