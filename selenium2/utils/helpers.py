from urllib.parse import urlparse

def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

