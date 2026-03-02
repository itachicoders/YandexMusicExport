# Yandex Music Playlist Exporter

Export any public Yandex Music playlist to a plain text file in **Artist — Track** format.

```
OTVphonk, ZERTAL - MONTAGEM PATRÃO
heapper - MONTAGEM VOZES INDICADOR (Slowed)
.fakereality, nesfot - wanna forget
семь пятниц, аляска - почему люди грустят
```

## Features

- **No dependencies** — uses Python standard library only
- **Fast** — single HTTP request, exports 500+ tracks in ~5 seconds
- Supports both `/users/` and `/iframe/playlist/` URL formats
- Auto-names the output file based on the playlist owner

## Requirements

- Python 3.10+
- Access to `music.yandex.ru` (use a VPN if blocked in your region)

## Installation

```bash
git clone https://github.com/itachicoders/YandexMusicExport.git
cd YandexMusicExport
```

No `pip install` needed.

## Usage

```bash
python export_playlist.py <URL>
```

**With a custom output file:**
```bash
python export_playlist.py <URL> --output my_playlist.txt
```

### Supported URL formats

```
https://music.yandex.ru/users/USERNAME/playlists/NUMBER
https://music.yandex.ru/iframe/playlist/USERNAME/NUMBER
```

### Example

```bash
python export_playlist.py "https://music.yandex.ru/iframe/playlist/itachicoders/3"
```

```
Плейлист: itachicoders / 3
Запрос: https://music.yandex.ru/handlers/playlist.jsx?owner=itachicoders&kinds=3&...
Готово! 5460 треков → C:\Users\...\itachicoders_playlist_3.txt
```

## Output format

Each line in the output file:
```
Artist1, Artist2 - Track Title
```

UTF-8 encoded, one track per line.

## Limitations

- **Private playlists** are not supported — the playlist must be publicly accessible
- Works only with `music.yandex.ru` (not `music.yandex.com`)

## How it works

The script calls the internal Yandex Music JSON API (`/handlers/playlist.jsx`) — the same endpoint the website uses itself. The entire playlist is returned in a single response, parsed, and written to a text file.

## License

MIT
