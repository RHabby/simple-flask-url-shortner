from urllib.parse import urlparse

import requests


# moved to forms.py with wtforms
def validate_url(url: str) -> bool:
    url = url.strip()

    if not url:
        return False

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    domain = parsed_url.netloc

    if not all([scheme, domain]):
        if scheme == "":
            url = f"https://{url}"
            return validate_url(url=url)
        return False

    r = requests.get(url)
    status = r.status_code
    print(scheme, domain, url, status)

    if str(status).startswith("3"):
        return validate_url(url=r.headers["Location"])
    if status != 200:
        return url, False

    return url, True
