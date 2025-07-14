import os
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / 'env.cfg'


def load_env():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key, value)


load_env()

MOVIE_PATHS = [p for p in os.getenv('MOVIE_PATHS', '').split(',') if p]
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
