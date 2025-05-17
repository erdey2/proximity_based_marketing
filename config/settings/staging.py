from .base import *

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# Optional: use different DB
""" DATABASES = {
    'default': env.db("STAGING_DATABASE_URL"),
} """
