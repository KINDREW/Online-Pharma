"""Development settings"""
from .base import *
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pharmacy',
        'USER': 'postgres',
        'PASSWORD': os.getenv('DATABASE_PASSWORD')
    }
}
