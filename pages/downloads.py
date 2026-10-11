import json
import logging
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from django.core.cache import cache
from django.shortcuts import render

logger = logging.getLogger(__name__)
REPOSITORY = 'ceoredson/affordax-downloads'
MANIFEST_URL = f'https://github.com/{REPOSITORY}/releases/latest/download/desktop-manifest.json'
PLATFORMS = {
    'windows-x64': ('Windows', '64-bit Intel / AMD · Microsoft WebView2', {'exe'}),
    'macos-arm64': ('macOS · Apple Silicon', 'M-series Macs · Disk image', {'dmg'}),
    'macos-x64': ('macOS · Intel', 'Intel Macs · Disk image', {'dmg'}),
    'linux-x64': ('Linux', '64-bit Intel / AMD · Debian package or AppImage', {'deb', 'AppImage'}),
}


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or manifest.get('schema') != 1:
        raise ValueError('Unsupported manifest.')
    version = manifest.get('version', '')
    if not isinstance(version, str) or not re.fullmatch(r'\d{1,4}\.\d{1,4}\.\d{1,4}', version):
        raise ValueError('Invalid release version.')
    artifacts = manifest.get('artifacts')
    if not isinstance(artifacts, list) or not 1 <= len(artifacts) <= 8:
        raise ValueError('Invalid release artifacts.')
    validated = []
    identities = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError('Invalid artifact.')
        platform = artifact.get('platform')
        format_name = artifact.get('format')
        if not isinstance(platform, str) or not isinstance(format_name, str) or platform not in PLATFORMS or format_name not in PLATFORMS[platform][2]:
            raise ValueError('Unsupported installer.')
        identity = (platform, format_name)
        if identity in identities:
            raise ValueError('Duplicate installer.')
        identities.add(identity)
        name = f'Affordax-{version}-{platform}.{format_name}'
        expected = f'https://github.com/{REPOSITORY}/releases/download/desktop-v{version}/{name}'
        if artifact.get('name') != name or artifact.get('url') != expected:
            raise ValueError('Untrusted download address.')
        address = urlsplit(expected)
        if address.scheme != 'https' or address.netloc != 'github.com':
            raise ValueError('Invalid download origin.')
        checksum = artifact.get('sha256', '')
        if not isinstance(checksum, str) or not re.fullmatch(r'[0-9a-f]{64}', checksum):
            raise ValueError('Invalid checksum.')
        size = artifact.get('bytes', 0)
        if not isinstance(size, int) or isinstance(size, bool) or not 0 < size <= 2 * 1024 ** 3:
            raise ValueError('Invalid artifact size.')
        validated.append({**artifact, 'name': name})
    return {'version': version, 'artifacts': validated}


def fetch_release():
    cached = cache.get('desktop-downloads:current')
    if cached is not None:
        return cached
    try:
        request = Request(MANIFEST_URL, headers={'User-Agent': 'Affordax-downloads', 'Accept': 'application/json'})
        with urlopen(request, timeout=3) as response:
            content = response.read(128 * 1024 + 1)
        if len(content) > 128 * 1024:
            raise ValueError('Release metadata is too large.')
        release = validate_manifest(json.loads(content))
        cache.set('desktop-downloads:last-good', release, 86400)
        result = {'release': release, 'stale': False}
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
        logger.info('Desktop release metadata unavailable: %s', type(error).__name__)
        previous = cache.get('desktop-downloads:last-good')
        result = {'release': previous, 'stale': previous is not None}
    cache.set('desktop-downloads:current', result, 300)
    return result


def downloads(request):
    state = fetch_release()
    release = state['release']
    cards = []
    for platform, (title, description, _) in PLATFORMS.items():
        cards.append({'title': title, 'description': description, 'platform': platform,
            'artifacts': [artifact for artifact in release['artifacts'] if artifact['platform'] == platform] if release else []})
    return render(request, 'pages/downloads.html', {'cards': cards, 'release': release, 'stale': state['stale']})
