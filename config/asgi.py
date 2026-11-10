"""
ASGI config untuk project SI SULUR.
Tidak wajib dipakai untuk MVP ini (kita pakai WSGI/Gunicorn),
tapi disertakan karena ini adalah file bawaan standar Django.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
