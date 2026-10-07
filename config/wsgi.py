"""
WSGI config untuk project SIAK PKK.
Dipakai saat deploy ke server production (misalnya via Gunicorn + Nginx).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
