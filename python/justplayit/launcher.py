import logging
from mpd import MPDClient
from mpd.base import ConnectionError

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


MPD = MPDConnection()

def main():
    log_format = '[%(asctime)s: %(levelname)s] %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    ensure_playing()
    new_tracks = get_new_tracks()
    add_tracks_to_playlist()


def ensure_playing():
    logging.info("ensure_playing")


def get_new_tracks():
    old_tracks = set(MPD.get_tracks_on_playlist())
    logging.info("%s tracks on playlist" % (len(old_tracks)))
    logging.debug("First 10: %s", list(old_tracks)[:10])
    raise Exception
    all_tracks = get_all_track_files()
    new_tracks = []
    for each_track in all_tracks:
        if each_track not in old_tracks:
            new_tracks.append(each_track)
    return new_tracks


if __name__ == "__main__":
    main()
