""" Module for the main plugin logic """
from functools import partial
from qt.core import QUrl # type: ignore
from calibre_plugins.calibre_rpc.config import prefs # type: ignore
from calibre_plugins.calibre_rpc.rpc import RPC, Action # type: ignore
from calibre_plugins.calibre_rpc.hooks import view_hook, edit_hook, edit_metadata_hook # type: ignore
from calibre.gui2.actions import InterfaceAction # type: ignore
from calibre.gui2.dialogs.message_box import MessageBox # type: ignore
from calibre.gui2 import open_url # type: ignore

class CalibreRPC(InterfaceAction):
    """
        Plugin Class
    """

    name = 'Calibre RPC'
    action_spec = ('Calibre RPC', None,
                   'Provides Discord Rich Presence to Calibre', None)
    action_add_menu = True
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
        self.calibre_rpc_menu = self.qaction.menu()
        m = partial(self.create_menu_action, self.calibre_rpc_menu)
        m('calibre_rpc_reset', ('Set status to browsing'), 'search.png', triggered=self.set_browsing_action)
        self.calibre_rpc_menu.addSeparator()
        m('calibre_rpc_report_issue', ('Report an issue'), 'debug.png', triggered=self.report_issue_action)
        m('calibre_rpc_help', ('Help'), 'help.png', triggered=self.help_action)


    def set_browsing_action(self):
        """ Reset RPC to Browsing State """

        if self.rpc.is_connected():
            state = 'Browsing Library: ' + str(len(self.db.search(''))) + ' Book(s)'
            self.rpc.update(Action.BROWSE, state)


    def report_issue_action(self):
        """ Direct User to Github Repository """

        open_url(QUrl('https://github.com/die/calibre-rpc/issues'))


    def help_action(self):
        """ Direct User to Github Repository """

        open_url(QUrl('https://github.com/die/calibre-rpc'))


    def initialize_rpc(self):
        """
            Called when the plugin has finished initializing
        """

        try:
            self.rpc.start()
            self.set_browsing_action()
            return True
        except Exception as e:
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

    
    def library_changed(self, db):
        """
            Called when user switches virtual libraries
        """
        self.db = db.new_api
        self.set_browsing_action()


    def shutting_down(self):
        """
            Called when the program shuts down
        """

        try:
            self.rpc.shutdown()
        except:
            pass # we don't need to inform the user here


    def show_exception(self, exception):
        """
            Show exceptions raised in the GUI
        """
        error_dialog = MessageBox(0, "Calibre RPC", str(exception))
        error_dialog.exec()
