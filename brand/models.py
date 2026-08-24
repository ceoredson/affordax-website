from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting(icon="site")
class SiteIdentity(BaseSiteSetting):
    display_name = models.CharField(max_length=80, default="Affordax")
    descriptor = models.CharField(max_length=140, default="Affordability and payroll, connected")
    legal_name = models.CharField(max_length=180, blank=True)
    portal_url = models.URLField(default="https://portal.example.com")
    support_email = models.EmailField(default="support@example.com")
    partnerships_email = models.EmailField(default="partners@example.com")
    phone = models.CharField(max_length=32, blank=True)
    office = models.CharField(max_length=140, default="Lilongwe, Malawi")
    linkedin_url = models.URLField(blank=True)
    primary_colour = models.CharField(max_length=7, default="#ef5b3f")
    ink_colour = models.CharField(max_length=7, default="#17202a")

    panels = [
        MultiFieldPanel([
            FieldPanel("display_name"), FieldPanel("descriptor"), FieldPanel("legal_name"),
            FieldPanel("portal_url"),
        ], heading="Identity"),
        MultiFieldPanel([
            FieldPanel("support_email"), FieldPanel("partnerships_email"),
            FieldPanel("phone"), FieldPanel("office"), FieldPanel("linkedin_url"),
        ], heading="Contact"),
        MultiFieldPanel([
            FieldPanel("primary_colour"), FieldPanel("ink_colour"),
        ], heading="Brand colours"),
    ]

