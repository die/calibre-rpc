from calibre_plugins.calibre_rpc.rpc import Action


# hook for viewing a book
def view_hook(main):
    view_action = main.gui.iactions['View']._view_calibre_books

    def _view_calibre_books(book_ids):
        # call the original function to open the reader
        view_action(book_ids)

        # if there is a book to open
        if len(book_ids) > 0:
            title = main.db.field_for('title', book_ids[0], default_value='Unknown')
            author = main.db.field_for('authors', book_ids[0], default_value='Unknown Author')[0]

            if main.RPC.is_connected():
                main.RPC.update(Action.VIEW, details='Reading: ' + title, state='By: ' + author)

    main.gui.iactions['View']._view_calibre_books = _view_calibre_books


# hook for editing a book
def edit_hook(main):
    edit_action = main.gui.iactions['Tweak ePub'].do_tweak

    def do_tweak(book_id):
        # call the original function when opening the editor
        edit_action(book_id)

        title = main.db.field_for('title', book_id, default_value='Unknown')
        author = main.db.field_for('authors', book_id, default_value='Unknown Author')[0]

        if main.RPC.is_connected():
            main.RPC.update(Action.EDIT, details='Editing: ' + title, state='By: ' + author)

    main.gui.iactions['Tweak ePub'].do_tweak = do_tweak
