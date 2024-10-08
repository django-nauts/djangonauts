from .settings import *  # Import everything from settings.py

# Override the settings specific to production

SECRET_KEY = 'django-insecure-75$7^wu+ilhv^68^vg*b88v7!&qcv1l$@p@j_#3grst=sro)td'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'djangonauts.me', 'www.djangonauts.me', 'https://djangonauts.me']

# Change media address based on your website
MEDIA_ROOT = "/home/djangona/djangonauts/media"
MEDIA_URL = "https://media.djangonauts.me/"

# other changes
