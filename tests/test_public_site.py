import pytest
from django.core.management import call_command

from enquiries.models import Enquiry, EnquiryKind


@pytest.fixture
def seeded_site(db):
    call_command("seed_site", verbosity=0)


def test_health_and_robots(client, settings):
    settings.PUBLIC_SITE_URL = "https://public.example"
    assert client.get("/health/").json() == {"status": "ok"}
    robots = client.get("/robots.txt")
    assert robots.status_code == 200
    assert "Disallow: /site-admin/" in robots.content.decode()
    assert "https://public.example/sitemap.xml" in robots.content.decode()


def test_seeded_homepage_is_server_rendered(client, seeded_site):
    response = client.get("/")
    assert response.status_code == 200
    content = response.content.decode()
    assert "Financial workflows should not depend on guesswork" in content
    assert "One accountable thread" in content


def test_homepage_uses_public_canonical_and_structured_data(client, seeded_site, settings):
    settings.PUBLIC_SITE_URL = "https://affordax.com"
    settings.ALLOWED_HOSTS.append("affordax-website.onrender.com")
    response = client.get("/", HTTP_HOST="affordax-website.onrender.com")
    content = response.content.decode()
    assert '<link rel="canonical" href="https://affordax.com/">' in content
    assert '"@type":"WebSite"' in content
    assert '"@type":"Organization"' in content
    assert "Payroll Affordability &amp; Deductions in Malawi" in content


@pytest.mark.parametrize("path", ["/employers/", "/providers/", "/how-it-works/", "/trust/", "/about/", "/privacy/", "/terms/", "/insights/"])
def test_seeded_pages_are_public(client, seeded_site, path):
    assert client.get(path).status_code == 200


def test_about_page_introduces_company_leadership(client, seeded_site):
    content = client.get("/about/").content.decode()
    assert "Precious Ngwira" in content
    assert "Chief Executive Officer" in content
    assert "precious-ngwira" in content


@pytest.mark.parametrize(
    "path",
    [
        "/insights/payroll-affordability-malawi/",
        "/insights/payroll-deduction-management/",
        "/insights/salary-backed-lending-malawi/",
    ],
)
def test_search_focused_insights_are_published(client, seeded_site, path):
    response = client.get(path)
    assert response.status_code == 200
    assert '"@type":"Article"' in response.content.decode()


def test_enquiry_pages_are_not_indexable(client, seeded_site):
    assert 'content="noindex,follow"' in client.get("/enquire/contact/").content.decode()
    assert 'content="noindex,nofollow"' in client.get("/enquire/thanks/").content.decode()


@pytest.mark.django_db
def test_employer_enquiry_is_persisted_before_notification(client, settings):
    settings.ENQUIRY_NOTIFICATION_EMAIL = ""
    response = client.post("/enquire/employer/", {
        "kind": EnquiryKind.EMPLOYER,
        "full_name": "Mwayi Tester",
        "email": "mwayi@example.mw",
        "phone": "+265999000000",
        "organisation": "Example Manufacturing",
        "job_title": "Payroll manager",
        "employee_count": 120,
        "licence_reference": "",
        "subject": "Employer pilot",
        "message": "We want to understand the controlled pilot process.",
        "consent_to_contact": "on",
        "website": "",
    })
    assert response.status_code == 302
    enquiry = Enquiry.objects.get()
    assert enquiry.kind == EnquiryKind.EMPLOYER
    assert enquiry.request_fingerprint
    assert "127.0.0.1" not in enquiry.request_fingerprint


@pytest.mark.django_db
def test_honeypot_and_provider_requirements_are_enforced(client):
    common = {
        "kind": EnquiryKind.PROVIDER,
        "full_name": "Test User",
        "email": "test@example.mw",
        "organisation": "Example Finance",
        "message": "Partnership enquiry",
        "consent_to_contact": "on",
    }
    response = client.post("/enquire/provider/", {**common, "website": "spam.example"})
    assert response.status_code == 200
    assert not Enquiry.objects.exists()
    response = client.post("/enquire/provider/", {**common, "website": ""})
    assert "licence or registration" in response.content.decode().lower()


@pytest.mark.django_db
def test_unknown_enquiry_form_is_not_a_server_error(client):
    assert client.get("/enquire/not-a-form/").status_code == 404
