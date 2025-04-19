from django.conf import settings
import os

# Start with a copy of the base settings
from pygoat.settings import *

# Override database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable django-heroku for tests
import django_heroku
django_heroku.settings = lambda x: None  # Disable django_heroku for tests

# Disable migrations for faster testing
class DisableMigrations:
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Simplify middleware for testing
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Remove problematic settings for SQLite
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Disable social authentication for tests
INSTALLED_APPS = [app for app in INSTALLED_APPS if not app.startswith('allauth.')]

# Use a faster password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable logging for tests
LOGGING = {}

# Remove social providers
SOCIALACCOUNT_PROVIDERS = {}

# Disable whitenoise for tests
MIDDLEWARE = [m for m in MIDDLEWARE if m != 'whitenoise.middleware.WhiteNoiseMiddleware']
