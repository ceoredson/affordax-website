from django.conf import settings


def site_identity(request):
    portal_url = settings.PORTAL_URL
    if not portal_url.startswith(("http://", "https://")):
        portal_url = f"https://{portal_url}"
    return {
        "configured_site_name": settings.SITE_NAME,
        "configured_descriptor": settings.SITE_DESCRIPTOR,
        "configured_portal_url": portal_url,
        "configured_public_site_url": settings.PUBLIC_SITE_URL,
    }
