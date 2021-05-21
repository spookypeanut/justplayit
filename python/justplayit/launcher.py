import os
import logging
import time

from justplayit.mpdconnection import MPDConnection
BOOKDIR = "/var/books"


MPD = MPDConnection()

def main():
    log_format = '[%(asctime)s: %(levelname)s] %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    while True:
        every_second()
        if time % 10 == 0:
            every_tenseconds()
        else:
            time.sleep(1)


def every_second():
    ensure_playing()


def every_tenseconds():
    new_books = get_new_books()
    logging.info("New books: %s", new_books)
    MPD.add_to_playlist(new_books)


def ensure_playing():
    logging.debug("ensure_playing")
    # raise NotImplementedError


def get_all_books():
    return sorted(os.listdir(BOOKDIR))


def get_new_books():
    old_tracks = set(MPD.get_tracks_on_playlist())
    logging.info("%s tracks on playlist" % (len(old_tracks)))
    logging.debug("First 10: %s", list(old_tracks)[:10])
    all_books = get_all_books()
    logging.info("Books: %s", all_books)
    new_books = []
    for each_book in all_books:
        found_book = False
        for old_track in old_tracks:
            if each_book in old_track:
                found_book = True
                break
        if found_book is True:
            continue
        new_books.append(each_book)
    return new_books


if __name__ == "__main__":
    main()
