import sys
from pathlib import Path

# Proje kök dizinini import path'e ekle
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


