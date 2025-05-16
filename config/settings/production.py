from .base import *

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DATABASES = {"default": dj_database_url.parse("postgresql://proximity_market_owner:npg_V3ByzE9vpkZm@ep-aged-resonance-a5yura0n-pooler.us-east-2.aws.neon.tech/proximity_market?sslmode=require")}

print("DB ENGINE:", os.getenv("DB_ENGINE"))
print("DB NAME:", os.getenv("DB_NAME"))
print("DB USER:", os.getenv("DB_USER"))
print("DB HOST:", os.getenv("DB_HOST"))

# Secure settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files setup
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
