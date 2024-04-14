import time
from enum import Enum
from calibre_plugins.calibre_rpc.pypresence.presence import Presence


class Action(Enum):
    BROWSE = 0
    VIEW = 1
    EDIT = 2


class RPC:
    def __init__(self):
        self.connected = False

    def start(self):
        client_id = '1163996659886346270'
        self.Presence = Presence(client_id, pipe=0)
        self.Presence.connect()
        self.connected = True
            

    def update(self, action, details=None, state=None):
        # TODO: use a switch on the action for different images
        self.Presence.update(details=details, state=state, large_image="calibre", large_text="Calibre",
                            start=time.time(),
                            buttons=[{"label": "Download Calibre", "url": "https://calibre-ebook.com/"}])


    def shutdown(self):
        if self.connected:
            self.Presence.clear()
            self.Presence.close()
            self.connected = False


    def is_connected(self):
        return self.connected
