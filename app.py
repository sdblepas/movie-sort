from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

from config import MOVIE_PATHS, TMDB_API_KEY
from movie_sorter import extract_title, scan_paths, fetch_metadata, plan_sort

app = Flask(__name__)
BASE_DEST = Path('/sorted')


@app.route('/')
def index():
    return render_template('index.html', paths=MOVIE_PATHS, api_key=TMDB_API_KEY)


@app.route('/scan')
def scan():
    files = scan_paths(MOVIE_PATHS)
    movies = []
    for f in files:
        title = extract_title(f.name)
        meta = fetch_metadata(title)
        dest = plan_sort(f, meta, BASE_DEST)
        movies.append({'file': f, 'dest': dest, 'meta': meta})
    return render_template('scan.html', movies=movies)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7080)
