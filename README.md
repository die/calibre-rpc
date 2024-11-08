# calibre-rpc
<img align="left" src="https://github.com/die/calibre-rpc/assets/48879283/b461e093-3d29-4042-b1e0-4091d9f37295" height="100" width="100"/>

Calibre RPC is a plugin for the e-book manager [Calibre](https://calibre-ebook.com/) to enable Discord Rich Presence.

This project was inspired by [Split](https://www.mobileread.com/forums/showthread.php?t=352476).
<br><br>
## Features
- Displays a browsing message when Calibre is opened, including the number of books in the current library.
- Displays the most recent book and its author opened by Calibre's ebook reader and editor.

## Installation

1. Download the [latest release](https://github.com/die/calibre-rpc/releases/latest).
2. Go into Calibre and select Preferences -> Plugins -> Loan plugin from file -> select the zip you downloaded.
3. Restart Calibre.

## Development
### Windows
- Clone this repository and install [make](https://gnuwin32.sourceforge.net/packages/make.htm).
- Open the repository in Visual Studio Code, or your preferable IDE, and run `make install` to get the calibre source or to update your current source.
- Set the `CALIBRE_DEVELOP_FROM` system environment variable to a local installation of calibre's source code, which should now be in the directory under `calibre`.
- Set the `Path` system environment variable to your local installation of Calibre, typically `C:\Program Files\Calibre2`.
- To build the plugin from source, run `make compile` inside the terminal.
- To export the plugin as a zip, run `make zip`.

To learn more about plugin development, there are quick tutorials found on the [calibre website](https://manual.calibre-ebook.com/creating_plugins.html).

## Goals
- Display the current page out of the total pages calculated by Calibre's ebook reader.
- Update the size of the library shown by the presence in real-time.

## Credits
The image found in this README.md originates from [Calibre's source](https://github.com/kovidgoyal/calibre).
The discord icon used for this plugin is from [freepnglogos](https://www.freepnglogos.com/images/discord-logo-png-7622.html).
This plugin makes use of [pypresence](https://github.com/qwertyquerty/pypresence) to allow a user to showcase their current Calibre activity within [Discord](https://discord.com/).
