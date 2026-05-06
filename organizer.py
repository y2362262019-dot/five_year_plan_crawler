import os
import re

from . import config


def _safe_name(name: str) -> str:
    return re.sub(r"[\\/:*?\"<>|]+", "_", name).strip()


_STRIP_EXTS = {".pdf", ".doc", ".docx", ".wps", ".PDF", ".DOC", ".DOCX", ".WPS"}


def _clean_title(title: str) -> str:
    """Truncate and clean title for filename use."""
    title = title.strip()
    title = re.sub(r"[\r\n\t]+", " ", title)
    title = re.sub(r"\s+", " ", title)
    # Strip file extension if the title text itself ends with one
    for ext in _STRIP_EXTS:
        if title.lower().endswith(ext.lower()):
            title = title[:-len(ext)]
            break
    if len(title) > 60:
        title = title[:60]
    return _safe_name(title)


def _city_dir(province: str, city_name: str) -> str:
    folder = _safe_name(f"{province}-{city_name}")
    base = os.path.join(config.OUTPUT_DIR, folder)
    os.makedirs(base, exist_ok=True)
    return base


def _make_filename(seq_id, province: str, city_name: str, title: str, ext: str) -> str:
    try:
        sid = int(seq_id)
    except (ValueError, TypeError):
        sid = seq_id
    parts = [str(sid), province, city_name]
    if title:
        parts.append(_clean_title(title))
    return _safe_name("-".join(parts) + ext)


def save_text(seq_id, province: str, city_name: str, title: str, text: str, url: str, encoding: str = "utf-8") -> str:
    d = _city_dir(province, city_name)
    fname = _make_filename(seq_id, province, city_name, title, ".txt")
    path = os.path.join(d, fname)

    content = f"标题：{title}\n来源：{url}\n编码：{encoding}\n\n{text}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def files_subdir(province: str, city_name: str) -> str:
    d = os.path.join(_city_dir(province, city_name), "files")
    os.makedirs(d, exist_ok=True)
    return d


def make_download_name(seq_id, province: str, city_name: str, title: str, ext: str) -> str:
    return _make_filename(seq_id, province, city_name, title, ext)
