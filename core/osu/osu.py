
from random import randint
from random import choice
from enum import Enum
from bs4 import BeautifulSoup
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

class Osu:
    """Osu! Commands"""

    def __init__(self, bot: Red):
        self.bot = bot

    def osuicon(self, iconname):
        host1,host2,host3,host4 = [
            self.bot.get_guild(435125536407420929),
            self.bot.get_guild(450402584839323649),         #emojidatabase
            self.bot.get_guild(450403317051293707),
            self.bot.get_guild(450412933105713172)]
        iconlist = host1.emojis + host2.emojis + host3.emojis + host4.emojis
        return str(discord.utils.get(iconlist, name=iconname))

    @commands.command()
    async def osulink(self,ctx,user: str=None):
        """Links your osu! profile

        Syntax: `$osulink osuusername`
        Username doesn't need to be written
        case sensitive. To link your user
        name with another osu profile invoke
        this command again. To reset it leave it
        in blank.
        """
        with open(os.path.dirname(os.path.abspath(__file__))+"/osudata.json", "r") as handler:
            raw = handler.read()
            localosudata = json.loads(raw)
        if user == None:
            if str(ctx.author.id) in localosudata["linkedusers"]:
                localosudata["linkedusers"].pop(str(ctx.author.id))
                await ctx.send("Your linked account has been removed. (>_<) ")
            else:
                await ctx.send("You don't have a linked account yet. Write your osu! username after this command to add it (≧◡≦) ")
        elif str(ctx.author.id) in localosudata["linkedusers"]:
            localosudata["linkedusers"][str(ctx.author.id)] = user
            await ctx.send("Your linked account has been changed.")
        else:
            localosudata["linkedusers"][str(ctx.author.id)] = user
            await ctx.send("Your Discord account has been linked! (⌒ω⌒)")
        with open(os.path.dirname(os.path.abspath(__file__))+"/osudata.json", "w") as handler:
            json.dump(localosudata, handler)


    @commands.command()
    async def osu(self,ctx, user: str=None):
        """Gets Osu! profile stats.

        Syntax: `$osu usernamehere`
        Username doesn't need to be written
        case sensitive. If no user is written
        it will use your Discord name. You can
        change this by linking your osu name
        using the comand $osulink"""
        with open(os.path.dirname(os.path.abspath(__file__))+"/osudata.json", "r") as handler:
            raw = handler.read()
            localosudata = json.loads(raw)
        if user == None:
            if str(ctx.author.id) in localosudata["linkedusers"]:
                user = localosudata["linkedusers"][str(ctx.author.id)]
            else:
                user = ctx.author.name
        osudata = requests.get("https://osu.ppy.sh/api/get_user?k="+localosudata["key"]+"&u="+user+"&type=string&m=0").json()
        osudata = osudata[0] #the api gives you a list
        profilepage = requests.get("https://osu.ppy.sh/users/"+osudata["user_id"]).text
        soppy = BeautifulSoup(profilepage, "html.parser").find(id = "json-user")
        for k in soppy:
            jsondata= json.loads(k)
        totaltaps="{:,}".format(int(osudata["count50"])+int(osudata["count100"])+int(osudata["count300"]))
        totalscore="{:,}".format(int(osudata["total_score"]))
        if osudata["pp_raw"] == "0":
            osudata["pp_raw"] = "0 (inactive)"
        personalinfo= ""
        playtime=str(int(int(jsondata["statistics"]["play_time"])/120)) #only for osu mode (yet?)
        stats=("Ranked Score: "+osudata["ranked_score"]+"\n"+
            "Accuracy: "+osudata["accuracy"][0:6]+"\n"+
            "Play count: "+osudata["playcount"]+"\n"+
            "Play time: "+playtime+"\n"+
            "Total score: "+totalscore+"\n"+
            "Total taps: "+totaltaps+"\n")
        for k in localosudata["personalindex"]:
            z = str(jsondata[k])
            if z != "None":
                personalinfo += localosudata["personalindex"][k]+z+"\n"
        embed=discord.Embed(title=osudata["username"]+"'s  "+self.osuicon("osu")+" Stats", description="Performance: **"+osudata["pp_raw"]+
            "pp**, ""*:earth_americas: #"+osudata["pp_rank"]+",  :flag_"+osudata["country"].lower()+": #"+
            osudata["pp_country_rank"]+"*", colour=ctx.guild.me.top_role.colour)
        embed.set_thumbnail(url=jsondata["avatar_url"])
        if jsondata["is_supporter"] == True:
                embed.set_footer(text=osudata["username"]+" is an Osu! supporter.", icon_url="https://i.imgur.com/NffHBo0.png")
        embed.add_field(name="Stats", value=stats, inline=False)
        embed.add_field(name="Snipes", value="{}: {}  {}: {}  {}: {}  {}: {}  {}: {}".format(self.osuicon("XH"),osudata["count_rank_ssh"],self.osuicon("X_"),osudata["count_rank_ss"],
            self.osuicon("SH"),osudata["count_rank_sh"],self.osuicon("S_"),osudata["count_rank_s"],self.osuicon("A_"),osudata["count_rank_a"]), inline=True)
        embed.add_field(name="Personal Info", value=personalinfo, inline=True)
        await ctx.send(embed=embed)
