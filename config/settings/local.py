from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-%7vimodp6z3r5$e$7+%ab)*c-!xygdgwf3=8md3@a(o&o6e@9b'
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'beacon_market_db',
        'USER': 'marketer',
        'PASSWORD': 'Marketer@1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CORS_ALLOW_ALL_ORIGINS = True
