
from litestar import Controller, get
from litestar.response import Template

from litestar.exceptions import NotFoundException

from space_station_stc.hull.plugin_abc.abc_controller import BasePluginController

LV_TEMPLATES_DIR = "logos_verita_templates/"

class Logos_Verita_Controller(BasePluginController):
    path = "/lv"

    @get("/")
    async def user_homepage(self ) -> str:
        return "Hello!"

    @get("/admin_panel")
    async def admin_panel(self) -> str:
        return "Hello dummy admin panel!"

    async def plugin_health(self) -> bool:
        return True
