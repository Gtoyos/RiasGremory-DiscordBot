import dbl
import discord
from discord.ext import commands
import redbot.core
from redbot.core import Config, commands, checks, bank
from redbot.core import commands
from redbot.core.bot import Red
import urllib.request
from urllib.parse import quote_plus
import aiohttp
import asyncio
import logging

class Guildcount(commands.Cog):
    """Internal guildcount for discordbots"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM0MzE1NjM3NTgwMDY0MzU5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTIyODgxMTk0fQ.cBnP8zbeeKuyCwFxOWDENmsgf_tOe8njTD5_QwGDRYQ'  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        await self.bot.wait_until_ready()
        while self == self.bot.get_cog("Guildcount"):
            try:
                await self.dblpy.post_server_count()
                print("successfully posted server count ({})".format(len(self.bot.guilds)))
            except Exception as e:
                print("Failed to post server count.\n {}: {}".format(type(e).__name__,e))
            await asyncio.sleep(1800) #30min.

    def __unload(self):
        self.task.cancel()
