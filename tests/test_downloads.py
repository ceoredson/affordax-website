from copy import deepcopy
from unittest.mock import patch

import pytest
from django.core.cache import cache

from pages.downloads import fetch_release, validate_manifest


def manifest():
    name = 'Affordax-1.0.0-windows-x64.exe'
    return {'schema': 1, 'version': '1.0.0', 'artifacts': [{'name': name, 'platform': 'windows-x64',
        'format': 'exe', 'bytes': 1024, 'sha256': 'a' * 64,
        'url': f'https://github.com/ceoredson/affordax-downloads/releases/download/desktop-v1.0.0/{name}'}]}


def test_manifest_accepts_only_expected_public_installer_addresses():
    assert validate_manifest(manifest())['version'] == '1.0.0'


@pytest.mark.parametrize('url', ['https://evil.example/app.exe', 'http://127.0.0.1/private',
    'https://github.com/ceoredson/affordax-desktop/releases/download/private/app.exe'])
def test_untrusted_or_private_source_downloads_are_rejected(url):
    data = manifest()
    data['artifacts'][0]['url'] = url
    with pytest.raises(ValueError):
        validate_manifest(data)


def test_duplicates_and_invalid_platform_types_are_rejected():
    data = manifest()
    data['artifacts'].append(deepcopy(data['artifacts'][0]))
    with pytest.raises(ValueError):
        validate_manifest(data)
    data = manifest()
    data['artifacts'][0]['platform'] = []
    with pytest.raises(ValueError):
        validate_manifest(data)


@pytest.mark.django_db
def test_download_page_does_not_invent_unpublished_installers(client):
    with patch('pages.downloads.fetch_release', return_value={'release': None, 'stale': False}):
        response = client.get('/downloads/')
    assert response.status_code == 200
    assert b'Public installers are not published yet' in response.content
    assert b'Installer publication pending' in response.content
    assert b'Affordax-1.0.0' not in response.content


@pytest.mark.django_db
def test_published_downloads_include_checksums_and_platform_selection(client):
    with patch('pages.downloads.fetch_release', return_value={'release': validate_manifest(manifest()), 'stale': False}):
        response = client.get('/downloads/')
    assert response.status_code == 200
    assert b'Affordax-1.0.0-windows-x64.exe' in response.content
    assert b'a' * 64 in response.content
    assert b'Apple Silicon' in response.content
    assert b'macOS' in response.content
    assert b'Linux' in response.content


def test_network_failure_retains_only_a_previously_valid_release():
    cache.clear()
    release = validate_manifest(manifest())
    cache.set('desktop-downloads:last-good', release)
    with patch('pages.downloads.urlopen', side_effect=TimeoutError):
        result = fetch_release()
    assert result == {'release': release, 'stale': True}
    cache.clear()
