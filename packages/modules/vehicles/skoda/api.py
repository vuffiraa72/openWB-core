#!/usr/bin/env python3

from typing import Union
from modules.vehicles.vwgroup.vwgroup import VwGroup
from modules.vehicles.skoda import libskoda
import aiohttp
from asyncio import new_event_loop, set_event_loop
from modules.common.store import RAMDISK_PATH
from modules.vehicles.skoda.config import Skoda


class api(VwGroup):

    def __init__(self):
        super(VwGroup, self).__init__()

    # async method, called from sync fetch_soc, required because libvwid/libskoda expect async environment
    async def _fetch_soc(self,
                         conf: Skoda,
                         vehicle: int) -> Union[int, float, str]:
        self.user_id = conf.configuration.user_id
        self.password = conf.configuration.password
        self.vin = conf.configuration.vin
        self.refreshToken = conf.configuration.refreshToken
        self.replyFile = 'soc_skoda_reply_vh_' + str(vehicle)
        self.accessTokenFile = str(RAMDISK_PATH) + '/soc_skoda_accessToken_vh_' + str(vehicle)
        self.accessToken_old = {}
        self.vehicle = vehicle
        self.conf = conf

        async with aiohttp.ClientSession() as self.session:
            self.w = libskoda.skoda(self.session)
            return super().request_data(self.session)


def fetch_soc(conf: Skoda, vehicle: int) -> Union[int, float, str]:

    # prepare and call async method
    loop = new_event_loop()
    set_event_loop(loop)

    # get soc, range from server
    a = api()
    soc, range, soc_ts, soc_tsX = loop.run_until_complete(a._fetch_soc(conf, vehicle))

    return soc, range, soc_ts, soc_tsX
