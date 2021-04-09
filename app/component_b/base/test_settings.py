from component_b.base.settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "memory:",
    }
}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

ROOT_URLCONF = 'component_b.base.urls'
