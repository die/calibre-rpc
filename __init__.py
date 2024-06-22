""" Module for the CalibreRPC plugin"""

from calibre.customize import InterfaceActionBase # type: ignore


class CalibreRPC(InterfaceActionBase):
    """ Base Class """

    name                    = 'Calibre RPC'
    description             = 'Provides Discord Rich Presence to Calibre'
    supported_platforms     = ['windows', 'osx', 'linux']
    author                  = 'https://github.com/die'
    version                 = (1, 0, 0) # hardcoded version, will not sync with Github releases
    minimum_calibre_version = (0, 7, 53)
    can_be_disabled         = True
    actual_plugin           = 'calibre_plugins.calibre_rpc.actions:CalibreRPC'

