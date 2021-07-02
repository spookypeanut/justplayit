from musicpd import MPDClient
from musicpd.base import ConnectionError

class MPDConnection(object):
    def __init__(self):
        self.client = MPDClient()
        self.port = 6600
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

    def ensure_playing(self):
        self._ensure_connected()
        #TODO

    def __getattr__(self, attrname):
        return getattr(self.client, attrname)
