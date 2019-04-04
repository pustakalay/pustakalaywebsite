from .base import *
from .secrets_prod import *
DEBUG = False

ALLOWED_HOSTS = []
BASE_URL = 'http://www.pustakalay.in/'
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
