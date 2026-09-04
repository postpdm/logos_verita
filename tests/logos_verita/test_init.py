import pytest

from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from space_station_stc.orion_manuscript.abc_stc_script import ABC_STC_Script, UnknownCommandError

from logos_verita import *

@pytest.mark.asyncio
async def test_init():
    """test init."""

    lv = Logos_Verita_Plugin()
    assert lv.fuser_title == 'Logos Verita reporting center'

@pytest.fixture
def app() -> Litestar:
    return Litestar(
        route_handlers=[Logos_Verita_Controller],
    )


@pytest.mark.asyncio
async def test_user_homepage(app: Litestar) -> None:
    async with AsyncTestClient(app) as client:
        response = await client.get("/lv/")

    assert response.status_code == HTTP_200_OK
    assert response.text == "Hello!"

