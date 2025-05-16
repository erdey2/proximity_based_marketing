from .base import *

DEBUG = False
SECRET_KEY = env("djhngo-insecure-%7vimodp6z3r5$e$7+%ab)*c-!xygdkjf3=8md3@a(o&o6e@9K")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

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
