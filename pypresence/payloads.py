import json
import os
import time

from typing import Union
from .utils import remove_none


class Payload:

    def __init__(self, data, clear_none=True):
        if clear_none:
            data = remove_none(data)
        self.data = data

    def __str__(self):
        return json.dumps(self.data, indent=2)

    @staticmethod
    def time():
        return time.time()

    @classmethod
    def set_activity(cls, pid: int = os.getpid(),
                     state: str = None, details: str = None,
                     start: int = None, end: int = None,
                     large_image: str = None, large_text: str = None,
                     small_image: str = None, small_text: str = None,
                     party_id: str = None, party_size: list = None,
                     join: str = None, spectate: str = None,
                     match: str = None, buttons: list = None,
                     instance: bool = True, activity: Union[bool, None] = True,
                     _rn: bool = True):

        # They should already be an int because we give typehints, but some people are fucking stupid and use
        # IDLE or some other stupid shit.
        if start:
            start = int(start)
        if end:
            end = int(end)

        if activity is None:
            act_details = None
            clear = True
        else:
            act_details = {
                    "type": 0,
                    "state": state,
                    "details": details,
                    "timestamps": {
                        "start": start,
                        "end": end
                    },
                    "assets": {
                        "large_image": large_image,
                        "large_text": large_text,
                        "small_image": small_image,
                        "small_text": small_text
                    },
                    "party": {
                        "id": party_id,
                        "size": party_size
                    },
                    "secrets": {
                        "join": join,
                        "spectate": spectate,
                        "match": match
                    },
                    "buttons": buttons,
                    "instance": instance
                }
            clear = False

        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": act_details
            },
            "nonce": '{:.20f}'.format(cls.time())
        }
        if _rn:
            clear = _rn
        return cls(payload, clear)