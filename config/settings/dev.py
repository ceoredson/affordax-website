from .base import *  # noqa: F403

DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Temporary external preview used by the team. Keep this exact rather than
# allowing every ngrok subdomain to submit requests to the development server.
ALLOWED_HOSTS.append("isthmian-maynard-idiomatic.ngrok-free.dev")  # noqa: F405
CSRF_TRUSTED_ORIGINS = ["https://isthmian-maynard-idiomatic.ngrok-free.dev"]

STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
}
