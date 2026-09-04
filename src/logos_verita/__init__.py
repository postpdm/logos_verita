from uuid import UUID

from litestar.config.app import AppConfig

from .controller import Logos_Verita_Controller
# take abstract
from space_station_stc.hull.plugin_abc.abc_plugin import BasePlugin

class Logos_Verita_Plugin(BasePlugin):
    # add routing
    controllers = [Logos_Verita_Controller]

    fuser_title = 'Logos Verita reporting center'
    fuser_description = 'Logos Verita is a data analysis and visualisation package. You can use it as a plugin for Space Station'
    fplugin_id = UUID( 'b4093afa-9289-4d7f-9c2b-6798dbde9fc0' )

    fstatic_req = [ ]

#