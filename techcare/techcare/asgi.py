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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techcare.settings")

# Get the base application
application = get_asgi_application()

# Wrap the application to include database connection check
@sync_to_async
def check_database():
    try:
        connections['default'].ensure_connection()
    except OperationalError:
        return False
    return True

async def database_middleware(scope, receive, send):
    if scope["type"] == "lifespan":
        # Handle lifespan messages
        message = await receive()
        if message["type"] == "lifespan.startup":
            # Check database connection on startup
            is_connected = await check_database()
            if not is_connected:
                await send({"type": "lifespan.startup.failed"})
                return
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})
        return

    # Pass through to the main application
    await application(scope, receive, send)

# Replace the base application with our wrapped version
application = database_middleware
