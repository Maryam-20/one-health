import sys
import os

print("--- [SUPERUSER SCRIPT STARTED] ---", flush=True)

try:
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techcare.settings")
    django.setup()
    print("Django setup completed successfully.", flush=True)
except Exception as e:
    print(f"Error during Django setup: {e}", flush=True)
    sys.exit(1)

from django.contrib.auth import get_user_model

User = get_user_model()

# Retrieve credentials from environment variables
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "Admin")
last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "User")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

print(f"DEBUG: DJANGO_SUPERUSER_EMAIL found: {bool(email)}", flush=True)
print(f"DEBUG: DJANGO_SUPERUSER_PASSWORD found: {bool(password)}", flush=True)

if not email or not password:
    print("ERROR: DJANGO_SUPERUSER_EMAIL or DJANGO_SUPERUSER_PASSWORD environment variable is missing or empty!", flush=True)
else:
    if not User.objects.filter(email=email).exists():
        print(f"Creating superuser for {email}...", flush=True)
        try:
            User.objects.create_superuser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            print("SUCCESS: Superuser created successfully!", flush=True)
        except Exception as e:
            print(f"ERROR: Failed to create superuser: {e}", flush=True)
    else:
        print(f"INFO: Superuser with email '{email}' already exists.", flush=True)

print("--- [SUPERUSER SCRIPT FINISHED] ---", flush=True)