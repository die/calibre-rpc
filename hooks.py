""" Module for storing hooks to GUI actions """

from calibre_plugins.calibre_rpc.rpc import Action # type: ignore # pylint: disable=import-error

def view_hook(main):
    """
        hook for viewing a book
    """

    view_action = main.gui.iactions['View']._view_calibre_books # pylint: disable=protected-access

    def _view_calibre_books(book_ids):
        # if there is a book to open
        if len(book_ids) > 0:
            title = main.db.field_for('title', book_ids[0], default_value='Unknown')
            author = main.db.field_for('authors', book_ids[0], default_value='Unknown')[0]

            if main.rpc.is_connected():
                main.rpc.update(Action.VIEW, details='Reading book', state=title + ' by ' + author)

        # call the original function to open the reader
        view_action(book_ids)

    main.gui.iactions['View']._view_calibre_books = _view_calibre_books # pylint: disable=protected-access


def edit_hook(main):
    """
        hook for editing a book
    """

    edit_action = main.gui.iactions['Tweak ePub'].do_tweak

    def do_tweak(book_id):
        title = main.db.field_for('title', book_id, default_value='Unknown')
        author = main.db.field_for('authors', book_id, default_value='Unknown')[0]

        if main.rpc.is_connected():
            main.rpc.update(Action.EDIT, details='Editing book', state=title + ' by ' + author)

        # call the original function when opening the editor
        edit_action(book_id)

    main.gui.iactions['Tweak ePub'].do_tweak = do_tweak


def edit_metadata_hook(main):
    """
        hook for editing metadata
    """
    edit_medadata_action = main.gui.iactions['Edit Metadata'].edit_metadata_for

    def edit_metadata_for(rows, book_ids, bulk=None):
        if main.rpc.is_connected():
            details = 'Editing metadata'
            if len(book_ids) > 1:
                state = 'Bulk editing (' + str(len(book_ids)) + ' books)'
            else:
                title = main.db.field_for('title', book_ids[0], default_value='Unknown')
                author = main.db.field_for('authors', book_ids[0], default_value='Unknown')[0]
                state = title + ' by ' + author

            main.rpc.update(Action.EDIT, details=details, state=state)

        # call the original function to edit metadata
        edit_medadata_action(rows, book_ids, bulk)

    main.gui.iactions['Edit Metadata'].edit_metadata_for = edit_metadata_for
