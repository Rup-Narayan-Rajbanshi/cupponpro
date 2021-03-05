from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['api.cupponpro.com', 'devapi.cupponpro.com', '127.0.0.1', 'localhost']

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

ENABLE_DEBUG_TOOLBAR = False

try:
    from .local_settings import *
except Exception as e:
    pass


if ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE += (
        'qinspect.middleware.QueryInspectMiddleware',
    )
    if 'loggers' in LOGGING:
        LOGGING['loggers'] = {
            'qinspect': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            }
        }
    QUERY_INSPECT_ENABLED = True
    QUERY_INSPECT_LOG_QUERIES = True
    # QUERY_INSPECT_LOG_TRACEBACKS = True


if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )    
    INSTALLED_APPS += (
        'debug_toolbar',
    )