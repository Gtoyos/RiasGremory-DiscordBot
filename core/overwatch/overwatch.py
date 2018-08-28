import discord
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

class Overwatch:
    """Overwatch commands"""
    def __init__(self, bot: Red):
        self.bot = bot
        self.headers = {'User-Agent': 'Rias-Gremory-Bot Python/3.x (Linux Ubuntu)'}

    def owicon(self, iconname):
        host1,host2,host3,host4 = [
            self.bot.get_guild(435125536407420929),
            self.bot.get_guild(450402584839323649),         #emojidatabase
            self.bot.get_guild(450403317051293707),
            self.bot.get_guild(450412933105713172)]
        iconlist = host1.emojis + host2.emojis + host3.emojis + host4.emojis
        return str(discord.utils.get(iconlist, name=iconname))

    @commands.guild_only()
    @commands.command()
    async def owlink(self,ctx,user: str=None):
        """Links your Overwatch profile

        Username has to be written
        case sensitive. To link your user
        name with another OW profile invoke
        this command again. To reset it leave it
        in blank.
        """
        with open(os.path.dirname(os.path.abspath(__file__))+"/overwatchdata.json", "r") as handler:
            raw = handler.read()
            localosudata = json.loads(raw)
        if user == None:
            if str(ctx.author.id) in localosudata["linkedusers"]:
                localosudata["linkedusers"].pop(str(ctx.author.id))
                await ctx.send("Your linked account has been removed. (>_<) ")
            else:
                await ctx.send("You don't have a linked account yet. Write your Battle.net username after this command to add it (≧◡≦) ")
        elif str(ctx.author.id) in localosudata["linkedusers"]:
            localosudata["linkedusers"][str(ctx.author.id)] = user
            await ctx.send("Your linked account has been changed.")
        else:
            localosudata["linkedusers"][str(ctx.author.id)] = user
            await ctx.send("Your Discord account has been linked! (⌒ω⌒)")
        with open(os.path.dirname(os.path.abspath(__file__))+"/overwatchdata.json", "w") as handler:
            json.dump(localosudata, handler)

    @commands.guild_only()
    @commands.command()
    async def owuser(self,ctx,user: str=None):
        """ Get user's OW profile info.

        Syntax: `$owuser [UsErNaMe#1234]`
        Remember that their stats must
        be public for accesing it"""
        with open(os.path.dirname(os.path.abspath(__file__))+"/overwatchdata.json", "r") as handler:
            raw = handler.read()
            localosudata = json.loads(raw)
        if user == None:
            if str(ctx.author.id) in localosudata["linkedusers"]:
                user = localosudata["linkedusers"][str(ctx.author.id)]
            else:
                user = ctx.author.name
        user = user.replace("#", "-")
        region =  "us" # 3 regions show the same info, idk why there is a region parameter
        private = False
        request_blob = requests.get("https://owapi.net/api/v3/u/"+user+"/blob", headers=self.headers)
        blob = request_blob.json()
        try:
            if blob["error"] == 404:
                await ctx.send("The username `"+user+"` was not found :confused:. Remember Battletag's names are case sensitive.")
                return
            if blob["error"] == "Private":
                private = True
        except:
            pass
        if  not blob[region]["stats"]["competitive"]["game_stats"]: #check if list is empty
            private = True
        #chek it is all good
        gblob=blob[region]["stats"]["competitive"]["overall_stats"]
        sblob=blob[region]["stats"]["competitive"]["game_stats"]
        try:
            sr_int = int(gblob["comprank"]) #BUG? what would happen if user is not ranked?
            if sr_int < 1499:
                tier="owbronze"
            elif sr_int < 1999:
                tier="owsilver"
            elif sr_int < 2499:
                tier="owgold"
            elif sr_int < 2999:
                tier="owplatinum"
            elif sr_int < 3499:
                tier="owdiamond"
            elif sr_int < 3999:
                tier="owmaster"
            elif sr_int > 4270:
                tier="owtop"
            elif sr_int > 4000:
                tier="owgrandmaster"
        except TypeError:
            tier= "Null" #supposing tier will not be 0.
        title=blob["_request"]["route"].split("/")[4].replace("-", "#")+" Current Season Stats" #Mark-1234 to Mark#1234
        if private == True:
            embed = discord.Embed(title=title, description="**"+str(gblob["comprank"])+" SR **"+self.owicon(tier) ,colour=ctx.guild.me.top_role.colour)
            embed.add_field(name="User has his current profile set to private.", value="Is this your profile? You can change it by: Options->Social->Career Profile Visiblity->Public ")
            await ctx.send(embed=embed)
            return
        level="Level: "+str(int(gblob["level"])+(int(gblob["prestige"])*100)) #level+prestige*100
        sr="**"+str(gblob["comprank"])+" SR **"+self.owicon(tier)
        description=level+", "+sr
        profileicon=gblob["avatar"]
        winrate = "*"+gblob["wins"]+"**W**, ",gblob["losses"]+"**L**, ("+gblob["win_rate"]+"% **WR**)*"
        medals =  (self.owicon("owgoldmedal")+": "+sblob["medals_gold"]+" "+self.owicon("owsilvermedal")+": "+sblob["medals_silver"]+
            " "+self.owicon("owbronzemedal")+": "+sblob["medals_bronze"])
        combat_stats = ("Damage done: *"+"{:,}".format(int(sblob["hero_damage_done"]))+",* Healing done: *"+"{:,}".format(int(sblob["healing_done"]))+
            ",* Time spent on fire: *"+sblob["time_spent_on_fire"][:4]+" hours*")
        kills = "KPD: **"+sblob["kpd"][:4]+"** Kills: *"+sblob["eliminations"]+"* Solo Kills: *"+sblob["solo_kills"]+"* Final Blows: *"+sblob["final_blows"]+"*"
        bestgame = ("Highest killstreak: *"+sblob["kill_streak_best"]+"* Most damage done: *"+"{:,}".format(int(sblob["hero_damage_done_most_in_game"]))+
            "* Most healing done: *"+"{:,}".format(int(sblob["healing_done_most_in_game"]))+"*")
        playtimeheroes=blob[region]["heroes"]["playtime"]["competitive"]
        sortedmains = sorted(playtimeheroes, key=lambda i: float(playtimeheroes[i]), reverse=True)
        mains = sortedmains[0].capitalize()+", "+sortedmains[1].capitalize()+", "+sortedmains[2].capitalize()
        embed = discord.Embed(title=title, description=description ,colour=ctx.guild.me.top_role.colour)
        embed.set_thumbnail(url=profileicon)
        embed.add_field(name="Winrate" ,value=winrate ,inline=True)
        embed.add_field(name="Medals" ,value=medals ,inline=True)
        embed.add_field(name="Combat" ,value=combat_stats, inline=True)
        embed.add_field(name="Kills" ,value=kills ,inline=True)
        embed.add_field(name="Best" ,value=bestgame ,inline=True)
        embed.add_field(name="Most Played Heroes", value=mains,inline=True)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def owmain(self,ctx,user: str=None):
        """ Get user's OW main heroes stats.

        Syntax: `$owmain [UsErNaMe#1234]`
        Remember that their stats must
        be public for accesing it"""
        with open(os.path.dirname(os.path.abspath(__file__))+"/overwatchdata.json", "r") as handler:
            raw = handler.read()
            localosudata = json.loads(raw)
        if user == None:
            if str(ctx.author.id) in localosudata["linkedusers"]:
                user = localosudata["linkedusers"][str(ctx.author.id)]
            else:
                user = ctx.author.name
        user = user.replace("#", "-")
        region =  "us" # 3 regions show the same info, idk why there is a region parameter
        private = False
        request_blob = requests.get("https://owapi.net/api/v3/u/"+user+"/blob", headers=self.headers)
        blob = request_blob.json()
        try:
            if blob["error"] == 404:
                await ctx.send("The username `"+user+"` was not found :confused:. Remember Battletag's names are case sensitive.")
                return
            if blob["error"] == "Private":
                private = True
        except:
            pass
        if not blob[region]["stats"]["competitive"]["game_stats"]: #check if list is empty
            private = True
        #chek it is all good
        gblob=blob[region]["stats"]["competitive"]["overall_stats"]
        sblob=blob[region]["stats"]["competitive"]["game_stats"]
        hblob=blob[region]["heroes"]
        try:
            sr_int = int(gblob["comprank"]) #BUG what would happen if user is not ranked?
            if sr_int < 1499:
                tier="owbronze"
            elif sr_int < 1999:
                tier="owsilver"
            elif sr_int < 2499:
                tier="owgold"
            elif sr_int < 2999:
                tier="owplatinum"
            elif sr_int < 3499:
                tier="owdiamond"
            elif sr_int < 3999:
                tier="owmaster"
            elif sr_int > 4270:
                tier="owtop"
            elif sr_int > 4000:
                tier="owgrandmaster"
        except TypeError:
            tier= "Null" #supposing tier will not be 0.
        title=blob["_request"]["route"].split("/")[4].replace("-", "#")+" Current Season Main Heroes" #Mark-1234 to Mark#1234
        if private == True:
            embed = discord.Embed(title=title, description="**"+str(gblob["comprank"])+" SR **"+self.owicon(tier) ,colour=ctx.guild.me.top_role.colour)
            embed.add_field(name="User has his current profile set to private.", value="Is this your profile? You can change it by: Options->Social->Career Profile Visiblity->Public ")
            await ctx.send(embed=embed)
            return
        playtimeheroes=hblob["playtime"]["competitive"]
        profileicon=gblob["avatar"]
        sortedmains = sorted(playtimeheroes, key=lambda i: float(playtimeheroes[i]), reverse=True)
        mainone = sortedmains[0]
        mainone_playtime = "Playtime: "+str(playtimeheroes[mainone])[:4]+" hs"
        mainone_winrate = "WR: "+str((int(hblob["stats"]["competitive"][mainone]["general_stats"]["win_percentage"])*100))[:4]+"%"
        mainone_gold = "Gold Medals: "+str(hblob["stats"]["competitive"][mainone]["general_stats"]["medals_gold"])+self.owicon("owgoldmedal")
        mainone_epl = "K/D: "+str(hblob["stats"]["competitive"][mainone]["general_stats"]["eliminations_per_life"])[:4]
        for key in hblob["stats"]["competitive"][mainone]["hero_stats"].keys():
            mainone_hero = key.replace("_", " ").capitalize()+": "+str(hblob["stats"]["competitive"][mainone]["hero_stats"][key])   #picks the first option of hero stats and breaks
            break;

        maintwo = sortedmains[1]
        maintwo_playtime = "Playtime: "+str(playtimeheroes[maintwo])[:4]+" hs"
        maintwo_winrate = "WR: "+str((int(hblob["stats"]["competitive"][maintwo]["general_stats"]["win_percentage"])*100))[:4]+"%"
        maintwo_gold = "Gold Medals: "+str(hblob["stats"]["competitive"][maintwo]["general_stats"]["medals_gold"])+self.owicon("owgoldmedal")
        maintwo_epl = "K/D: "+str(hblob["stats"]["competitive"][maintwo]["general_stats"]["eliminations_per_life"])[:4]
        for key in hblob["stats"]["competitive"][maintwo]["hero_stats"].keys():
            maintwo_hero = key.replace("_", " ").capitalize()+": "+str(hblob["stats"]["competitive"][maintwo]["hero_stats"][key])   #picks the first option of hero stats and breaks
            break;

        mainthree = sortedmains[2]
        mainthree_playtime = "Playtime: "+str(playtimeheroes[mainthree])[:4]+" hs"
        mainthree_winrate = "WR: "+str((int(hblob["stats"]["competitive"][mainthree]["general_stats"]["win_percentage"])*100))[:4]+"%"
        mainthree_gold = "Gold Medals: "+str(hblob["stats"]["competitive"][mainthree]["general_stats"]["medals_gold"])+self.owicon("owgoldmedal")
        mainthree_epl = "K/D: "+str(hblob["stats"]["competitive"][mainthree]["general_stats"]["eliminations_per_life"])[:4]
        for key in hblob["stats"]["competitive"][mainthree]["hero_stats"].keys():
            mainthree_hero = key.replace("_", " ").capitalize()+": "+str(hblob["stats"]["competitive"][mainthree]["hero_stats"][key])   #picks the first option of hero stats and breaks
            break;

        embed = discord.Embed(title=title, description="**"+str(gblob["comprank"])+" SR **"+self.owicon(tier) ,colour=ctx.guild.me.top_role.colour)
        embed.set_thumbnail(url=profileicon)
        embed.add_field(name=mainone.capitalize() ,value="{}, {}, {}, {}, {}".format(mainone_playtime,mainone_winrate,mainone_gold,mainone_epl,mainone_hero), inline=False)
        embed.add_field(name=maintwo.capitalize() ,value="{}, {}, {}, {}, {}".format(maintwo_playtime,maintwo_winrate,maintwo_gold,maintwo_epl,maintwo_hero), inline=False)
        embed.add_field(name=mainthree.capitalize() ,value="{}, {}, {}, {}, {}".format(mainthree_playtime,mainthree_winrate,mainthree_gold,mainthree_epl,mainthree_hero), inline=False)
        await ctx.send(embed=embed)
