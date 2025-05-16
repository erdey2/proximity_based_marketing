from .base import *

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'proximity_market',
        'USER': 'proximity_market_owner',
        'PASSWORD': 'npg_V3ByzE9vpkZm',
        'HOST': 'ep-aged-resonance-a5yura0n-pooler.us-east-2.aws.neon.tech',
        'PORT': '5432',
    }
}

# Secure settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

print("PRODUCTION DATABASE_URL:", env.str("DATABASE_URL", default="NOT SET"))
# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
