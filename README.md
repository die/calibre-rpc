# calibre-rpc
<img align="left" src="https://github.com/die/calibre-rpc/assets/48879283/b461e093-3d29-4042-b1e0-4091d9f37295" height="100" width="100"/>

Calibre RPC is a plugin for the e-book manager [Calibre](https://calibre-ebook.com/) to enable Discord Rich Presence.

This project was inspired by [Split](https://www.mobileread.com/forums/showthread.php?t=352476).
<br><br>
## Features
- Displays a browsing message when Calibre is opened, including the number of books in the current library.
- Displays the most recent book and its author opened by Calibre's ebook reader.
- Displays the most recent book and its author opened by Calibre's ebook editor.

## Usage

Download the [latest release](https://github.com/die/calibre-rpc/releases/latest), extract its contents, and put `Calibre RPC.zip` in `%appdata%/calibre/plugins`. 

You can also load the plugin from file in Calibre's preferences.

## Development
- Open the directory with any IDE of your choice that supports Python. For reference, this project was written with [PyCharm](https://www.jetbrains.com/pycharm/).
- Set the `CALIBRE_DEVELOP_FROM` system environment variable to a local installation of calibre's source code.
- Set the `Path` system environment variable to your local installation of Calibre, typically `C:\Program Files\Calibre2`.
- To build the plugin from source, run `calibre-customize -b  /path/to/calibre-rpc-master;` inside the terminal.
- To run Calibre in debug mode with the plugin, use the command `calibre-debug -g`.

To learn more about plugin development, there are quick tutorials found on the [calibre website](https://manual.calibre-ebook.com/creating_plugins.html).

## Goals
- Display the current page out of the total pages calculated by Calibre's ebook reader.
- Display the current file being edited in Calibre's ebook editor.
- Enable/disable the rich presence without requiring a restart.
- Update the size of the library shown by the presence in real-time.

## Credits
The image found in this README.md originates from [Calibre's source](https://github.com/kovidgoyal/calibre).

This plugin makes use of [pypresence](https://github.com/qwertyquerty/pypresence) to allow a user to showcase their current Calibre activity within [Discord](https://discord.com/).
