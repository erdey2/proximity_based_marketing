from .base import *

DEBUG = True
SECRET_KEY = "django-insecure-%7vimodp6z3r5$e$7+%ab)*c-!xygdgwf3=8md3@a(o&o6e@9b"
ALLOWED_HOSTS = ["*"]

# Use SQLite for testing
""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "test_db.sqlite3",
    }
} """

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
