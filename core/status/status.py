
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

class Status:
    """Internal status module"""

    def __init__(self, bot: Red):
        self.bot = bot

    @client.async_event
    def on_ready():
        with open(os.path.dirname(os.path.abspath(__file__))+"/statusdata.json", "r") as handler:
            raw = handler.read()
        data = json.loads(raw)
        while True:
            asyncio.sleep(60)
            print("a 60 seconds cycle has passed since i connected")
            statustype = random.randint(0,2)
            if statustype == 0:
                status = random.choice(data["Playing"])
            elif statustype == 1:
                status = random.choice(data["Watching"])
            elif statustype ==2:
                status = random.choice(data["Listening"])
            await self.bot.change_presence(game=discord.Game(name=status, type=statustype))
            await asyncio.sleep(900)
 #presence types: 0 playing, 1 streaming, 2 listening to, 3 watching
