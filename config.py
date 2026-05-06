from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_FILE = ROOT_DIR / "data" / "地级市五年规划（新版本）.xls"
OUTPUT_DIR = ROOT_DIR / "output"
CHECKPOINT_DIR = OUTPUT_DIR / "checkpoints"
CHECKPOINT_FILE = CHECKPOINT_DIR / "progress.json"

# Domains to skip (third-party, paid, or not gov)
SKIP_DOMAINS = {
    "view.officeapps.live.com",
}

FILE_EXTENSIONS_BINARY = {".pdf", ".doc", ".docx", ".wps"}
FILE_EXTENSIONS_HTML = {".html", ".htm", ".shtml", ".php", ".asp", ".aspx", ".jsp"}

# Rate limiting (seconds)
FETCH_DELAY_MIN = 2.0
FETCH_DELAY_MAX = 5.0

# Fetch settings
FETCH_TIMEOUT = 30
MAX_RETRIES = 2

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
]
