import random
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import requests

from . import config


@dataclass
class FetchResult:
    url: str
    final_url: str
    fetch_status: str  # "SUCCESS" | "TIMEOUT" | "HTTP_ERROR" | "NETWORK_ERROR"
    http_status: Optional[int]
    text: str
    encoding: str
    error_message: Optional[str]


def _is_allowed_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_skip_domain(url: str) -> bool:
    netloc = urlparse(url).netloc.lower()
    for skip in config.SKIP_DOMAINS:
        if skip in netloc:
            return True
    return False


def _try_decode(content: bytes) -> tuple[str, str]:
    for enc in ["utf-8", "gbk", "gb2312", "gb18030", "big5"]:
        try:
            return content.decode(enc), enc
        except (UnicodeDecodeError, LookupError):
            continue
    return content.decode("latin-1", errors="replace"), "latin-1"


def fetch_url(
    url: str,
    timeout: int = config.FETCH_TIMEOUT,
    max_retries: int = config.MAX_RETRIES,
) -> FetchResult:
    if not _is_allowed_url(url):
        return FetchResult(url=url, final_url="", fetch_status="INVALID_URL",
                           http_status=None, text="", encoding="", error_message="Invalid URL")

    if _is_skip_domain(url):
        return FetchResult(url=url, final_url="", fetch_status="SKIPPED_DOMAIN",
                           http_status=None, text="", encoding="", error_message="Third-party domain")

    headers = {
        "User-Agent": random.choice(config.USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
    }

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout,
                                allow_redirects=True, stream=False)
            if resp.status_code >= 400:
                return FetchResult(
                    url=url, final_url=resp.url, fetch_status="HTTP_ERROR",
                    http_status=resp.status_code, text="", encoding="",
                    error_message=f"HTTP {resp.status_code}",
                )

            resp.encoding = resp.apparent_encoding
            raw = resp.content
            text, enc = _try_decode(raw)
            return FetchResult(
                url=url, final_url=resp.url, fetch_status="SUCCESS",
                http_status=resp.status_code, text=text, encoding=enc,
                error_message=None,
            )
        except requests.Timeout as e:
            last_error = str(e)
            fetch_status = "TIMEOUT"
        except requests.exceptions.SSLError as e:
            last_error = str(e)
            fetch_status = "SSL_ERROR"
            break
        except requests.exceptions.ConnectionError as e:
            last_error = str(e)
            fetch_status = "NETWORK_ERROR"

        if attempt >= max_retries:
            break

    return FetchResult(
        url=url, final_url="", fetch_status=fetch_status,
        http_status=None, text="", encoding="",
        error_message=last_error,
    )


def is_pdf_url(url: str) -> bool:
    return url.lower().rstrip("/").endswith(".pdf")
