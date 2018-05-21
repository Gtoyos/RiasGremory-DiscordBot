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
#DEVELOP. suppreg moved to loldata.json and many more. CHANGE ALL JSON FILES!!!
class Lol:

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def lol(self, ctx):
        """League of Legends commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @staticmethod
    def loldata(option):
        with open("loldata.json") as handler:
            raw = handler.read()
            if option == "key":
                return json.loads(raw)["token"]["0"]
            elif option == "champsid":
                return json.loads(raw)["champsid"]
            elif option == "junglersid":
                return json.loads(raw)["junglersid"]
            elif option == "region":
                return json.loads(raw)["region"]
            elif option == "map":
                return json.loads(raw)["map"]
            elif option == "gamemode":
                return json.loads(raw)["gamemode"]
            elif option == "elo":
                return json.loads(raw)["elo"]
            elif option == "version":
                return requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

    @lol.command()
    async def summ(self, ctx, *args):
        """Obtains Summoner info.

        syntax: $lol summ [reg] [name].
        Summoner's name doesn't need to be
        written case sensitive nor with spaces"""

        [x.lower() for x in args]
        if len(args) == 0:
            await ctx.send(":x: *Missing Parameters: Region & Summoner*".format())
            return
        region = args[0]
        if region not in self.loldata("region"):
            await ctx.send(":x: *The region code isn't correct senpai 7w7*".format())
            return
        if len(args) < 2:
            await ctx.send(":x: *Summoner name missing or incorrect format.*".format())
            return
        if len(args) > 2:
            summ = "".join(args[1:69])
        if len(args) == 2:
            summ = args[1]
        #reponse error handler
        summhandler = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summ+"?api_key="+self.loldata("key"))
        if summhandler.status_code == 429:
            await ctx.send("*Too much requests, pls try again in 2 minutes* :sweat: ".format())
            return
        elif summhandler.status_code == 404:
            await ctx.send("*404 Summoner Not Found* :confused: ".format())
            return
        elif summhandler.status_code == 500 or summhandler.status_code == 503:
            await ctx.send("*I'm afraid the Riot API is unavailable at the moment* :confused: ".format())
            return
        summdata = summhandler.json()
        summidstr = str(summdata["id"])
        elodatah = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/league/v3/positions/by-summoner/"+summidstr+"?api_key="+self.loldata("key"))
        elodata = elodatah.json()
        malvlh = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/"+summidstr+"?api_key="+self.loldata("key"))
        malvl = malvlh.json()
        maestryh = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/"+summidstr+"?api_key="+self.loldata("key"))
        maestry = maestryh.json()
        if elodatah.status_code == 503 or malvlh.status_code == 503 or maestryh.status_code == 503:
            await self.bot.say("*The Riot API is currently unavailable. Please try again later :persevere:*".format())
            return
        #main role and champs
        mainchamps = []
        mains = maestry[0:3]
        champsid = [d["championId"] for d in mains]
        for a in champsid:
            mainchamps.append(self.loldata("champsid")[str(a)]) #mainchamps
        rolcounts = {'Assassin': 0, 'Marksman': 0, 'Fighter': 0, 'Mage': 0, 'Support': 0, 'Tank': 0, 'Jungler': 0}
        jun = 0
        for champ in mainchamps:
            rol = (requests.get("http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/data/en_US/champion/"+champ+".json").json()['data'][champ]["tags"])
            for i in rol:
                rolcounts[i] = rolcounts.get(i, 0) + 1
        for champi in champsid:
            try:
                if str(champi) in self.loldata("junglersid"):
                    jun = jun + 1
            except:
                continue;
        rolcounts['Jungler'] = jun
        if int(rolcounts["Jungler"]) >= 2:
            mainrole = "JG"
        elif int(rolcounts["Marksman"]) >= 2:
            mainrole = "ADC"
        elif int(rolcounts["Fighter"]) >= 2 and int(rolcounts["Assassin"]) >= 2 and int(rolcounts["Jungler"]) >= 1:
            mainrole = "JG"
        elif int(rolcounts["Fighter"]) >= 2 and int(rolcounts["Assassin"]) >= 2:
            mainrole = "TOP"
        else:
            maxrol = max(rolcounts, key=rolcounts.get)
            if maxrol == "Support":
                mainrole = "SUP"
            elif maxrol == "Marksman":
                mainrole = "ADC"
            elif maxrol == "Mage":
                mainrole = "MID"
            elif maxrol == "Tank":
                mainrole = "TOP"
            elif maxrol == "Assassin":
                mainrole = "MID"
            elif maxrol == "Jungler":
                mainrole = "JG"
            elif maxrol == "Fighter":
                mainrole = "TOP"
        summdataicon = str(summdata["profileIconId"])
        summicon = "http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/img/profileicon/"+summdataicon+".png"
        if len(elodata) == 0:
            soloq = "Unranked"
            flex = "Unranked"
            winrate = "0%"
            totalwins = 0
            totallosses = 0                            #checkplacementelo
        elif len(elodata) == 1:
            if "RANKED_SOLO_5x5" in elodata[0]["queueType"]:
                soloq = elodata[0]["tier"]+" "+elodata[0]["rank"]
                winrate = (elodata[0]["wins"])*100/(elodata[0]["wins"]+elodata[0]["losses"])
                totalwins = elodata[0]["wins"]
                totallosses = elodata[0]["losses"]
                flex = "Unranked"
            if "RANKED_FLEX_SR" in elodata[0]["queueType"]:
                flex= elodata[0]["tier"]+" "+elodata[0]["rank"]
                winrate = (elodata[0]["wins"])*100/(elodata[0]["wins"]+elodata[0]["losses"])
                totalwins = elodata[0]["wins"]
                totallosses = elodata[0]["losses"]
                soloq = "Unranked"
        elif len(elodata) == 2:
            if "RANKED_FLEX_SR" in elodata[0]["queueType"]:
                flex= elodata[0]["tier"]+" "+elodata[0]["rank"]
                soloq= elodata[1]["tier"]+" "+elodata[1]["rank"]
            elif "RANKED_SOLO_5x5" in elodata[0]["queueType"]:
                soloq= elodata[0]["tier"]+" "+elodata[0]["rank"]
                flex= elodata[1]["tier"]+" "+elodata[1]["rank"]
            winrate = ((elodata[0]["wins"]+elodata[1]["wins"])*100/((elodata[0]["wins"]+elodata[1]["wins"])+(elodata[0]["losses"]+elodata[1]["losses"])))
            totalwins = elodata[0]["wins"] + elodata[1]["wins"]
            totallosses = elodata[0]["losses"] + elodata[1]["losses"]
        if soloq.startswith("CHALLENGER") or flex.startswith("CHALLENGER"):
            color = "0xffff00"
        elif soloq.startswith("MASTER") or flex.startswith("MASTER"):
            color = "0xff8600"
        elif soloq.startswith("DIAMOND") or flex.startswith("DIAMOND"):
            color = "0x00ffff"
        elif soloq.startswith("PLATINUM") or flex.startswith("PLATINUM"):
            color = "0x97ffff"
        elif soloq.startswith("GOLD") or flex.startswith("GOLD"):
            color = "0xffff80"
        elif soloq.startswith("SILVER") or flex.startswith("SILVER"):
            color = "0x494949"
        elif soloq.startswith("BRONZE") or flex.startswith("BRONZE"):
            color = "0x804000"
        else:
            color = "0xffffff"
        mainchampsstr = ", ".join(mainchamps)
        colorh = int(color, 16)
        opgg = "http://"+self.loldata("region")[region]+".op.gg/summoner/userName="+summdata["name"].replace(" ", "")                                                   #embedformatforv3?
        lolking = "http://www.lolking.net/summoner/"+self.loldata("region")[region]+"/"+summidstr+"/"+summdata["name"].replace(" ", "")+"#/profile"
        links = "[op.gg]({}) & [Lolking]({})".format(opgg, lolking)
        embed=discord.Embed(title=summdata["name"], description="Main"+" "+mainrole+" "+mainchampsstr, color=colorh)
        embed.set_thumbnail(url=summicon)
        embed.add_field(name="Solo/Duo", value=soloq, inline=True)
        embed.add_field(name="Flex", value=flex, inline=True)
        embed.add_field(name="Winrate", value=winrate, inline=True)
        embed.add_field(name="Games", value="W"+(str(totalwins))+" "+"L"+(str(totallosses)), inline=True)
        embed.add_field(name="Maestry Score", value=malvl, inline=True)
        embed.add_field(name="Summoner Level", value=summdata["summonerLevel"], inline=True)
        embed.add_field(name="More Info", value=links, inline=True)
        embed.set_footer(text='Summoner ID:'+" "+summidstr)
        await ctx.send(embed=embed)

    @lol.command(no_pm=True)
    async def game(self, ctx, *args):
        """Obtains Summoner's game info.

        syntax: $lol game [reg] [name].
        Summoner's name doesn't need to be
        written case sensitive nor with spaces"""

        [x.lower() for x in args]
        if len(args) == 0:
            await ctx.send(":x: *Missing Parameters: Region & Summoner*".format())
            return
        region = args[0]
        if region not in self.loldata("region"):
            await ctx.send(":x: *The region code isn't correct senpai 7w7*".format())
            return
        if len(args) < 2:
            await ctx.send(":x: *Summoner name missing or incorrect format.*".format())
            return
        if len(args) > 2:
            summ = "".join(args[1:69]) #python characteristic
        if len(args) == 2:
            summ = args[1]
        summhandler = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/summoner/v3/summoners/by-name/"+summ+"?api_key="+self.loldata("key"))
        if summhandler.status_code == 429:
            await ctx.send("*I'm receiving too many requests, pls try again in 2 minutes* :sweat: ".format())
            return
        elif summhandler.status_code == 404:
            await ctx.send("*404 Summoner Not Found* :confused: ".format())
            return
        elif summhandler.status_code == 500 or summhandler.status_code == 503:
            await ctx.send("*I'm afraid the Riot API is unavailable at the moment* :confused: ".format())
            return
        summdata = summhandler.json()
        summidstr = str(summdata["id"])
        gamehandler = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/"+summidstr+"?api_key="+self.loldata("key"))
        if gamehandler.status_code == 404:
            await ctx.send("*Summoner isn't currently in a game* :expressionless: ".format()) #possible bug
            return
        elif gamehandler.status_code == 503 or summhandler.status_code == 503:
            await ctx.send("*The Riot API is currently unavailable. Please try again later :persevere:*".format())
            return
        gamedata = gamehandler.json()
        gametype = self.loldata("gamemode")[str(gamedata["gameQueueConfigId"])]
        maptype = self.loldata("map")[str(gamedata["mapId"])]
        playersdata = []
        for summ in gamedata["participants"]:
            preplayer = [summ["teamId"],summ["championId"],summ["summonerId"], summ["summonerName"]]                            #player data key:  [team, champ, summid, name]
            playersdata.append(preplayer)
        iterator = 0
        for player in playersdata:
            leaguehandler = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/league/v3/positions/by-summoner/"+str(player[2])+"?api_key="+self.loldata("key"))
            if leaguehandler.status_code == 503:
                await ctx.send("*The Riot API is currently unavailable. Please try again later :persevere:*".format())
                return
            elif leaguehandler.status_code == 429:
                await ctx.send("*Too much requests, pls try again in 2 minutes* :sweat: ".format())
                return
            elodata = leaguehandler.json()
            # modified form summoner command
            if len(elodata) == 0:
                soloq = "Unranked"
                flex = "Unranked"
                winrate = 0
                totalwins = 0                               #nice
                totallosses = 0                            #checkplacementelo
            elif len(elodata) == 1:
                if "RANKED_SOLO_5x5" in elodata[0]["queueType"]:
                    soloq = elodata[0]["tier"]+" "+elodata[0]["rank"]
                    winrate = round(int(elodata[0]["wins"])*100/(elodata[0]["wins"]+elodata[0]["losses"]), 1)
                    totalwins = elodata[0]["wins"]
                    totallosses = elodata[0]["losses"]
                    flex = "Unranked"
                if "RANKED_FLEX_SR" in elodata[0]["queueType"]:
                    flex= elodata[0]["tier"]+" "+elodata[0]["rank"]
                    winrate = round(int(elodata[0]["wins"])*100/(elodata[0]["wins"]+elodata[0]["losses"]), 1)
                    totalwins = elodata[0]["wins"]
                    totallosses = elodata[0]["losses"]
                    soloq = "Unranked"
            elif len(elodata) == 2:
                if "RANKED_FLEX_SR" in elodata[0]["queueType"]:
                    flex= elodata[0]["tier"]+" "+elodata[0]["rank"]
                    soloq= elodata[1]["tier"]+" "+elodata[1]["rank"]
                elif "RANKED_SOLO_5x5" in elodata[0]["queueType"]:
                    soloq= elodata[0]["tier"]+" "+elodata[0]["rank"]
                    flex= elodata[1]["tier"]+" "+elodata[1]["rank"]                   #warning 0&1 are correct? - flexible order patch added
                winrate = round(int((elodata[0]["wins"]+elodata[1]["wins"])*100/((elodata[0]["wins"]+elodata[1]["wins"])+(elodata[0]["losses"]+elodata[1]["losses"]))), 1)
                totalwins = elodata[0]["wins"] + elodata[1]["wins"]
                totallosses = elodata[0]["losses"] + elodata[1]["losses"]
            # modified from summoner command
            elolist = [soloq, flex, winrate, totalwins, totallosses]
            playersdata[iterator].extend(elolist)                           #index:               0     1       2      3      4     5       6       7           8
            iterator = iterator + 1                                         #player data key:  [team, champ, summid, name, soloq, flex, winrate, totalwins, totallosses]
        soloqelo = []
        flexelo = []
        intelo = self.loldata("elo")
        for av in playersdata:              #average elo
            if av[4] in intelo:
                soloqelo.append(intelo[av[4]])
            if av[5] in intelo:
                flexelo.append(intelo[av[5]])
        totalsolo = int(round(sum(soloqelo)/len(soloqelo)))
        totalflex = int(round(sum(flexelo)/len(flexelo)))
        intelo = dict([[v,k] for k,v in intelo.items()])#dictionary inverted
        avgsoloelo = intelo[totalsolo]
        avgflexelo = intelo[totalflex]
        bestelo = max(totalsolo, totalflex)
        if intelo[bestelo].startswith("CHALLENGER"):
            color = "0xffff00"
            icon = "http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/img/profileicon/3206.png"
        elif intelo[bestelo].startswith("MASTER"):
            color = "0xff8600"
            icon = "http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/img/profileicon/3202.png"
        elif intelo[bestelo].startswith("DIAMOND"):
            color = "0x00ffff"
            icon = "http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/img/profileicon/3199.png"
        elif intelo[bestelo].startswith("PLATINUM"):
            color = "0x97ffff"
            icon = "http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/img/profileicon/3196.png"
        elif intelo[bestelo].startswith("GOLD"):
            color = "0xffff80"
            icon = "http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/img/profileicon/3193.png"
        elif intelo[bestelo].startswith("SILVER"):
            color = "0x494949"
            icon = "http://ddragon.leagueoflegends.com/cdn/"+self.loldata("version")+"/img/profileicon/3190.png"
        elif intelo[bestelo].startswith("BRONZE"):
            color = "0x804000"
            icon = "http://ddragon.leagueoflegends.com/cdn/"+self.self.loldata("version")+"/img/profileicon/3189.png"
        else:
            color = "0xffffff"
            icon = "https://vignette.wikia.nocookie.net/leagueoflegends/images/8/89/UnrankedBadge.png"
        colorh = int(color, 16)
        avgsoloelolist = avgsoloelo.split(" ")
        avgsololeague = avgsoloelo[0].lower().capitalize()
        avgsolonum = avgsoloelolist[1]
        avgflexelolist = avgflexelo.split(" ")
        avgflexleague = avgflexelo[0].lower().capitalize()
        avgflexnum = avgflexelolist[1]
        champsid = self.loldata("champsid")
        for aw in playersdata:
            if aw[4].startswith("BRONZE"):
                if aw[4].endswith("V"):
                    aw[4] = "B5"
                elif aw[4].endswith("IV"):
                    aw[4] = "B4"
                elif aw[4].endswith("III"):
                    aw[4] = "B3"
                elif aw[4].endswith("II"):
                    aw[4] = "B2"
                elif aw[4].endswith("I"):
                    aw[4] = "B1"
            elif aw[4].startswith("SILVER"):
                if aw[4].endswith("V"):
                    aw[4] = "S5"
                elif aw[4].endswith("IV"):
                    aw[4] = "S4"
                elif aw[4].endswith("III"):
                    aw[4] = "S3"
                elif aw[4].endswith("II"):
                    aw[4] = "S2"
                elif aw[4].endswith("I"):
                    aw[4] = "S1"
            elif aw[4].startswith("GOLD"):
                if aw[4].endswith("V"):
                    aw[4] = "G5"
                elif aw[4].endswith("IV"):
                    aw[4] = "G4"
                elif aw[4].endswith("III"):
                    aw[4] = "G3"
                elif aw[4].endswith("II"):
                    aw[4] = "G2"
                elif aw[4].endswith("I"):
                    aw[4] = "G1"
            elif aw[4].startswith("PLATINUM"):
                if aw[4].endswith("V"):
                    aw[4] = "P5"
                elif aw[4].endswith("IV"):
                    aw[4] = "P4"
                elif aw[4].endswith("III"):
                    aw[4] = "P3"
                elif aw[4].endswith("II"):
                    aw[4] = "P2"
                elif aw[4].endswith("I"):
                    aw[4] = "P1"
            elif aw[4].startswith("DIAMOND"):
                if aw[4].endswith("V"):
                    aw[4] = "D5"
                elif aw[4].endswith("IV"):
                    aw[4] = "D4"
                elif aw[4].endswith("III"):
                    aw[4] = "D3"
                elif aw[4].endswith("II"):
                    aw[4] = "D2"
                elif aw[4].endswith("I"):
                    aw[4] = "D1"
            elif aw[4].startswith("MASTER"):
                aw[4] = "M"
            elif aw[4].startswith("CHALLENGER"):
                aw[4] = "C"
            else:
                aw[4] = "U"
        for aw in playersdata:
            if aw[5].startswith("BRONZE"):
                if aw[5].endswith("V"):
                    aw[5] = "B5"
                elif aw[5].endswith("IV"):
                    aw[5] = "B4"
                elif aw[5].endswith("III"):
                    aw[5] = "B3"
                elif aw[5].endswith("II"):
                    aw[5] = "B2"
                elif aw[5].endswith("I"):
                    aw[5] = "B1"
            elif aw[5].startswith("SILVER"):
                if aw[5].endswith("V"):
                    aw[5] = "S5"
                elif aw[5].endswith("IV"):
                    aw[5] = "S4"
                elif aw[5].endswith("III"):
                    aw[5] = "S3"
                elif aw[5].endswith("II"):
                    aw[5] = "S2"
                elif aw[5].endswith("I"):
                    aw[5] = "S1"
            elif aw[5].startswith("GOLD"):
                if aw[5].endswith("V"):
                    aw[5] = "G5"
                elif aw[5].endswith("IV"):
                    aw[5] = "G4"
                elif aw[5].endswith("III"):
                    aw[5] = "G3"
                elif aw[5].endswith("II"):
                    aw[5] = "G2"
                elif aw[5].endswith("I"):
                    aw[5] = "G1"
            elif aw[5].startswith("PLATINUM"):
                if aw[5].endswith("V"):
                    aw[5] = "P5"
                elif aw[5].endswith("IV"):
                    aw[5] = "P4"
                elif aw[5].endswith("III"):
                    aw[5] = "P3"
                elif aw[5].endswith("II"):
                    aw[5] = "P2"
                elif aw[5].endswith("I"):
                    aw[5] = "P1"
            elif aw[5].startswith("DIAMOND"):
                if aw[5].endswith("V"):
                    aw[5] = "D5"
                elif aw[5].endswith("IV"):
                    aw[5] = "D4"
                elif aw[5].endswith("III"):
                    aw[5] = "D3"
                elif aw[5].endswith("II"):
                    aw[5] = "D2"
                elif aw[5].endswith("I"):
                    aw[5] = "D1"
            elif aw[5].startswith("MASTER"):
                aw[5] = "M"
            elif aw[5].startswith("CHALLENGER"):
                aw[5] = "C"
            else:
                aw[5] = "U"
        for aw in playersdata:
            aw[6] = str(aw[6])
            aw[7] = str(aw[7])
            aw[8] = str(aw[8])
        embed=discord.Embed(title=maptype+" "+gametype+" "+"Game", description="Average Elo: "+"Solo/Duo:"+" "+avgsololeague+" "+avgsolonum+" , Flex: "+avgflexleague+" "+avgflexnum, color=colorh)
        embed.set_thumbnail(url=icon)
        embed.add_field(name=playersdata[0][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[0][1])]+")", value="**S:**".format()+playersdata[0][4]+" **F:**".format()+playersdata[0][5]+" WR:"+playersdata[0][6]+"%"+"(W"+playersdata[0][7]+",L"
        +playersdata[0][8]+")", inline=True)
        embed.add_field(name=playersdata[5][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[5][1])]+")", value="**S:**".format()+playersdata[5][4]+" **F:**".format()+playersdata[5][5]+" WR:"+playersdata[5][6]+"%"+"(W"+playersdata[0][7]+",L"
        +playersdata[5][8]+")", inline=True)
        embed.add_field(name=playersdata[1][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[1][1])]+")", value="**S:**".format()+playersdata[1][4]+" **F:**".format()+playersdata[1][5]+" WR:"+playersdata[1][6]+"%"+"(W"+playersdata[0][7]+",L"
        +playersdata[1][8]+")", inline=True)
        embed.add_field(name=playersdata[6][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[6][1])]+")", value="**S:**".format()+playersdata[6][4]+" **F:**".format()+playersdata[6][5]+" WR:"+playersdata[6][6]+"%"+"(W"+playersdata[6][7]+",L"
        +playersdata[6][8]+")", inline=True)
        embed.add_field(name=playersdata[2][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[2][1])]+")", value="**S:**".format()+playersdata[2][4]+" **F:**".format()+playersdata[2][5]+" WR:"+playersdata[2][6]+"%"+"(W"+playersdata[2][7]+",L"
        +playersdata[2][8]+")", inline=True)
        embed.add_field(name=playersdata[7][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[7][1])]+")", value="**S:**".format()+playersdata[7][4]+" **F:**".format()+playersdata[7][5]+" WR:"+playersdata[7][6]+"%"+"(W"+playersdata[7][7]+",L"
        +playersdata[7][8]+")", inline=True)
        embed.add_field(name=playersdata[3][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[3][1])]+")", value="**S:**".format()+playersdata[3][4]+" **F:**".format()+playersdata[3][5]+" WR:"+playersdata[3][6]+"%"+"(W"+playersdata[3][7]+",L"
        +playersdata[3][8]+")", inline=True)
        embed.add_field(name=playersdata[8][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[8][1])]+")", value="**S:**".format()+playersdata[8][4]+" **F:**".format()+playersdata[8][5]+" WR:"+playersdata[8][6]+"%"+"(W"+playersdata[8][7]+",L"
        +playersdata[8][8]+")", inline=True)
        embed.add_field(name=playersdata[4][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[4][1])]+")", value="**S:**".format()+playersdata[4][4]+" **F:**".format()+playersdata[4][5]+" WR:"+playersdata[4][6]+"%"+"(W"+playersdata[4][7]+",L"
        +playersdata[4][8]+")", inline=True)
        embed.add_field(name=playersdata[9][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[9][1])]+")", value="**S:**".format()+playersdata[9][4]+" **F:**".format()+playersdata[9][5]+" WR:"+playersdata[9][6]+"%"+"(W"+playersdata[9][7]+",L"
        +playersdata[9][8]+")", inline=True)
        await ctx.send(embed=embed)
                        #index:               0     1       2      3      4     5       6       7           8
                          #player data key:  [team, champ, summid, name, soloq, flex, winrate, totalwins, totallosses]
