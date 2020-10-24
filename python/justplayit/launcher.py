import os
import logging
from mpd import MPDClient
from mpd.base import ConnectionError

BOOKDIR = "/var/books"

class MPDConnection(object):
    def __init__(self):
        self.client = MPDClient()
        self.port = 6601
        self._connect()

    def _connect(self):
        self.client.connect("localhost", self.port)

    def _is_connected(self):
        try:
            self.client.ping()
            return True
        except ConnectionError:
            return False

    def _ensure_connected(self):
        if self._is_connected() is True:
            return True
        self._connect()
        return True

    def get_tracks_on_playlist(self):
        self._ensure_connected()
        return self.client.playlist()

    def add_to_playlist(self, to_add):
        if isinstance(to_add, str):
            to_add = [to_add]
        for eachone in to_add:
            self.client.add(eachone)


MPD = MPDConnection()

def main():
    log_format = '[%(asctime)s: %(levelname)s] %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    ensure_playing()
    new_books = get_new_books()
    logging.info("New books: %s", new_books)
    MPD.add_to_playlist(new_books)


def ensure_playing():
    logging.info("ensure_playing")


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
