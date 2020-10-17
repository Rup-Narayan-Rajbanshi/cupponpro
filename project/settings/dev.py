from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['157.245.103.32', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
