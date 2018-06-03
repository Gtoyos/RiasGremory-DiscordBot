
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

class Social:
    """Social Commands"""

    def __init__(self, bot: Red):
        self.bot = bot

    @staticmethod
    def getreaction(option, mode):
        with open(os.path.dirname(os.path.abspath(__file__))+"/reactiondata.JSON", "r") as handler:
            raw = handler.read()
            return json.loads(raw)[option][mode]

    @commands.guild_only()
    @commands.command()
    async def greet(self,ctx,user: discord.Member=None):
        """Greets a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} greets himself...weird...".format(ctx.author.mention))
            img = self.getreaction("greet", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("{} greeted me. ^^".format(ctx.author.mention))
            img = self.getreaction("greet", "rias")
        else:
            await ctx.send("{} greets {}".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("greet", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def pat(self,ctx,user: discord.Member=None):
        """Pats a user on the head"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} started patting himself".format(ctx.author.mention))
            img = self.getreaction("pat", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("{} started patting me :3".format(ctx.author.mention))
            img = self.getreaction("pat", "rias")
        else:
            await ctx.send("{} started patting {}".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("pat", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def hug(self,ctx,user: discord.Member=None):
        """Hugs a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} hugs himself, ehhh?".format(ctx.author.mention))
            img = self.getreaction("hug", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("{} hugged me <3".format(ctx.author.mention))
            img = self.getreaction("hug", "rias")
        else:
            await ctx.send("{} hugs {} <3".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("hug", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def kiss(self,ctx,user: discord.Member=None):
        """Kisses a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} is trying to kiss himself -.-".format(ctx.author.mention))
            img = self.getreaction("kiss", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("N-No {}, that would be my first kissu~".format(ctx.author.mention))
            img = self.getreaction("kiss", "rias")
        else:
            await ctx.send("{} k-k-k-kisses {} :$".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("kiss", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def cheek(self,ctx,user: discord.Member=None):
        """Kisses a user on the cheek"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} is trying to kiss his own cheek OwO".format(ctx.author.mention))
            img = self.getreaction("cheek", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("N-No {}, your breath stinks...".format(ctx.author.mention))
            img = self.getreaction("cheek", "rias")
        else:
            await ctx.send("Aww, {} kissed {} on the cheek!".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("cheek", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def hand(self,ctx,user: discord.Member=None):
        """Holds hands with a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} is holding hands with himself, what a virgin...".format(ctx.author.mention))
            img = self.getreaction("hand", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("I'm sorry {}, but I like where my hands are right now...".format(ctx.author.mention))
            img = self.getreaction("hand", "rias")
        else:
            await ctx.send("{} is holding hands with {} kyaaaa~".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("hand", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def love(self,ctx,user: discord.Member=None):
        """Shows some lewdy love to a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("Heh...{} is doing love to himself...".format(ctx.author.mention))
            img = self.getreaction("love", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("{} you bad boy, no lewdy with riasu~".format(ctx.author.mention))
            img = self.getreaction("love", "rias")
        else:
            await ctx.send("{} & {} are being 2lewd4me, g-get a room you two ._.".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("love", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def punch(self,ctx,user: discord.Member=None):
        """Starts punching a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("N-NANI?!!! {} started punching himself.".format(ctx.author.mention))
            img = self.getreaction("punch", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("Heh, nice try {}-kun~".format(ctx.author.mention))
            img = self.getreaction("punch", "rias")
        else:
            await ctx.send("The absolute madman {} started punching {}".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("punch", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def slap(self,ctx,user: discord.Member=None):
        """Starts slapping a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("N-NANI?!!! {} started punching himself.".format(ctx.author.mention))
            img = self.getreaction("slap", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("Don't even try {}-kun~".format(ctx.author.mention))
            img = self.getreaction("slap", "rias")
        else:
            await ctx.send("SHIEEET, {} started slapping the sh*t out of {}".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("slap", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.command()
    async def bully(self,ctx,user: discord.Member=None):
        """Starts bullying everyone or a user

        To bully everyone don't mention any user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("Oh no! {} started bullying everyone!".format(ctx.author.mention))
            img = self.getreaction("bully", "yes")
        elif user.id == 343156375800643594:
            await ctx.send("I'm immune to bullying, dumb {}-kun~".format(ctx.author.mention))
            img = self.getreaction("bully", "rias")
        else:
            await ctx.send("Oh no! {} started bullying {}!".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("bully", "yes"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def nobully(self,ctx,user: discord.Member=None):
        """Saves a user from a bully

        To save everyone don't mention any user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} transformed into Anti-bully Ranger! Everyone has been saved~".format(ctx.author.mention))
            img = self.getreaction("bully", "no")
        elif user.id == 343156375800643594:
            await ctx.send("I didn't need your help. But I appreciate your intention {} (>ω<)".format(ctx.author.mention))
            img = self.getreaction("bully", "norias")
        else:
            await ctx.send("{} transformed into Anti-bully Ranger! You've been saved {}".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("bully", "no"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def cuddle(self,ctx,user: discord.Member=None):
        """Starts cuddling a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} is trying to cuddle with himself, ehhh?".format(ctx.author.mention))
            img = self.getreaction("cuddle", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("{} is cuddling me owo".format(ctx.author.mention))
            img = self.getreaction("cuddle", "rias")
        else:
            await ctx.send("{} started cuddling {} <3".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("cuddle", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def stare(self,ctx,user: discord.Member=None):
        """Stares at a user"""
        if user == None or user.id == ctx.author.id:
            await ctx.send("{} is staring at himself profoundly...".format(ctx.author.mention))
            img = self.getreaction("stare", "himself")
        elif user.id == 343156375800643594:
            await ctx.send("{} is staring at me :S".format(ctx.author.mention))
            img = self.getreaction("stare", "rias")
        else:
            await ctx.send("{} is staring at {}...".format(ctx.author.mention, user.mention))
            img = random.choice(self.getreaction("stare", "0"))
        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)
        embed.set_image(url=img)
        await ctx.send(embed=embed)
