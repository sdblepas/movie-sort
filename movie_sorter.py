import re
from pathlib import Path
from typing import List, Dict

from tmdbv3api import TMDb, Search, Movie

from config import TMDB_API_KEY


tmdb = TMDb()
if TMDB_API_KEY:
    tmdb.api_key = TMDB_API_KEY

search = Search()
movie_api = Movie()


BLACKLIST = [
    r"\b(1080p|720p|480p|2160p|4k|hdr|dvdrip|brrip|bluray|blu-ray|webdl|web-dl|web|xvid|x264|x265|h264|h265|hevc|ac3|aac|dts|truehd|hdrip|hdtv|repack|extended|multi|french|vostfr|subbed|dubbed|retail|dvdscr|cam|bdrip|bdr|brr|webrip|webr)\b",
    r"\b(S\d{2}E\d{2}|S\d{2}|E\d{2})\b",
    r"\b(VF|VO|VOST|TRUEFRENCH|ENGLISH|FRENCH|VOF|VFF|VFI|MULTI)\b",
    r"\b(5\.1|7\.1|2\.0|FLAC|EAC3|TRUEHD|DTSHD|DTS-HD|DOLBY|ATMOS|X265|X264|REMUX)\b",
    r"\b(CUSTOM|PROPER|REPACK|LIMITED|UNRATED|FINAL|EXTENDED|RETAIL|COMPLETE|SUBBED)\b",
]

def extract_title(filename: str) -> str:
    name = Path(filename).stem
    cleaned = name.replace('_', ' ').replace('.', ' ')
    cleaned = re.sub(r'\s+', ' ', cleaned)
    if '-' in cleaned:
        cleaned = cleaned.rsplit('-', 1)[0]
    cleaned = re.sub('|'.join(BLACKLIST), '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\b(19|20)\d{2}\b', '', cleaned)
    cleaned = re.sub(r'\[.*?\]|\(.*?\)', '', cleaned)
    cleaned = re.sub(r"[^a-zA-ZÀ-ÿ0-9 '\-]", '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip().title()


def scan_paths(paths: List[str]) -> List[Path]:
    movie_files = []
    for p in paths:
        folder = Path(p)
        if folder.exists():
            for file in folder.rglob('*'):
                if file.suffix.lower() in {'.mp4', '.mkv', '.avi'}:
                    movie_files.append(file)
    return movie_files


def fetch_metadata(title: str) -> Dict:
    if not TMDB_API_KEY:
        return {}
    results = search.movies({'query': title})
    if results:
        movie = movie_api.details(results[0].id)
        data = {
            'title': movie.title,
            'year': movie.release_date.split('-')[0] if movie.release_date else '',
            'collection': movie.belongs_to_collection['name'] if movie.belongs_to_collection else None,
            'directors': [c['name'] for c in movie.credits['crew'] if c['job'] == 'Director'],
            'actors': [c['name'] for c in movie.credits['cast'][:3]],
        }
        return data
    return {}


def plan_sort(file: Path, meta: Dict, base: Path) -> Path:
    if meta.get('collection'):
        actor = meta['actors'][0] if meta.get('actors') else 'Unknown Actor'
        return base / meta['collection'] / actor / file.name
    if meta.get('directors'):
        return base / meta['directors'][0] / file.name
    if meta.get('year'):
        return base / meta['year'] / file.name
    return base / 'Unknown' / file.name
