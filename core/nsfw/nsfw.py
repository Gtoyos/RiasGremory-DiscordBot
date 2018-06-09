
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
from bs4 import BeautifulSoup
import os

class Nsfw:
    """Nsfw Commands"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

    @staticmethod
    def getnsfw(option):
        with open(os.path.dirname(os.path.abspath(__file__))+"/nsfwdata.json", "r") as handler:
            raw = handler.read()
            return json.loads(raw)[option]

    @commands.guild_only()
    @commands.is_nsfw()
    @commands.command()
    async def yandere(self,ctx,user: discord.Member=None):
        """Sends a lewd image owo"""
        link = random.choice(self.getnsfw("yandere"))
        data = requests.get(link, headers=self.headers).text
        soup = BeautifulSoup(data)
        for img in soup.findAll(id = "highres"):
            image = img.get('href')
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.is_nsfw()
    @commands.command()
    async def furry(self,ctx,user: discord.Member=None):
        """Sends a furry image from e621"""
        link = random.choice(self.getnsfw("furry"))
        data = requests.get(link, headers=self.headers).text
        soup = BeautifulSoup(data)
        for img in soup.findAll(id = "highres"):
            image = img.get('href')
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.is_nsfw()
    @commands.command()
    async def yandere(self,ctx,user: discord.Member=None):
        """Sends a lewd image owo"""
        link = random.choice(self.getnsfw("yandere"))
        data = requests.get(link, headers=self.headers).text
        soup = BeautifulSoup(data)
        for img in soup.findAll(id = "highres"):
            image = img.get('href')
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.is_nsfw()
    @commands.command()
    async def nsfwgif(self,ctx,user: discord.Member=None):
        """Sends a Nsfw 3D gif"""
        link = random.choice(self.getnsfw("3dnsfwgifs"))
        data = requests.get(link, headers=self.headers).text
        soup = BeautifulSoup(data)
        for img in soup.findAll(id = "highres"):
            image = img.get('href')
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
