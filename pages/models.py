from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page

from .blocks import PUBLIC_BLOCKS


class HomePage(Page):
    template = "pages/home_page.html"
    max_count = 1

    eyebrow = models.CharField(max_length=80, blank=True)
    hero_title = models.CharField(max_length=150)
    hero_text = models.TextField(max_length=420)
    primary_label = models.CharField(max_length=50, default="Book a conversation")
    primary_url = models.CharField(max_length=240, default="/enquire/demo/")
    secondary_label = models.CharField(max_length=50, default="See how it works")
    secondary_url = models.CharField(max_length=240, default="/how-it-works/")
    signal_label = models.CharField(max_length=80, default="Built for Malawi's private sector")
    body = StreamField(PUBLIC_BLOCKS, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("eyebrow"), FieldPanel("hero_title"), FieldPanel("hero_text"),
            FieldPanel("primary_label"), FieldPanel("primary_url"),
            FieldPanel("secondary_label"), FieldPanel("secondary_url"),
            FieldPanel("signal_label"),
        ], heading="Opening statement"),
        FieldPanel("body"),
        InlinePanel("proof_points", label="Proof point"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["pages.StandardPage", "pages.AudiencePage", "pages.InsightIndexPage"]


class HomeProofPoint(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="proof_points")
    value = models.CharField(max_length=36)
    label = models.CharField(max_length=150)
    panels = [FieldPanel("value"), FieldPanel("label")]


class StandardPage(Page):
    template = "pages/standard_page.html"
    eyebrow = models.CharField(max_length=80, blank=True)
    introduction = models.TextField(max_length=500, blank=True)
    body = StreamField(PUBLIC_BLOCKS, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("eyebrow"), FieldPanel("introduction"), FieldPanel("body"),
    ]
    parent_page_types = ["pages.HomePage"]
    subpage_types = []


class AudiencePage(Page):
    template = "pages/audience_page.html"
    audience_label = models.CharField(max_length=60)
    hero_title = models.CharField(max_length=150)
    hero_text = models.TextField(max_length=440)
    action_label = models.CharField(max_length=50)
    action_url = models.CharField(max_length=240)
    body = StreamField(PUBLIC_BLOCKS, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("audience_label"), FieldPanel("hero_title"), FieldPanel("hero_text"),
            FieldPanel("action_label"), FieldPanel("action_url"),
        ], heading="Audience opening"),
        FieldPanel("body"),
    ]
    parent_page_types = ["pages.HomePage"]
    subpage_types = []


class InsightIndexPage(Page):
    template = "pages/insight_index_page.html"
    introduction = models.TextField(max_length=420, blank=True)
    content_panels = Page.content_panels + [FieldPanel("introduction")]
    parent_page_types = ["pages.HomePage"]
    subpage_types = ["pages.InsightPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["articles"] = self.get_children().live().public().specific().order_by("-first_published_at")
        return context


class InsightPage(Page):
    template = "pages/insight_page.html"
    publication_date = models.DateField()
    summary = models.TextField(max_length=320)
    body = RichTextField(features=["h2", "h3", "bold", "italic", "link", "ol", "ul", "blockquote"])

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"), FieldPanel("summary"), FieldPanel("body"),
    ]
    parent_page_types = ["pages.InsightIndexPage"]
    subpage_types = []

