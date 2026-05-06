import re
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    lines = [re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in text.splitlines()]
    compact = [line for line in lines if line]

    # Trim short boilerplate lines from head
    head_trim = 0
    for i, line in enumerate(compact[:5]):
        if len(line) < 15:
            head_trim = i + 1
        else:
            break

    # Trim short boilerplate lines from tail
    tail_trim = len(compact)
    for i, line in enumerate(reversed(compact[-5:])):
        if len(line) < 15:
            tail_trim = len(compact) - i - 1
        else:
            break

    return "\n".join(compact[head_trim:tail_trim])


def extract_title(soup: BeautifulSoup) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    heading = soup.find(["h1", "h2"])
    return heading.get_text(" ", strip=True) if heading else ""


def extract_page_content(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")

    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    title = extract_title(soup)
    raw_text = soup.get_text("\n")
    return {
        "title": title,
        "clean_text": clean_text(raw_text),
    }


_FILE_EXTS = {".pdf", ".doc", ".docx", ".wps"}


def find_file_links(html: str, base_url: str) -> list[dict]:
    """Scan HTML for PDF/DOC/DOCX/WPS download links, resolving relative URLs."""
    soup = BeautifulSoup(html or "", "html.parser")
    file_links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href:
            continue
        full_url = urljoin(base_url, href)
        path = urlparse(full_url).path.lower()
        if any(path.endswith(ext) for ext in _FILE_EXTS):
            if full_url not in seen:
                seen.add(full_url)
                text = a.get_text(strip=True) or ""
                file_links.append({"url": full_url, "text": text})

    return file_links
