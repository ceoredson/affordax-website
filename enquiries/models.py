import uuid

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet


class EnquiryKind(models.TextChoices):
    CONTACT = "CONTACT", "General contact"
    DEMO = "DEMO", "Book a conversation"
    EMPLOYER = "EMPLOYER", "Employer application"
    PROVIDER = "PROVIDER", "Financial provider application"
    COMPLAINT = "COMPLAINT", "Complaint or correction"


class EnquiryStatus(models.TextChoices):
    NEW = "NEW", "New"
    IN_PROGRESS = "IN_PROGRESS", "In progress"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"


@register_snippet
class Enquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField(max_length=20, choices=EnquiryKind.choices, db_index=True)
    status = models.CharField(max_length=20, choices=EnquiryStatus.choices, default=EnquiryStatus.NEW, db_index=True)
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)
    organisation = models.CharField(max_length=180, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    employee_count = models.PositiveIntegerField(null=True, blank=True)
    licence_reference = models.CharField(max_length=120, blank=True)
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    consent_to_contact = models.BooleanField(default=False)
    marketing_opt_in = models.BooleanField(default=False)
    source_url = models.URLField(max_length=500, blank=True)
    request_fingerprint = models.CharField(max_length=64, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("kind"), FieldPanel("status"), FieldPanel("created_at", read_only=True),
        ], heading="Triage"),
        MultiFieldPanel([
            FieldPanel("full_name"), FieldPanel("email"), FieldPanel("phone"),
            FieldPanel("organisation"), FieldPanel("job_title"),
        ], heading="Contact"),
        MultiFieldPanel([
            FieldPanel("employee_count"), FieldPanel("licence_reference"),
            FieldPanel("subject"), FieldPanel("message"),
        ], heading="Request"),
        FieldPanel("consent_to_contact", read_only=True),
        FieldPanel("marketing_opt_in", read_only=True),
    ]

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["kind", "status", "created_at"])]

    def __str__(self):
        return f"{self.get_kind_display()} · {self.full_name}"

