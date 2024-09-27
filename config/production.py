from .settings import *  # Import everything from settings.py

# Override the settings specific to production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-75$7^wu+ilhv^68^vg*b88v7!&qcv1l$@p@j_#3grst=sro)td'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'djangonauts.me']

# Use SECURE_* Settings for HTTPS 
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Use Secure Session and CSRF Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Disable X-Frame-Options Header
X_FRAME_OPTIONS = 'DENY'

# Set SECURE_PROXY_SSL_HEADER if Behind a Proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Limit Cross-Origin Resource Sharing (CORS)
CORS_ORIGIN_WHITELIST = ['https://djangonauts.me']
