import os
import time

from calibre.customize import InterfaceActionBase
from calibre.gui2.actions import InterfaceAction
from calibre_plugins.calibre_rpc.pypresence.presence import Presence


class CalibreRPC(InterfaceActionBase):
    name = 'Calibre RPC'
    description = 'Provides Discord Rich Presence to Calibre'
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'die'
    version = (1, 0, 0)
    can_be_disabled = True
    minimum_calibre_version = (0, 7, 53)
    actual_plugin = 'calibre_plugins.calibre_rpc:Main'


class Main(InterfaceAction):
    RPC = None
    viewed_book = 'Unknown'
    viewed_book_author = 'Unknown Author'
    edited_book = 'Unknown'
    edited_book_author = 'Unknown Author'
    db = None

    def genesis(self):
        # start pypresence
        client_id = '1163996659886346270'
        self.RPC = Presence(client_id, pipe=0)
        self.RPC.connect()

    def initialization_complete(self):
        self.db = self.gui.current_db.new_api
        # hook actions
        view_action = self.gui.iactions['View']._view_calibre_books
        edit_action = self.gui.iactions['Tweak ePub'].do_tweak

        # initialize presence
        self.update('library')

        def _view_calibre_books(book_ids):
            # call the original function to open the reader
            view_action(book_ids)
            self.last_action = 'view'

            # if there is a book to open
            if len(book_ids) > 0:
                self.viewed_book = self.db.field_for('title', book_ids[0], default_value='Unknown')
                self.viewed_book_author = self.db.field_for('authors', book_ids[0], default_value='Unknown Author')[0]
                self.update('view')

        def do_tweak(book_id):
            edit_action(book_id)
            self.edited_book = self.db.field_for('title', book_id, default_value='Unknown')
            self.edited_book_author = self.db.field_for('authors', book_id, default_value='Unknown Author')[0]
            self.update('edit')

        # set functions to actions
        self.gui.iactions['View']._view_calibre_books = _view_calibre_books
        self.gui.iactions['Tweak ePub'].do_tweak = do_tweak

    def update(self, action):
        # use different format based on the gui
        match action:
            case 'view':
                self.RPC.update(details=self.viewed_book, state='By ' + self.viewed_book_author, large_image="calibre", large_text="Calibre",
                                start=time.time(),
                                buttons=[{"label": "Download Calibre", "url": "https://calibre-ebook.com/"}])

            case 'edit':
                self.RPC.update(details='Editing ' + self.edited_book, state='By ' + self.edited_book_author, large_image="calibre",
                                large_text="Calibre",
                                start=time.time(),
                                buttons=[{"label": "Download Calibre", "url": "https://calibre-ebook.com/"}])
            case'library':
                self.RPC.update(details='Browsing Library ' + '(' + str(len(self.db.search(''))) + ' Books)', large_image="calibre",
                                large_text="Calibre", start=time.time(),
                                buttons=[{"label": "Download Calibre", "url": "https://calibre-ebook.com/"}])

    def shutting_down(self):
        # clean up rpc when calibre closes
        if self.RPC is not None:
            self.RPC.clear(os.getpid());
            self.RPC.close()
