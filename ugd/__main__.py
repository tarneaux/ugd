from bs4 import BeautifulSoup
from optparse import OptionParser
from dataclasses import dataclass
import os, sys, re

from . import ug


def main():
    opts, urls = parse_args()
    print("Downloading...")

    for url in urls:
        try:
            song = get_song(url)
        except Exception as e:
            print(f"Couldn't download {url}: {e}")
            continue
        path = get_song_path(song, opts.download_dir)
        dir = os.path.dirname(path)
        if not os.path.isdir(dir):
            os.mkdir(dir)
        open(path, "w").write(song_to_text(song))


def get_song(url: str) -> ug.SongDetail:
    url = url.removeprefix("https://tabs.ultimate-guitar.com/tab/")
    if url.startswith("https://"):
        raise ValueError("I don't know about this domain.")
    return ug.get_song(url)


def get_song_path(song: ug.SongDetail, download_dir: str):
    return os.path.join(
        download_dir,
        sanitize_fn(song.artist_name),
        sanitize_fn(song.song_name) + ".txt",
    )


def sanitize_fn(fn: str) -> str:
    return re.sub(r"[^\w_. -]", "_", fn)


def parse_args():
    parser = OptionParser(usage="%prog [-d <download-dir>] <-f <filename>|<URL>>")

    parser.add_option("-f", "--file", help="Read URLs from file")
    parser.add_option(
        "-d",
        "--download-dir",
        help="Download directory",
        default=os.path.expanduser("~/ug-tabs"),
    )

    opts, args = parser.parse_args()

    if len(args) == 0 and opts.file is not None:
        urls = open(os.path.expanduser(opts.file)).read().splitlines()
    elif len(args) > 0 and opts.file is None:
        urls = args
    else:
        parser.print_usage()
        sys.exit(1)

    opts = Opts(os.path.expanduser(opts.download_dir))

    if not os.path.isdir(opts.download_dir):
        print(f"FATAL: '{opts.download_dir}' is not a directory")
        parser.print_usage()
        sys.exit(1)

    return opts, urls


@dataclass
class Opts:
    download_dir: str


def song_to_text(song: ug.SongDetail):
    NEWLINE_STR = "**/**NEWLINE**/**"
    html = song.tab.replace("<br/>", NEWLINE_STR)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().replace(NEWLINE_STR, "\n")


if __name__ == "__main__":
    main()
