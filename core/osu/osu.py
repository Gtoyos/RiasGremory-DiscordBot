
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
import datetime
import argparse
from .pippy.parser.beatmap import Beatmap
from .pippy.pp.counter import calculate_pp, Mods, calculate_pp_by_acc
from .pippy import diff

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

    @commands.guild_only()
    @commands.command()
    async def osulink(self,ctx,user: str=None):
        """Links your osu! profile

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

    @commands.guild_only()
    @commands.command()
    async def osu(self,ctx, user: str=None):
        """Gets Osu! profile stats.

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
        try:
            osudata = osudata[0] #the api gives you a list also useful to chek if user exists.
        except:
            await ctx.send("*404 username not found* :confused: ".format())
            return
        profilepage = requests.get("https://osu.ppy.sh/users/"+osudata["user_id"]).text
        soppy = BeautifulSoup(profilepage, "html.parser").find(id = "json-user")
        for k in soppy:
            jsondata= json.loads(k)
        totaltaps="{:,}".format(int(osudata["count50"])+int(osudata["count100"])+int(osudata["count300"]))
        totalscore="{:,}".format(int(osudata["total_score"]))
        rankedscore="{:,}".format(int(osudata["ranked_score"]))
        if osudata["pp_raw"] == "0":
            osudata["pp_raw"] = "0 (inactive)"
        personalinfo= ""
        playtime=str(int(int(jsondata["statistics"]["play_time"])/3600)) #only for osu mode (yet?)
        stats=("Ranked Score: "+rankedscore+"\n"+
            "Accuracy: "+osudata["accuracy"][0:6]+"%\n"+
            "Play count: "+osudata["playcount"]+"\n"+
            "Play time: "+playtime+" hours\n"+
            "Total score: "+totalscore+"\n"+
            "Total taps: "+totaltaps+"\n")
        lastvisitformatted = jsondata["lastvisit"][:-15]
        jsondata["lastvisit"] = lastvisitformatted
        for k in localosudata["personalindex"]:
            z = str(jsondata[k])
            if z != "None":
                personalinfo += localosudata["personalindex"][k]+z+"\n"
        if jsondata["avatar_url"].endswith("avatar-guest.png"):
            jsondata["avatar_url"] = "https://osu.ppy.sh/images/layout/avatar-guest.png"
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

    @commands.guild_only()
    @commands.command()
    async def taiko(self,ctx, user: str=None):
        """Gets Osu! taiko profile stats.

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
        osudata = requests.get("https://osu.ppy.sh/api/get_user?k="+localosudata["key"]+"&u="+user+"&type=string&m=1").json()
        try:
            osudata = osudata[0] #the api gives you a list also useful to chek if user exists.
        except:
            await ctx.send("*404 username not found* :confused: ".format())
            return
        profilepage = requests.get("https://osu.ppy.sh/users/"+osudata["user_id"]).text
        soppy = BeautifulSoup(profilepage, "html.parser").find(id = "json-user")
        for k in soppy:
            jsondata= json.loads(k)
        totaltaps="{:,}".format(int(osudata["count50"])+int(osudata["count100"])+int(osudata["count300"]))
        totalscore="{:,}".format(int(osudata["total_score"]))
        rankedscore="{:,}".format(int(osudata["ranked_score"]))
        if osudata["pp_raw"] == "0":
            osudata["pp_raw"] = "0 (inactive)"
        personalinfo= ""
        stats=("Ranked Score: "+rankedscore+"\n"+
            "Accuracy: "+osudata["accuracy"][0:6]+"%\n"+
            "Play count: "+osudata["playcount"]+"\n"+
            "Total score: "+totalscore+"\n"+
            "Total taps: "+totaltaps+"\n")
        lastvisitformatted = jsondata["lastvisit"][:-15]
        jsondata["lastvisit"] = lastvisitformatted
        for k in localosudata["personalindex"]:
            z = str(jsondata[k])
            if z != "None":
                personalinfo += localosudata["personalindex"][k]+z+"\n"
        if jsondata["avatar_url"].endswith("avatar-guest.png"):
            jsondata["avatar_url"] = "https://osu.ppy.sh/images/layout/avatar-guest.png"
        embed=discord.Embed(title=osudata["username"]+"'s  "+self.osuicon("taiko")+" Stats", description="Performance: **"+osudata["pp_raw"]+
            "pp**, ""*:earth_americas: #"+osudata["pp_rank"]+",  :flag_"+osudata["country"].lower()+": #"+
            osudata["pp_country_rank"]+"*", colour=ctx.guild.me.top_role.colour)
        embed.set_thumbnail(url=jsondata["avatar_url"])
        if jsondata["is_supporter"] == True:
                embed.set_footer(text=osudata["username"]+" is an Osu! supporter.", icon_url="https://i.imgur.com/NffHBo0.png")
        embed.add_field(name="Stats", value=stats, inline=False)
        embed.add_field(name="Snipes", value="{}: {}  {}: {}  {}: {}  {}: {}  {}: {}".format(self.osuicon("XH"),osudata["count_rank_ssh"],self.osuicon("X_"),osudata["count_rank_ss"],
            self.osuicon("SH"),osudata["count_rank_sh"],self.osuicon("S_"),osudata["count_rank_s"],self.osuicon("A_"),osudata["count_rank_a"]), inline=False)
        embed.add_field(name="Personal Info", value=personalinfo, inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def mania(self,ctx, user: str=None):
        """Gets Osu! mania profile stats.

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
        osudata = requests.get("https://osu.ppy.sh/api/get_user?k="+localosudata["key"]+"&u="+user+"&type=string&m=3").json()
        try:
            osudata = osudata[0] #the api gives you a list also useful to chek if user exists.
        except:
            await ctx.send("*404 username not found* :confused: ".format())
            return
        profilepage = requests.get("https://osu.ppy.sh/users/"+osudata["user_id"]).text
        soppy = BeautifulSoup(profilepage, "html.parser").find(id = "json-user")
        for k in soppy:
            jsondata= json.loads(k)
        totaltaps="{:,}".format(int(osudata["count50"])+int(osudata["count100"])+int(osudata["count300"]))
        totalscore="{:,}".format(int(osudata["total_score"]))
        rankedscore="{:,}".format(int(osudata["ranked_score"]))
        if osudata["pp_raw"] == "0":
            osudata["pp_raw"] = "0 (inactive)"
        personalinfo= ""
        stats=("Ranked Score: "+rankedscore+"\n"+
            "Accuracy: "+osudata["accuracy"][0:6]+"%\n"+
            "Play count: "+osudata["playcount"]+"\n"+
            "Total score: "+totalscore+"\n"+
            "Total taps: "+totaltaps+"\n")
        lastvisitformatted = jsondata["lastvisit"][:-15]
        jsondata["lastvisit"] = lastvisitformatted
        for k in localosudata["personalindex"]:
            z = str(jsondata[k])
            if z != "None":
                personalinfo += localosudata["personalindex"][k]+z+"\n"
        if jsondata["avatar_url"].endswith("avatar-guest.png"):
            jsondata["avatar_url"] = "https://osu.ppy.sh/images/layout/avatar-guest.png"
        embed=discord.Embed(title=osudata["username"]+"'s  "+self.osuicon("mania")+" Stats", description="Performance: **"+osudata["pp_raw"]+
            "pp**, ""*:earth_americas: #"+osudata["pp_rank"]+",  :flag_"+osudata["country"].lower()+": #"+
            osudata["pp_country_rank"]+"*", colour=ctx.guild.me.top_role.colour)
        embed.set_thumbnail(url=jsondata["avatar_url"])
        if jsondata["is_supporter"] == True:
                embed.set_footer(text=osudata["username"]+" is an Osu! supporter.", icon_url="https://i.imgur.com/NffHBo0.png")
        embed.add_field(name="Stats", value=stats, inline=False)
        embed.add_field(name="Snipes", value="{}: {}  {}: {}  {}: {}  {}: {}  {}: {}".format(self.osuicon("XH"),osudata["count_rank_ssh"],self.osuicon("X_"),osudata["count_rank_ss"],
            self.osuicon("SH"),osudata["count_rank_sh"],self.osuicon("S_"),osudata["count_rank_s"],self.osuicon("A_"),osudata["count_rank_a"]), inline=False)
        embed.add_field(name="Personal Info", value=personalinfo, inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def ctb(self,ctx, user: str=None):
        """Gets Osu! Ctb profile stats.

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
        osudata = requests.get("https://osu.ppy.sh/api/get_user?k="+localosudata["key"]+"&u="+user+"&type=string&m=2").json()
        try:
            osudata = osudata[0] #the api gives you a list also useful to chek if user exists.
        except:
            await ctx.send("*404 username not found* :confused: ".format())
            return
        profilepage = requests.get("https://osu.ppy.sh/users/"+osudata["user_id"]).text
        soppy = BeautifulSoup(profilepage, "html.parser").find(id = "json-user")
        for k in soppy:
            jsondata= json.loads(k)
        totaltaps="{:,}".format(int(osudata["count50"])+int(osudata["count100"])+int(osudata["count300"]))
        totalscore="{:,}".format(int(osudata["total_score"]))
        rankedscore="{:,}".format(int(osudata["ranked_score"]))
        if osudata["pp_raw"] == "0":
            osudata["pp_raw"] = "0 (inactive)"
        personalinfo= ""
        stats=("Ranked Score: "+rankedscore+"\n"+
            "Accuracy: "+osudata["accuracy"][0:6]+"%\n"+
            "Play count: "+osudata["playcount"]+"\n"+
            "Total score: "+totalscore+"\n"+
            "Total taps: "+totaltaps+"\n")
        lastvisitformatted = jsondata["lastvisit"][:-15]
        jsondata["lastvisit"] = lastvisitformatted
        for k in localosudata["personalindex"]:
            z = str(jsondata[k])
            if z != "None":
                personalinfo += localosudata["personalindex"][k]+z+"\n"
        if jsondata["avatar_url"].endswith("avatar-guest.png"):
            jsondata["avatar_url"] = "https://osu.ppy.sh/images/layout/avatar-guest.png"
        embed=discord.Embed(title=osudata["username"]+"'s  "+self.osuicon("ctb")+" Stats", description="Performance: **"+osudata["pp_raw"]+
            "pp**, ""*:earth_americas: #"+osudata["pp_rank"]+",  :flag_"+osudata["country"].lower()+": #"+
            osudata["pp_country_rank"]+"*", colour=ctx.guild.me.top_role.colour)
        embed.set_thumbnail(url=jsondata["avatar_url"])
        if jsondata["is_supporter"] == True:
                embed.set_footer(text=osudata["username"]+" is an Osu! supporter.", icon_url="https://i.imgur.com/NffHBo0.png")
        embed.add_field(name="Stats", value=stats, inline=False)
        embed.add_field(name="Snipes", value="{}: {}  {}: {}  {}: {}  {}: {}  {}: {}".format(self.osuicon("XH"),osudata["count_rank_ssh"],self.osuicon("X_"),osudata["count_rank_ss"],
            self.osuicon("SH"),osudata["count_rank_sh"],self.osuicon("S_"),osudata["count_rank_s"],self.osuicon("A_"),osudata["count_rank_a"]), inline=False)
        embed.add_field(name="Personal Info", value=personalinfo, inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def osurecent(self,ctx,user: str=None):
        """Gets latest Osu play.

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
        recentplay = requests.get("https://osu.ppy.sh/api/get_user_recent?k="+localosudata["key"]+"&u="+user+"&type=string&m=0&limit=1").json()
        try:
            recentplay = recentplay[0] #the api gives you a list also useful to chek if user exists.
        except:
            await ctx.send("*Username not found or there are no recent plays from: `"+user+"`*".format())
            return
        beatmap = requests.get("https://osu.ppy.sh/api/get_beatmaps?k="+localosudata["key"]+"&b="+recentplay["beatmap_id"]).json()
        beatmap = beatmap[0]
        profilepage = requests.get("https://osu.ppy.sh/users/"+recentplay["user_id"]).text
        soppy = BeautifulSoup(profilepage, "html.parser").find(id = "json-user")
        for k in soppy:
            jsondata= json.loads(k)
        if jsondata["avatar_url"].endswith("avatar-guest.png"):
            jsondata["avatar_url"] = "https://osu.ppy.sh/images/layout/avatar-guest.png"
        osudata = requests.get("https://osu.ppy.sh/api/get_user?k="+localosudata["key"]+"&u="+user+"&type=string&m=0").json()
        osudata = osudata[0]

        bpage = requests.get("https://osu.ppy.sh/b/"+recentplay["beatmap_id"]).text
        soppy = BeautifulSoup(bpage, "html.parser").find(id = "json-beatmapset")
        for k in soppy:
            juasondata= json.loads(k)

        c100 = int(bestplay["count100"])
        c50 = int(bestplay["count50"])
        misses = int(bestplay["countmiss"])
        combo = int(bestplay["maxcombo"])
        acc = (50*int(recentplay["count50"])+100*int(recentplay["count100"])+300*int(recentplay["count300"]))/(300*(int(recentplay["count300"])+int(recentplay["count100"])+int(recentplay["count50"])+int(recentplay["countmiss"])))
        score_ver = 1 #score v2 or v1

        #mod calculation
        number = int(recentplay["enabled_mods"])
        mod_list = []
        mods = ['PF', 'SO', 'FL', 'NC', 'HT', 'RX', 'DT', 'SD', 'HR', 'HD', 'EZ', 'NF']
        peppyNumbers = [16384, 4096, 1024, 576, 256, 128, 64, 32, 16, 8, 2, 1]
        for i in range(len(mods)):
            if number >= peppyNumbers[i]:
                number-= peppyNumbers[i]
                mod_list.append(mods[i])
        mod_s = "".join(mod_list)
        if recentplay["enabled_mods"] == "0":
            mod_s = ""
        data = requests.get("https://osu.ppy.sh/osu/{}".format(recentplay["beatmap_id"])).content.decode('utf8')
        btmap = Beatmap(data)
        good = btmap.parse()
        if not good:
            raise ValueError("Beatmap verify failed. "
                    "Either beatmap is not for osu! standart, or it's malformed")
        if not combo or combo > btmap.max_combo:
            combo = btmap.max_combo

        mods = Mods(mod_s)
        btmap.apply_mods(mods)
        aim, speed, stars, btmap = diff.counter.main(btmap)
        if not acc:
            pp = calculate_pp(aim, speed, btmap, misses, c100, c50, mods, combo, score_ver)
        else:
            pp = calculate_pp_by_acc(aim, speed, btmap, acc, mods, combo, misses, score_ver)

        title = "{artist} - {title} [{version}] +{mods} ({creator})".format(
            artist=btmap.artist, title=btmap.title, version=btmap.version,
            mods=mod_s, creator=btmap.creator
        )
        if stars < 1.8:
            staricon = "osueasy"
        elif stars < 2.8:
            staricon = "osunormal"
        elif stars < 3.8:
            staricon = "osuhard"
        elif stars < 4.8:
            staricon = "osuinsane"
        elif stars < 5.8:
            staricon = "osuextra"
        elif stars < 6.8:
            staricon = "osuultra"
        starsandmods = "Stars: "+str(round(stars,2))+" "+self.osuicon(staricon)+" Mods: **"+mod_s+"**"
        playscore="{:,}".format(int(recentplay["score"]))
        blinks = "[:tv:](https://osu.ppy.sh/d/"+recentplay["beatmap_id"]+") [:musical_note:](https://osu.ppy.sh/d/"+recentplay["beatmap_id"]+"n) [:heart_decoration:](osu://b/"+recentplay["beatmap_id"]+")"
        embed = discord.Embed(title=title, url="https://osu.ppy.sh/b/"+beatmap["beatmap_id"]+"&m=1")
        embed.set_author(name=user+"'s latest play. *(#"+osudata["pp_rank"]+")*", url="https://osu.ppy.sh/users/"+recentplay["user_id"], icon_url=jsondata["avatar_url"])
        embed.set_thumbnail(url=juasondata["covers"]["list@2x"])
        embed.add_field(name="Difficulty and Mods" ,value=starsandmods ,inline=True)
        embed.add_field(name="Score and Accuracy" ,value="*"+str(playscore)+" Acc: %"+str(round(pp.acc_percent, 2)),inline=True)
        embed.add_field(name="Combo" ,value="{comb}/{max_comb} with {miss} misses".format(comb=combo, max_comb=btmap.max_combo, miss=misses) ,inline=True)
        embed.add_field(name="Performance" ,value=str(pp.pp)+"**pp**" ,inline=True)
        embed.add_field(name="Date" ,value=recentplay["date"] ,inline=True)
        embed.add_field(name="Download Beatmap", value=blinks,inline=True)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def osubest(self,ctx,user: str=None):
        """Gets best Osu play.

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
        bestplay = requests.get("https://osu.ppy.sh/api/get_user_best?k="+localosudata["key"]+"&u="+user+"&type=string&m=0&limit=1").json()
        try:
            bestplay = bestplay[0] #the api gives you a list also useful to chek if user exists.
        except:
            await ctx.send("*Username not found or there are no recent plays from: `"+user+"`*".format())
            return
        beatmap = requests.get("https://osu.ppy.sh/api/get_beatmaps?k="+localosudata["key"]+"&b="+bestplay["beatmap_id"]).json()
        beatmap = beatmap[0]
        profilepage = requests.get("https://osu.ppy.sh/users/"+bestplay["user_id"]).text
        soppy = BeautifulSoup(profilepage, "html.parser").find(id = "json-user")
        for k in soppy:
            jsondata= json.loads(k)
        if jsondata["avatar_url"].endswith("avatar-guest.png"):
            jsondata["avatar_url"] = "https://osu.ppy.sh/images/layout/avatar-guest.png"
        osudata = requests.get("https://osu.ppy.sh/api/get_user?k="+localosudata["key"]+"&u="+user+"&type=string&m=0").json()
        osudata = osudata[0]

        bpage = requests.get("https://osu.ppy.sh/b/"+bestplay["beatmap_id"]).text
        soppy = BeautifulSoup(bpage, "html.parser").find(id = "json-beatmapset")
        for k in soppy:
            juasondata= json.loads(k)

        c100 = int(bestplay["count100"])
        c50 = int(bestplay["count50"])
        misses = int(bestplay["countmiss"])
        combo = int(bestplay["maxcombo"])
        acc = (50*int(bestplay["count50"])+100*int(bestplay["count100"])+300*int(bestplay["count300"]))/(300*(int(bestplay["count300"])+int(bestplay["count100"])+int(bestplay["count50"])+int(bestplay["countmiss"])))
        score_ver = 1 #score v2 or v1

        #mod calculation
        number = int(bestplay["enabled_mods"])
        mod_list = []
        mods = ['PF', 'SO', 'FL', 'NC', 'HT', 'RX', 'DT', 'SD', 'HR', 'HD', 'EZ', 'NF']
        peppyNumbers = [16384, 4096, 1024, 576, 256, 128, 64, 32, 16, 8, 2, 1]
        for i in range(len(mods)):
            if number >= peppyNumbers[i]:
                number-= peppyNumbers[i]
                mod_list.append(mods[i])
        mod_s = "".join(mod_list)
        if bestplay["enabled_mods"] == "0":
            mod_s = ""
        data = requests.get("https://osu.ppy.sh/osu/{}".format(bestplay["beatmap_id"])).content.decode('utf8')
        btmap = Beatmap(data)
        good = btmap.parse()
        if not good:
            raise ValueError("Beatmap verify failed. "
                    "Either beatmap is not for osu! standart, or it's malformed")
        if not combo or int(combo) > int(btmap.max_combo):
            combo = btmap.max_combo

        mods = Mods(mod_s)
        btmap.apply_mods(mods)
        aim, speed, stars, btmap = diff.counter.main(btmap)
        if not acc:
            pp = calculate_pp(aim, speed, btmap, misses, c100, c50, mods, combo, score_ver)
        else:
            pp = calculate_pp_by_acc(aim, speed, btmap, acc, mods, combo, misses, score_ver)

        title = "{artist} - {title} [{version}] +{mods} ({creator})".format(
            artist=btmap.artist, title=btmap.title, version=btmap.version,
            mods=mod_s, creator=btmap.creator
        )
        if stars < 1.8:
            staricon = "osueasy"
        elif stars < 2.8:
            staricon = "osunormal"
        elif stars < 3.8:
            staricon = "osuhard"
        elif stars < 4.8:
            staricon = "osuinsane"
        elif stars < 5.8:
            staricon = "osuextra"
        elif stars < 6.8:
            staricon = "osuultra"
        starsandmods = "Stars: "+str(round(stars,2))+" "+self.osuicon(staricon)+" Mods: **"+mod_s+"**"
        playscore="{:,}".format(int(bestplay["score"]))
        blinks = "[:tv:](https://osu.ppy.sh/d/"+bestplay["beatmap_id"]+") [:musical_note:](https://osu.ppy.sh/d/"+bestplay["beatmap_id"]+"n) [:heart_decoration:](osu://b/"+bestplay["beatmap_id"]+")"
        embed = discord.Embed(title=title, url="https://osu.ppy.sh/b/"+beatmap["beatmap_id"]+"&m=1")
        embed.set_author(name=user+"'s latest play. *(#"+osudata["pp_rank"]+")*", url="https://osu.ppy.sh/users/"+bestplay["user_id"], icon_url=jsondata["avatar_url"])
        embed.set_thumbnail(url=juasondata["covers"]["list@2x"])
        embed.add_field(name="Difficulty and Mods" ,value=starsandmods ,inline=True)
        embed.add_field(name="Score and Accuracy" ,value="*"+str(playscore)+" Acc: %"+str(round(pp.acc_percent, 2)),inline=True)
        embed.add_field(name="Combo" ,value="{comb}/{max_comb} with {miss} misses".format(comb=combo, max_comb=btmap.max_combo, miss=misses) ,inline=True)
        embed.add_field(name="Performance" ,value=str(pp.pp)+"**pp**" ,inline=True)
        embed.add_field(name="Date" ,value=bestplay["date"] ,inline=True)
        embed.add_field(name="Download Beatmap", value=blinks,inline=True)
        await ctx.send(embed=embed)
