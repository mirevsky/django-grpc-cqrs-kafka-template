import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'component_b.base.test_settings')
from django.core.wsgi import get_wsgi_application
get_wsgi_application()