import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'component_a.base.test_settings')
from django.core.wsgi import get_wsgi_application
get_wsgi_application()