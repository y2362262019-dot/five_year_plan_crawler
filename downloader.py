import os
import random
from dataclasses import dataclass
from typing import Optional

import requests

from . import config


@dataclass
class DownloadResult:
    url: str
    file_name: str
    local_path: str
    file_size: int
    status: str  # "SUCCESS" | "FAILED"
    error_message: Optional[str]


def download_file(url: str, save_dir: str, file_name: str) -> DownloadResult:
    os.makedirs(save_dir, exist_ok=True)
    local_path = os.path.join(save_dir, file_name)

    if os.path.exists(local_path):
        size = os.path.getsize(local_path)
        return DownloadResult(url=url, file_name=file_name, local_path=local_path,
                              file_size=size, status="SUCCESS", error_message=None)

    headers = {
        "User-Agent": random.choice(config.USER_AGENTS),
        "Accept": "*/*",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=config.FETCH_TIMEOUT,
                            allow_redirects=True, stream=True)
        if resp.status_code >= 400:
            return DownloadResult(url=url, file_name=file_name, local_path="",
                                  file_size=0, status="FAILED",
                                  error_message=f"HTTP {resp.status_code}")

        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        size = os.path.getsize(local_path)
        return DownloadResult(url=url, file_name=file_name, local_path=local_path,
                              file_size=size, status="SUCCESS", error_message=None)
    except Exception as e:
        if os.path.exists(local_path):
            os.remove(local_path)
        return DownloadResult(url=url, file_name=file_name, local_path="",
                              file_size=0, status="FAILED", error_message=str(e))
