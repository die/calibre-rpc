""" Module for storing plugin prefs """

from calibre.utils.config import JSONConfig # type: ignore # pylint: disable=import-error no-name-in-module

prefs = JSONConfig('plugins/calibre_rpc')

# Set defaults
prefs.defaults['enabled'] = True
