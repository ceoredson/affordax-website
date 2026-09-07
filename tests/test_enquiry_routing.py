import pytest

from enquiries.models import Enquiry


@pytest.mark.django_db
def test_provider_cannot_bypass_licence_requirement_with_hidden_kind(client):
    response = client.post('/enquire/provider/', {
        'kind': 'CONTACT', 'full_name': 'Test Person',
        'email': 'test@example.com', 'message': 'Discuss access',
        'consent_to_contact': 'on',
    })
    assert response.status_code == 200
    assert not Enquiry.objects.exists()
    assert 'licence or registration reference' in response.content.decode()


@pytest.mark.django_db
def test_route_owns_enquiry_kind(client):
    response = client.post('/enquire/contact/', {
        'kind': 'PROVIDER', 'full_name': 'Test Person',
        'email': 'test@example.com', 'message': 'A general question',
        'consent_to_contact': 'on',
    })
    assert response.status_code == 302
    assert Enquiry.objects.get().kind == 'CONTACT'
