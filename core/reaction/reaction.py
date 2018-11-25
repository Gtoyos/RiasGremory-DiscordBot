
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

class Reaction(commands.Cog):
    """Reaction Commands"""

    def __init__(self, bot: Red):
        self.bot = bot

    @staticmethod
    def getreaction(option, mode):
        with open(os.path.dirname(os.path.abspath(__file__))+"/reactiondata.JSON", "r") as handler:
            raw = handler.read()
            return json.loads(raw)[option][mode]

    @commands.guild_only()
    @commands.command()
    async def smug(self,ctx,user: discord.Member=None):
        """Posts one of the smuggest qties on the web fam"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("smug", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.command()
    async def honk(self,ctx,user: discord.Member=None):
        """HONK HONK~"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("honk", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def dance(self,ctx,user: discord.Member=None):
        """Show me your moves ヽ(⌐■_■)ノ♪♬"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("dance", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def pout(self,ctx,user: discord.Member=None):
        """BAKA ONIISAMA!!!"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("pout", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def cry(self,ctx,user: discord.Member=None):
        """Oniisama is not giving me attention ;_;"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("cry", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def smile(self,ctx,user: discord.Member=None):
        """A smile a day, keeps the sadness away :3"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("smile", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def blush(self,ctx,user: discord.Member=None):
        """T-Thanks, y-you too!"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("blush", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def shrug(self,ctx,user: discord.Member=None):
        """A shrug a day, keeps the salt in bay!"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("shrug", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def thumbsup(self,ctx,user: discord.Member=None):
        """Returns a random thumbsup image!"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("thumbsup", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def sleepy(self,ctx,user: discord.Member=None):
        """Returns a random sleepy image!"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("sleepy", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def teehee(self,ctx,user: discord.Member=None):
        """Returns a random teehee image!"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("teehee", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def cute(self,ctx,user: discord.Member=None):
        """Posts cute stuff :3"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("cute", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def nani(self,ctx,user: discord.Member=None):
        """You are already dead..."""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("nani", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def awoo(self,ctx,user: discord.Member=None):
        """AWOOOOO~"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("awoo", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def thinking(self,ctx,user: discord.Member=None):
        """Really gets my almonds noggling..."""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("thinking", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def cat(self,ctx,user: discord.Member=None):
        """Gives random Cat image :3"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("cat", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def dog(self,ctx,user: discord.Member=None):
        """Gives random Dog image :3"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{}".format(ctx.author.mention))
        else:
            await ctx.send("{} {}".format(ctx.author.mention, user.mention))
        img = random.choice(self.getreaction("dog", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
