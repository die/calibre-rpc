""" Module for the CalibreRPC plugin"""

from calibre_plugins.calibre_rpc.config import prefs # type: ignore # pylint: disable=import-error
from calibre_plugins.calibre_rpc.rpc import RPC, Action # type: ignore # pylint: disable=import-error
from calibre_plugins.calibre_rpc.hooks import view_hook, edit_hook, edit_metadata_hook # type: ignore # pylint: disable=import-error
from calibre.customize import InterfaceActionBase # type: ignore # pylint: disable=import-error no-name-in-module
from calibre.gui2.actions import InterfaceAction # type: ignore # pylint: disable=import-error no-name-in-module
from calibre.gui2.dialogs.message_box import MessageBox # type: ignore # pylint: disable=import-error no-name-in-module


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
    """
        Plugin Class
    """

    name = 'Calibre RPC'
    action_spec = ('Calibre RPC', None,
                   'Provides Discord Rich Presence to Calibre', None)
    rpc = None
    db = None

    def genesis(self):
        """
            Initialize plugin
        """

        self.rpc = RPC()

        icon = get_icons('images/icon.png') # type: ignore pylint: disable=undefined-variable
        self.qaction.setIcon(icon)
        self.qaction.setText('Calibre RPC')
        self.qaction.triggered.connect(self.toggle_rpc)

    def initialize_rpc(self):
        """
            Called when the plugin has finished initializing
        """

        try:
            self.rpc.start()
            state = 'Browsing Library ' + '(' + str(len(self.db.search(''))) + ' Books)'
            self.rpc.update(Action.BROWSE, state)
            return True
        except Exception as e: # pylint: disable=broad-exception-caught
            self.show_exception(e)
            return False

    def toggle_rpc(self):
        """
            Toggle the RPC using the interface
        """

        if self.rpc.is_connected():
            self.rpc.shutdown()
            self.qaction.setToolTip('Start Calibre RPC')
            prefs['enabled'] = False
        else:
            if self.initialize_rpc():
                self.qaction.setToolTip('Stop Calibre RPC')
                prefs['enabled'] = True

    def gui_layout_complete(self):
        """
            Called when the GUI has completed

            Use this so we can show exception dialogs on launch
        """

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
        edit_metadata_hook(self)

    def shutting_down(self):
        """
            Called when the program shuts down
        """

        try:
            self.rpc.shutdown()
        except: # pylint: disable=bare-except
            pass # we don't need to inform the user here

    def show_exception(self, exception):
        """
            Show exceptions raised in the GUI
        """
        error_dialog = MessageBox(0, "Calibre RPC", str(exception))
        error_dialog.exec()
