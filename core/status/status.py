
from random import randint
from random import choice
from enum import Enum
import random
import discord
import redbot.core
from redbot.core import Config, commands, checks, bank
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, prev_page, next_page, close_menu
from redbot.core import commands
from redbot.core.bot import Red
import urllib.request
from urllib.parse import quote_plus
import datetime
import time
import aiohttp
import asyncio
import requests
import json
import random
import os

class Status(commands.Cog):
    """Internal status module"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.task = bot.loop.create_task(self._status())

    async def _status(self):
        await self.bot.wait_until_ready()
        with open(os.path.dirname(os.path.abspath(__file__))+"/statusdata.json", "r") as handler:
            raw = handler.read()
        data = json.loads(raw)
        while self == self.bot.get_cog("Status"):
            statustype = random.randint(0,2)
            if statustype == 0:
                status = random.choice(data["Playing"])
                statustpye = 1 #discord.py changed 0 to unkown
            elif statustype == 1:
                status = random.choice(data["Watching"])
                statustype = 3 #discord.py changed watching to 3
            elif statustype ==2:
                status = random.choice(data["Listening"])
            stad = discord.Activity(name=status, type=statustype)
            await self.bot.change_presence(activity=stad)
            await asyncio.sleep(900) #15min.

    def __unload(self):
        self.task.cancel()
 #presence types: 0 playing, 1 streaming, 2 listening to, 3 watching
