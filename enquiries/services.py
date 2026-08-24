import hashlib
import logging
from dataclasses import dataclass

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from .models import Enquiry

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SubmissionContext:
    source_url: str
    ip_address: str


def _fingerprint(ip_address):
    material = f"{settings.SECRET_KEY}:{ip_address}".encode()
    return hashlib.sha256(material).hexdigest()


def _notify(enquiry_id):
    if not settings.ENQUIRY_NOTIFICATION_EMAIL:
        return
    enquiry = Enquiry.objects.get(id=enquiry_id)
    try:
        send_mail(
            subject=f"New website request: {enquiry.get_kind_display()}",
            message=(
                f"Reference: {enquiry.id}\n"
                f"From: {enquiry.full_name} <{enquiry.email}>\n"
                f"Organisation: {enquiry.organisation or 'Not supplied'}\n\n"
                "Review the request in the website administration area."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ENQUIRY_NOTIFICATION_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Failed to send enquiry notification", extra={"enquiry_id": str(enquiry.id)})


@transaction.atomic
def submit_enquiry(cleaned_data, *, context):
    payload = {key: value for key, value in cleaned_data.items() if key != "website"}
    enquiry = Enquiry.objects.create(
        **payload,
        source_url=context.source_url[:500],
        request_fingerprint=_fingerprint(context.ip_address),
    )
    transaction.on_commit(lambda: _notify(enquiry.id))
    return enquiry

