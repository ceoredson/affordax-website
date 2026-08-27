from django.conf import settings


def site_identity(request):
    return {
        "configured_site_name": settings.SITE_NAME,
        "configured_descriptor": settings.SITE_DESCRIPTOR,
        "configured_portal_url": settings.PORTAL_URL,
        "configured_public_site_url": settings.PUBLIC_SITE_URL,
    }
