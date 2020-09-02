from urllib.parse import urlparse

import requests


def validate_url(url: str) -> bool:
    url = url.strip()

    if not url:
        return False

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    domain = parsed_url.netloc

    if not all([scheme, domain]):
        return False

    r = requests.head(url)
    if r.status_code != 200:
        return False

    return True
