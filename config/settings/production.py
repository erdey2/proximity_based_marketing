from .base import *

DEBUG = False
SECRET_KEY = env("djhngo-insecure-%7vimodp6z3r5$e$7+%ab)*c-!xygdkjf3=8md3@a(o&o6e@9K")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# Secure settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True