import time

from enum import Enum
from calibre_plugins.calibre_rpc.pypresence.presence import Presence


class Action(Enum):
    BROWSE = 0
    VIEW = 1
    EDIT = 2


class RPC:
    def __init__(self):
        self.Presence = None

    def start(self):
        if self.Presence is None:
            client_id = '1163996659886346270'
            self.Presence = Presence(client_id, pipe=0)

        self.Presence.connect()

    def update(self, action, details=None, state=None):
        if not self.enabled():
            return

        # TODO: use a switch on the action for different images

        self.Presence.update(details=details, state=state, large_image="calibre", large_text="Calibre",
                             start=time.time(),
                             buttons=[{"label": "Download Calibre", "url": "https://calibre-ebook.com/"}])

    def enabled(self):
        return self.Presence is not None

    def shutdown(self):
        if self.enabled():
            self.Presence.clear()
            self.Presence.close()
            self.Presence = None
