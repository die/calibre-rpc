from calibre.customize import InterfaceActionBase
from calibre.gui2.actions import InterfaceAction
from calibre.gui2.dialogs.message_box import MessageBox
from calibre_plugins.calibre_rpc.config import prefs
from calibre_plugins.calibre_rpc.rpc import RPC, Action
from calibre_plugins.calibre_rpc.hooks import view_hook, edit_hook

class CalibreRPC(InterfaceActionBase):
    name = 'Calibre RPC'
    description = 'Provides Discord Rich Presence to Calibre'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'https://github.com/die'
    version = (1, 0, 0) # hardcoded version, will not sync with Github releases
    can_be_disabled = True
    minimum_calibre_version = (0, 7, 53)
    actual_plugin = 'calibre_plugins.calibre_rpc:Main'


class Main(InterfaceAction):

    name = 'Calibre RPC'
    action_spec = ('Calibre RPC', None,
                   'Provides Discord Rich Presence to Calibre', None)
    RPC = None
    db = None

    def genesis(self):
        self.RPC = RPC()

        icon = get_icons('images/icon.png')
        self.qaction.setIcon(icon)
        self.qaction.setText('Calibre RPC')
        self.qaction.triggered.connect(self.toggle_rpc)

    def initialize_rpc(self):
        try:
            self.RPC.start()
            self.RPC.update(Action.BROWSE, 'Browsing Library ' + '(' + str(len(self.db.search(''))) + ' Books)')
            return True
        except Exception as e:
            self.show_exception(e)
            return False


    def toggle_rpc(self):
        # toggle the rpc using the interface
        if self.RPC.is_connected():
            self.RPC.shutdown()
            self.qaction.setToolTip('Start Calibre RPC')
            prefs['enabled'] = False
        else:
            if self.initialize_rpc():
                self.qaction.setToolTip('Stop Calibre RPC')
                prefs['enabled'] = True

    
    # use this so we can show exception dialogs on launch
    def gui_layout_complete(self):
        self.db = self.gui.current_db.new_api

        # handle presence on calibre launch
        if prefs['enabled']:
                if self.initialize_rpc():
                    self.qaction.setToolTip('Stop Calibre RPC')
        else:
            self.qaction.setToolTip('Start Calibre RPC')

        # hook actions
        view_hook(self)
        edit_hook(self)


    def shutting_down(self):
        try:
            # clean up rpc when calibre closes
            self.RPC.shutdown()
        except:
            pass # we don't need to inform the user here

    
    # show exceptions raised
    def show_exception(self, exception):
        error_dialog = MessageBox(0, "Calibre RPC", str(exception))
        error_dialog.exec()
