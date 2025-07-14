# Movie Sorter

A simple local web application for organizing movies on a NAS. It scans configured folders, fetches metadata from TMDb, and suggests a smart sort plan. The app can run in Docker and be configured via an `env.cfg` file.

## Features
- Add and edit movie paths
- Configure TMDb API key
- Scan movie folders
- Suggest sorting destinations using collections, directors, or release years
- Execute file moves

## Usage

1. Edit `env.cfg` with your movie paths and TMDb API key.
2. Build the Docker image and start with `docker-compose up`.
3. Access the web UI at `http://localhost:7080`.

## Development

Requires Python 3.11. Install dependencies with `pip install -r requirements.txt` and run `python app.py`.
