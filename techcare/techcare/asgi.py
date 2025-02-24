"""
ASGI config for techcare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import time
from django.core.asgi import get_asgi_application
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techcare.settings")

# Try to connect to the database with retries
max_tries = 10
current_try = 1

while current_try <= max_tries:
    try:
        connections['default'].ensure_connection()
        break
    except OperationalError:
        wait = min(current_try * 2, 10)
        print(f"Database connection failed. Waiting {wait} seconds...")
        time.sleep(wait)
        current_try += 1

application = get_asgi_application()
