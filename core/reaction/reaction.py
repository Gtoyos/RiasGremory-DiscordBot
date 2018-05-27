
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

class Reaction:
    """Reaction Commands"""

    def __init__(self, bot: Red):
        self.bot = bot

    @staticmethod
    def getreaction(option, mode):
        with open("/home/gtoyos/.local/lib/python3.6/site-packages/redbot/cogs/reaction/reactiondata.json", "r") as handler:
            raw = handler.read()
            return json.loads(raw)[option][mode]

    @commands.guild_only()
    @commands.command()
    async def greet(self,ctx,user: discord.Member=None):
        if user == None or user.id == author.id:
            await ctx.send("{} greets himself...weird...".format(author.mention))
            img = random.choice(self.getreaction("greet", "himself"))
        elif user.id == 343156375800643594:
            await ctx.send("{} greeted me. :3".format(author.mention))
            img = random.choice(self.getreaction("greet", "0"))
        else:
            await ctx.send("{} greets {}".format(author.mention, user.mention))
            img = random.choice(self.getreaction("greet", "0"))
        embed = discord.embed(colour=notify_channel.guild.me.top_role.colour)
        embed.set_image(img)
        await ctx.send(embed=embed)
