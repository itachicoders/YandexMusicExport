"""
Экспорт плейлиста Яндекс Музыки в текстовый файл.

Использование:
    python export_playlist.py <URL> [--output FILE]

Примеры URL:
    https://music.yandex.ru/iframe/playlist/USERNAME/NUMBER
    https://music.yandex.ru/users/USERNAME/playlists/NUMBER
"""

import sys
import re
import json
import argparse
import urllib.request
import urllib.parse
from pathlib import Path


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}


def fetch(url: str, extra: dict = {}) -> str:
    req = urllib.request.Request(url, headers={**HEADERS, **extra})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_url(url: str) -> tuple:
    for p in [
        r'music\.yandex\.[a-z]+/(?:iframe/)?playlist/([^/?#]+)/(\d+)',
        r'music\.yandex\.[a-z]+/users/([^/?#]+)/playlists/(\d+)',
    ]:
        m = re.search(p, url)
        if m:
            return m.group(1), m.group(2)
    return None, None


def safe_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip() or "playlist"


def format_track(track: dict) -> str | None:
    title = (track.get("title") or "").strip()
    if not title:
        return None
    artists = track.get("artists") or []
    names = [a["name"] for a in artists if isinstance(a, dict) and a.get("name")]
    return f"{', '.join(names) or 'Unknown'} - {title}"


def fetch_tracks(owner: str, kind: str) -> list:
    params = urllib.parse.urlencode({
        "owner": owner,
        "kinds": kind,
        "light": "false",
        "lang": "ru",
        "external-domain": "music.yandex.ru",
        "overembed": "false",
    })
    url = f"https://music.yandex.ru/handlers/playlist.jsx?{params}"
    print(f"Запрос: {url}")
    data = json.loads(fetch(url, {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://music.yandex.ru/users/{owner}/playlists/{kind}",
    }))
    return (data.get("playlist") or {}).get("tracks") or []


def export_playlist(url: str, output_file: str | None = None):
    owner, kind = parse_url(url)
    if not owner:
        print("Не удалось распознать ссылку.")
        print("  https://music.yandex.ru/iframe/playlist/USERNAME/NUMBER")
        print("  https://music.yandex.ru/users/USERNAME/playlists/NUMBER")
        sys.exit(1)

    print(f"Плейлист: {owner} / {kind}")

    try:
        tracks = fetch_tracks(owner, kind)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Возможные причины: плейлист приватный или нет доступа к music.yandex.ru")
        sys.exit(1)

    if not tracks:
        print("Треки не найдены.")
        sys.exit(1)

    lines = [f for t in tracks if (f := format_track(t))]

    if output_file is None:
        output_file = f"{safe_filename(owner)}_playlist_{kind}.txt"

    Path(output_file).write_text("\n".join(lines), encoding="utf-8")
    print(f"Готово! {len(lines)} треков → {Path(output_file).resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Экспорт плейлиста Яндекс Музыки",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("url", help="Ссылка на плейлист")
    parser.add_argument("--output", "-o", help="Имя выходного файла")
    args = parser.parse_args()
    export_playlist(args.url, output_file=args.output)


if __name__ == "__main__":
    main()
