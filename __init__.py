from calibre.customize import InterfaceActionBase
from calibre.gui2.actions import InterfaceAction
from calibre_plugins.calibre_rpc.config import prefs
from calibre_plugins.calibre_rpc.rpc import RPC, Action
from calibre_plugins.calibre_rpc.hooks import view_hook, edit_hook

class CalibreRPC(InterfaceActionBase):
    name = 'Calibre RPC'
    description = 'Provides Discord Rich Presence to Calibre'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'https://github.com/die'
    version = (1, 0, 2)
    can_be_disabled = True
    minimum_calibre_version = (0, 7, 53)
    actual_plugin = 'calibre_plugins.calibre_rpc:Main'


class Main(InterfaceAction):
    RPC = None
    db = None

    def genesis(self):
        self.RPC = RPC()

        icon = get_icons('images/icon.png')
        self.qaction.setIcon(icon)
        self.qaction.setText('Calibre RPC')
        self.qaction.triggered.connect(self.toggle_rpc)

    def initialize_rpc(self):
        self.RPC.start()
        self.RPC.update(Action.BROWSE, 'Browsing Library ' + '(' + str(len(self.db.search(''))) + ' Books)')

    def toggle_rpc(self):
        # toggle the rpc using the interface
        if self.RPC.enabled():
            self.RPC.shutdown()
            self.qaction.setToolTip('Start Calibre RPC')
            prefs['enabled'] = False
        else:
            self.initialize_rpc()
            self.qaction.setToolTip('Stop Calibre RPC')
            prefs['enabled'] = True

    def initialization_complete(self):
        self.db = self.gui.current_db.new_api

        # handle presence on calibre launch
        if prefs['enabled']:
            self.initialize_rpc()
            self.qaction.setToolTip('Stop Calibre RPC')
        else:
            self.qaction.setToolTip('Start Calibre RPC')

        # hook actions
        view_hook(self)
        edit_hook(self)

    def shutting_down(self):
        # clean up rpc when calibre closes
        self.RPC.shutdown()
