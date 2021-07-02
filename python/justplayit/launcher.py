import os
import logging
import time

from justplayit.mpdconnection import MPDConnection
BOOKDIR = "/var/audiobooks"
MPD = MPDConnection()
# The number of seconds between every_so_often getting run
SO_OFTEN = 20


def main():
    log_format = '[%(asctime)s: %(levelname)s] %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    lastten = 0
    while True:
        every_second()
        if time.time() - lastten > SO_OFTEN:
            lastten = time.time()
            every_so_often()
        else:
            time.sleep(1)


def every_second():
    MPD.ensure_playing()
    logging.debug(MPD.currentsong())


def every_so_often():
    new_books = get_new_books()
    logging.info("New books: %s", new_books)
    MPD.add_to_playlist(new_books)


def get_all_books():
    return sorted(os.listdir(BOOKDIR))


def get_new_books():
    old_tracks = set(MPD.playlist())
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
