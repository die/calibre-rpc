import os
import time

from enum import Enum
from calibre_plugins.calibre_rpc.pypresence.presence import Presence


class Action(Enum):
    BROWSE = 0
    VIEW = 1
    EDIT = 2


class RPC:
    Presence = None

    def __init__(self):
        client_id = '1163996659886346270'
        self.Presence = Presence(client_id, pipe=0)

    def start(self):
        self.Presence.connect()

    def update(self, action, details=None, state=None):

        # TODO: use a switch on the action for different images

        self.Presence.update(details=details, state=state, large_image="calibre", large_text="Calibre",
                             start=time.time(),
                             buttons=[{"label": "Download Calibre", "url": "https://calibre-ebook.com/"}])

    def shutdown(self):
        self.Presence.clear(os.getpid())
        self.Presence.close()
