# test_abc_stc_script.py

import pytest

from space_station_stc.orion_manuscript.abc_stc_script import ABC_STC_Script, UnknownCommandError

from logos_verita import *

@pytest.mark.asyncio
async def test_init():
    """test init."""

    lv = Logos_Verita_Plugin()
    assert lv.fuser_title == 'Logos Verita reporting center'
