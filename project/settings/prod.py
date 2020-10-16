from .base import *
from decouple import config

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default':{
        'ENGINE': config('DATABASE_ENGINE'),
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'PASSWORD':config('DATABASES_PASSWORD'),
    }
}