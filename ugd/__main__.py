from . import ug
from bs4 import BeautifulSoup


def main():
    # print(ug.get_chords(ug.ug_tab("3250376")))
    song = ug.get_song("3250376")
    print(song_tab_text(song))


def song_tab_text(song: ug.SongDetail):
    NEWLINE_STR = "**/**NEWLINE**/**"
    html = song.tab.replace("<br/>", NEWLINE_STR)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().replace(NEWLINE_STR, "\n")


if __name__ == "__main__":
    main()
