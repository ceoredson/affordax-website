from django.conf import settings
from django.http import HttpResponse, JsonResponse


def health(request):
    return JsonResponse({"status": "ok"})


def robots(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /site-admin/",
        "Disallow: /system-admin/",
        f"Sitemap: {settings.PUBLIC_SITE_URL}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")

