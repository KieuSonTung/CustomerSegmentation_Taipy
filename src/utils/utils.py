import os
from pathlib import Path


class AppPath:
    UTILS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    SRC_DIR = UTILS_DIR.parent
    ROOT_DIR = SRC_DIR.parent
    DATA_DIR = Path(SRC_DIR, "data")

    DATA_FILE_PATH = Path(DATA_DIR, "data.csv")