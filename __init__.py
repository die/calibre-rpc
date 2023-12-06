from calibre.customize import InterfaceActionBase
from calibre.gui2.actions import InterfaceAction
from calibre_plugins.calibre_rpc.rpc import RPC, Action
from calibre_plugins.calibre_rpc.hooks import view_hook, edit_hook


class CalibreRPC(InterfaceActionBase):
    name = 'Calibre RPC'
    description = 'Provides Discord Rich Presence to Calibre'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'https://github.com/die'
    version = (1, 0, 1)
    can_be_disabled = True
    minimum_calibre_version = (0, 7, 53)
    actual_plugin = 'calibre_plugins.calibre_rpc:Main'


class Main(InterfaceAction):
    RPC = None
    db = None

    def genesis(self):
        # start pypresence
        self.RPC = RPC()
        self.RPC.start()

    def initialization_complete(self):
        self.db = self.gui.current_db.new_api

        # initialize presence
        self.RPC.update(Action.BROWSE, 'Browsing Library ' + '(' + str(len(self.db.search(''))) + ' Books)')

        # hook actions
        view_hook(self)
        edit_hook(self)

    def shutting_down(self):
        # clean up rpc when calibre closes
        self.RPC.shutdown()
