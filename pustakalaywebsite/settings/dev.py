from .base import *
from .secrets_dev import *
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','192.168.1.63']
BASE_URL = '127.0.0.1:8000'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
