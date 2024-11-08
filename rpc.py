""" Module for interacting with the RPC """

import time
from enum import Enum
from calibre_plugins.calibre_rpc.pypresence.presence import Presence # type: ignore


class Action(Enum):
    """
        Action types, potentially to be used for various RPC images
    """
    BROWSE = 0
    VIEW = 1
    EDIT = 2


class RPC:
    """
        Class to manage RPC
    """

    def __init__(self):
        self.connected = False
        self.presence = None

    def start(self):
        """
            Starts the RPC
        """
    
        client_id = '1163996659886346270'
        self.presence = Presence(client_id, pipe=0)
        self.presence.connect()
        self.connected = True
            

    def update(self, action, details=None, state=None):
        """
            Update the RPC

            TODO: use a switch on the action for different images
        """

        # if state is too large, only use the book's title
        if (state is not None and len(state) > 128): 
            title = state.split(' by ')[0]

            # handle case where the title still exceeds limit
            if (len(title) > 128):
                title = title[:125] + '...'

            state = title

        self.presence.update(details=details,
                            state=state,
                            large_image="calibre",
                            large_text="Calibre",
                            start=time.time(),
                            buttons=[
                                {
                                    "label": "Download Calibre", 
                                    "url": "https://calibre-ebook.com/"
                                }
                            ])


    def shutdown(self):
        """
            Shutdown the RPC
        """

        if self.connected:
            self.presence.clear()
            self.presence.close()
            self.connected = False


    def is_connected(self):
        """
            Check for if the RPC is connected to Discord
        """

        return self.connected
