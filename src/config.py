from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLEANED_DIR = DATA_DIR / "cleaned"

RAW_CSV_PATH = RAW_DIR / "system_metrics.csv"
CLEANED_CSV_PATH = CLEANED_DIR / "cleaned.csv"
DB_PATH = DATA_DIR / "valinx.db"

DEFAULT_MODEL_NAME = "isolation_forest"
DEFAULT_TOP_K = 5
