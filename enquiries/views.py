from dataclasses import dataclass

from django.http import Http404
from django.shortcuts import redirect, render
from django_ratelimit.decorators import ratelimit

from .forms import EnquiryForm, style_form
from .models import EnquiryKind
from .services import SubmissionContext, submit_enquiry


@dataclass(frozen=True)
class FormPage:
    kind: str
    eyebrow: str
    heading: str
    introduction: str
    submit_label: str
    privacy_note: str


PAGES = {
    "contact": FormPage(EnquiryKind.CONTACT, "Start a conversation", "Tell us what you are working through", "Questions, partnerships or something unclear—we will route your message to the right person.", "Send message", "Do not include passwords, one-time codes, full identity numbers or payroll files."),
    "demo": FormPage(EnquiryKind.DEMO, "A working session, not a sales script", "See the workflow with your own operating questions", "We will focus the conversation on your payroll or lending process, controls and integration needs.", "Request a conversation", "We will use your details only to arrange and follow up this request unless you opt into updates."),
    "employer": FormPage(EnquiryKind.EMPLOYER, "For employers", "Bring deduction administration into one accountable workflow", "Tell us about your organisation and payroll environment. This is an enquiry, not automatic activation.", "Submit employer enquiry", "Do not upload employee or payroll information here."),
    "provider": FormPage(EnquiryKind.PROVIDER, "For financial providers", "Explore governed access to salary-backed collections", "Licensed institutions can discuss products, origination controls, settlement and integration.", "Submit provider enquiry", "Submitting this form does not constitute approval or platform access."),
    "complaint": FormPage(EnquiryKind.COMPLAINT, "Support and redress", "Raise a complaint without exposing sensitive information", "Give us a short summary and any existing case reference. We will contact you through a protected channel if more evidence is needed.", "Raise complaint", "Never enter a full National ID, password, one-time code or salary details in this form."),
}


@ratelimit(key="ip", rate="6/h", method="POST", block=True)
def enquiry_page(request, page_name):
    try:
        page = PAGES[page_name]
    except KeyError as exc:
        raise Http404 from exc
    initial = {"kind": page.kind}
    form = style_form(EnquiryForm(request.POST or None, initial=initial))
    if request.method == "POST" and form.is_valid():
        enquiry = submit_enquiry(
            form.cleaned_data,
            context=SubmissionContext(
                source_url=request.build_absolute_uri(),
                ip_address=request.META.get("REMOTE_ADDR", "unknown"),
            ),
        )
        request.session["enquiry_reference"] = str(enquiry.id)
        return redirect("enquiries:thanks")
    return render(request, "enquiries/form_page.html", {"form": form, "form_page": page})


def thanks(request):
    reference = request.session.pop("enquiry_reference", "")
    return render(request, "enquiries/thanks.html", {"reference": reference})
