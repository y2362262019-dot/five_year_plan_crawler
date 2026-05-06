import json
import os
from dataclasses import asdict, dataclass, field
from typing import Dict, List


@dataclass
class RowProgress:
    row_index: int
    status: str  # "pending" | "fetched" | "failed" | "skipped"
    local_file: str = ""


@dataclass
class Checkpoint:
    last_row: int = 0
    rows: Dict[int, RowProgress] = field(default_factory=dict)


def load(path) -> Checkpoint:
    path = str(path)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Checkpoint(
                last_row=data.get("last_row", 0),
                rows={int(k): RowProgress(**v) for k, v in data.get("rows", {}).items()},
            )
    return Checkpoint()


def save(cp: Checkpoint, path):
    path = str(path)
    tmp_path = path + ".tmp"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "last_row": cp.last_row,
        "rows": {str(k): asdict(v) for k, v in cp.rows.items()},
    }
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


def is_done(cp: Checkpoint, row_index: int) -> bool:
    return row_index in cp.rows and cp.rows[row_index].status in ("fetched", "failed", "skipped")


def mark(cp: Checkpoint, row_index: int, status: str, local_file: str = ""):
    cp.rows[row_index] = RowProgress(row_index=row_index, status=status, local_file=local_file)
    cp.last_row = max(cp.last_row, row_index)
