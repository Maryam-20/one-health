"""
ASGI config for techcare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.db import connections
from django.db.utils import OperationalError
from asgiref.sync import sync_to_async
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techcare.settings")

async def check_db_connection():
    max_tries = 10
    current_try = 1

    @sync_to_async
    def check_connection():
        try:
            connections['default'].ensure_connection()
            return True
        except OperationalError:
            return False

    while current_try <= max_tries:
        is_connected = await check_connection()
        if is_connected:
            break
        
        wait = min(current_try * 2, 10)
        print(f"Database connection failed. Waiting {wait} seconds...")
        await asyncio.sleep(wait)
        current_try += 1

# Initialize application after DB check
application = get_asgi_application()

# Run DB connection check
asyncio.run(check_db_connection())
