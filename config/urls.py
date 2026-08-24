from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from pages.views import health, robots

urlpatterns = [
    path("health/", health, name="health"),
    path("robots.txt", robots, name="robots"),
    path("sitemap.xml", sitemap, name="sitemap"),
    path("site-admin/", include(wagtailadmin_urls)),
    path("system-admin/", admin.site.urls),
    path("documents/", include(wagtaildocs_urls)),
    path("enquire/", include("enquiries.urls")),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "images/favicon.svg", permanent=True)),
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
