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

class Lol(commands.Cog):
    """League of Legends commands"""
    def __init__(self, bot: Red):
        self.bot = bot

    @staticmethod
    def loldata(option):
        with open(os.path.dirname(os.path.abspath(__file__))+"/loldata.json", "r") as handler:
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
            elif option == "linkedsumms":
                return json.loads(raw)["linkedsumms"]
            elif option == "version":
                return requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

    def lolicons(self, iconname):
        host1,host2,host3,host4 = [
            self.bot.get_guild(435125536407420929),
            self.bot.get_guild(450402584839323649),         #emojidatabase
            self.bot.get_guild(450403317051293707),
            self.bot.get_guild(450412933105713172)]
        iconlist = host1.emojis + host2.emojis + host3.emojis + host4.emojis
        return str(discord.utils.get(iconlist, name=iconname))

    @commands.guild_only()
    @commands.command()
    async def lollink(self,ctx,region: str=None,user: str=None):
        """Links your Lol summoner's name.

        Syntax: `$lollink summonername`
        Summoner doesn't need to be written
        case sensitive but without spaces.
        To link your username
        with another summoner's name invoke
        this command again. To reset it leave it
        in blank.
        """
        with open(os.path.dirname(os.path.abspath(__file__))+"/loldata.json", "r") as handler:
            raw = handler.read()
            loldata = json.loads(raw)
        if user == None and region == None:
            if str(ctx.author.id) in loldata["linkedsumms"]:
                loldata["linkedsumms"].pop(str(ctx.author.id))
                await ctx.send("Your linked account has been removed. (>_<) ")
            else:
                await ctx.send("You don't have a linked account yet. Write your summoner's name after this command to add it (≧◡≦) ")
        elif user == None or region == None:
            await ctx.send(":x: *Summoner name or region code missing.*".format())
            return
        elif region not in self.loldata("region"):
            await ctx.send(":x: *The region code isn't correct senpai 7w7*".format())
            return
        elif str(ctx.author.id) in loldata["linkedsumms"]:
            loldata["linkedsumms"][str(ctx.author.id)] = [region,user]
            await ctx.send("Your linked account has been changed.")
        else:
            loldata["linkedsumms"][str(ctx.author.id)] = [region,user]
            await ctx.send("Your Discord account has been linked with: "+user+" from "+region+" (⌒ω⌒)")
            await ctx.send("Remember that your summoner's name has to be written without spaces!")
        with open(os.path.dirname(os.path.abspath(__file__))+"/loldata.json", "w") as handler:
            json.dump(loldata, handler)

    @commands.guild_only()
    @commands.command()
    async def lolsumm(self, ctx, *args):
        """Gets summoner's profile info.

        syntax: $lol summ [reg] [name].
        Summoner's name doesn't need to be
        written case sensitive nor with spaces"""
        [x.lower() for x in args]
        if len(args) == 0:
            if str(ctx.author.id) in self.loldata("linkedsumms"):
                region = self.loldata("linkedsumms")[str(ctx.author.id)][0]
                summ = self.loldata("linkedsumms")[str(ctx.author.id)][1]
            else:
                await ctx.send("You don't have a linked summoner yet. Use the command lollink to link one (≧◡≦) ")
                return
        if len(args) > 0:
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
        accidstr = str(summdata["accountId"])
        elodatah = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/league/v3/positions/by-summoner/"+summidstr+"?api_key="+self.loldata("key"))
        elodata = elodatah.json()
        malvlh = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/"+summidstr+"?api_key="+self.loldata("key"))
        malvl = malvlh.json()
        maestryh = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/"+summidstr+"?api_key="+self.loldata("key"))
        maestry = maestryh.json()
        lastgamesh = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/match/v3/matchlists/by-account/"+accidstr+"?endIndex=10&api_key="+self.loldata("key"))
        lastgames = lastgamesh.json()
        if elodatah.status_code == 503 or malvlh.status_code == 503 or maestryh.status_code == 503 or lastgamesh.status_code == 503:
            await ctx.send("*The Riot API is currently unavailable. Please try again later :persevere:*".format())
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
        #last Games
        wins = []
        for k in lastgames["matches"]:
            matchdata = requests.get("https://"+self.loldata("region")[region]+".api.riotgames.com/lol/match/v3/matches/"+str(k["gameId"])+"?api_key="+self.loldata("key")).json()
            participantgameid = [obj for obj in matchdata["participantIdentities"] if obj["player"]["summonerId"]==int(summidstr)]
            participantgameteam = [obj for obj in matchdata["participants"] if obj["participantId"]==participantgameid[0]["participantId"]]
            winnerteam = [obj for obj in matchdata["teams"] if obj["win"]=="Win"]
            if participantgameteam[0]["teamId"] == winnerteam[0]["teamId"]:
                wins.append(1)
        lastgameswr = str((len(wins)*100)/len(lastgames["matches"]))
        lastgamesfinal = str(len(wins))+"W "+str((len(lastgames["matches"])-len(wins)))+"L *("+str(lastgameswr[0:4])+"% WR)*"
        if len(elodata) == 0:
            soloq = "Unranked"
            flex = "Unranked"
            winrate = "0%"
            totalwins = 0
            totallosses = 0                            #checkplacementelo
        elif len(elodata) == 1:
            if "RANKED_SOLO_5x5" in elodata[0]["queueType"]:
                soloq = elodata[0]["tier"]+" "+elodata[0]["rank"]
                soloqlp = str(elodata[0]["leaguePoints"])+"LP"
                winrate = (elodata[0]["wins"])*100/(elodata[0]["wins"]+elodata[0]["losses"])
                totalwins = elodata[0]["wins"]
                totallosses = elodata[0]["losses"]
                flex = "Unranked"
            if "RANKED_FLEX_SR" in elodata[0]["queueType"]:
                flex= elodata[0]["tier"]+" "+elodata[0]["rank"]
                flexlp = str(elodata[0]["leaguePoints"]) + " lp"
                winrate = (elodata[0]["wins"])*100/(elodata[0]["wins"]+elodata[0]["losses"])
                totalwins = elodata[0]["wins"]
                totallosses = elodata[0]["losses"]
                soloq = "Unranked"
        elif len(elodata) == 2:
            if "RANKED_FLEX_SR" in elodata[0]["queueType"]:
                flex= elodata[0]["tier"]+" "+elodata[0]["rank"]
                flexlp = str(elodata[0]["leaguePoints"]) + "LP"
                soloq= elodata[1]["tier"]+" "+elodata[1]["rank"]
                soloqlp = str(elodata[1]["leaguePoints"])+ "LP"
            elif "RANKED_SOLO_5x5" in elodata[0]["queueType"]:
                soloq= elodata[0]["tier"]+" "+elodata[0]["rank"]
                soloqlp = str(elodata[0]["leaguePoints"]) + "LP"
                flex= elodata[1]["tier"]+" "+elodata[1]["rank"]
                flexlp = str(elodata[1]["leaguePoints"]) + "LP"
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
        colorh = int(color, 16)
        tierflex = flex.split()
        tiersolo = soloq.split()
        opgg = "http://"+region+".op.gg/summoner/userName="+summdata["name"].replace(" ", "")                                                   #embedformatforv3?
        lolking = "http://www.lolking.net/summoner/"+region+"/"+summidstr+"/"+summdata["name"].replace(" ", "")+"#/profile"
        links = "[op.gg]({}) & [Lolking]({})".format(opgg, lolking)
        embed=discord.Embed(title=summdata["name"], description="*Main "+mainrole+": "+self.lolicons(mainchamps[0])+
            " "+mainchamps[0]+", "+self.lolicons(mainchamps[1])+" "+mainchamps[1]+", "+self.lolicons(mainchamps[2])+
            " "+mainchamps[2]+".*", color=colorh)
        embed.set_thumbnail(url=summicon)
        try:            #if its unranked
            embed.add_field(name="Solo/Duo", value=self.lolicons(tiersolo[0].lower().capitalize())+" "+tiersolo[0].lower().capitalize()+" "+tiersolo[1]+" *"+soloqlp+"*", inline=True)
        except:
            embed.add_field(name="Solo/Duo", value=self.lolicons("Unranked")+" *Unranked*", inline = True)
        try:
            embed.add_field(name="Flex", value=self.lolicons(tierflex[0].lower().capitalize())+" "+tierflex[0].lower().capitalize()+" "+tierflex[1]+" *"+flexlp+"*", inline=True)
        except:
            embed.add_field(name="Flex", value=self.lolicons("Unranked")+" *Unranked*", inline = True)
        embed.add_field(name="Winrate", value=str(winrate)[0:4]+"% *("+"W"+(str(totalwins))+", "+"L"+(str(totallosses))+")*", inline=True)
        embed.add_field(name="Last Games", value=lastgamesfinal, inline=True)
        embed.add_field(name="Maestry Score", value=malvl, inline=True)
        embed.add_field(name="Summoner Level", value=summdata["summonerLevel"], inline=True)
        embed.add_field(name="More Info", value=links, inline=True)
        embed.set_footer(text='Summoner ID:'+" "+summidstr)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def lolgame(self, ctx, *args):
        """Obtains summoner's game info.

        syntax: $lol game [reg] [name].
        Summoner's name doesn't need to be
        written case sensitive nor with spaces"""
        [x.lower() for x in args]
        if len(args) == 0:
            if str(ctx.author.id) in self.loldata("linkedsumms"):
                region = self.loldata("linkedsumms")[str(ctx.author.id)][0]
                summ = self.loldata("linkedsumms")[str(ctx.author.id)][1]
            else:
                await ctx.send("You don't have a linked summoner yet. Use the command lollink to link one (≧◡≦) ")
                return
        if len(args) > 0:
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
        avgslist = avgsoloelo.split(" ")
        avgflist = avgflexelo.split(" ")
        avgstier,avgftier = avgslist[0].lower().capitalize(),avgflist[0].lower().capitalize()
        avgsnum,avgfnum = avgslist[1],avgflist[1]
        if intelo[bestelo].startswith("CHALLENGER"):
            color = "0xffff00"
        elif intelo[bestelo].startswith("MASTER"):
            color = "0xff8600"
        elif intelo[bestelo].startswith("DIAMOND"):
            color = "0x00ffff"
        elif intelo[bestelo].startswith("PLATINUM"):
            color = "0x97ffff"
        elif intelo[bestelo].startswith("GOLD"):
            color = "0xffff80"
        elif intelo[bestelo].startswith("SILVER"):
            color = "0x494949"
        elif intelo[bestelo].startswith("BRONZE"):
            color = "0x804000"
        else:
            color = "0xffffff"
        colorh = int(color, 16)
        champsid = self.loldata("champsid")
        for k in playersdata:
            k[1] = champsid[str(k[1])]
        blueteam = []
        redteam = []
        for k in playersdata:
            if k[0] == 100:
                blueteam.append(k)
            if k[0] == 200:
                redteam.append(k)
        for k in blueteam:
            if k[4] is not "Unranked":
                k[4] = k[4].split()
            if k[5] is not "Unranked":
                k[5] = k[5].split()
            if k[4] == "Unranked":
                k[4] = ["Unranked", " "]
            if k[5] == "Unranked":
                k[5] = ["Unranked", " "]
        for k in redteam:
            if k[4] is not "Unranked":
                k[4] = k[4].split()
            if k[5] is not "Unranked":
                k[5] = k[5].split()
            if k[4] == "Unranked":
                k[4] = ["Unranked", " "]
            if k[5] == "Unranked":
                k[5] = ["Unranked", " "]
        embed = discord.Embed(title=maptype+" "+gametype+" Game", description="Average Tier: *Solo/Duo: **"+self.lolicons(avgstier)+avgsnum+"** , Flex: **"+
            self.lolicons(avgftier)+avgfnum+"***", color=colorh)
        embed.add_field(name=":large_blue_circle: Blue Team", value=self.lolicons(blueteam[0][1].capitalize())+"**"+blueteam[0][3].capitalize()+"**\n"+
            self.lolicons(blueteam[1][1])+"**"+blueteam[1][3].title()+"**\n"+
            self.lolicons(blueteam[2][1])+"**"+blueteam[2][3].title()+"**\n"+
            self.lolicons(blueteam[3][1])+"**"+blueteam[3][3].title()+"**\n"+
            self.lolicons(blueteam[4][1])+"**"+blueteam[4][3].title()+"**\n", inline=True)
        embed.add_field(name=self.lolicons("Null")+"Solo ｜ Flex", value=self.lolicons("Null")+self.lolicons(blueteam[0][4][0].lower().capitalize())+"**"+blueteam[0][4][1]+"**  "+
            self.lolicons(blueteam[0][5][0].lower().capitalize())+"**"+blueteam[0][5][1]+"**\n"+
            self.lolicons("Null")+self.lolicons(blueteam[1][4][0].lower().capitalize())+"**"+blueteam[1][4][1]+"**  "+
            self.lolicons(blueteam[1][5][0].lower().capitalize())+"**"+blueteam[1][5][1]+"**\n"+
            self.lolicons("Null")+self.lolicons(blueteam[2][4][0].lower().capitalize())+"**"+blueteam[2][4][1]+"**  "+
            self.lolicons(blueteam[2][5][0].lower().capitalize())+"**"+blueteam[2][5][1]+"**\n"+
            self.lolicons("Null")+self.lolicons(blueteam[3][4][0].lower().capitalize())+"**"+blueteam[3][4][1]+"**  "+              #siguiente parche: hacer que las ligas I,II,V, unranked (doble espacio?)
            self.lolicons(blueteam[3][5][0].lower().capitalize())+"**"+blueteam[3][5][1]+"**\n"+                                    #terminen con un espacio asi quedan todas alineadas...
            self.lolicons("Null")+self.lolicons(blueteam[4][4][0].lower().capitalize())+"**"+blueteam[4][4][1]+"**  "+
            self.lolicons(blueteam[4][5][0].lower().capitalize())+"**"+blueteam[4][5][1]+"**\n", inline=True)
        embed.add_field(name=self.lolicons("Null")+"Winrate",value=self.lolicons("Null")+str(blueteam[0][6])+"% *("+"W"+str(blueteam[0][7])+", "+"L"+str(blueteam[0][8])+")*\n"+
            self.lolicons("Null")+str(blueteam[1][6])+"% *("+"W"+(str(blueteam[1][7]))+", "+"L"+str(blueteam[1][8])+")*\n"+
            self.lolicons("Null")+str(blueteam[2][6])+"% *("+"W"+(str(blueteam[2][7]))+", "+"L"+str(blueteam[2][8])+")*\n"+
            self.lolicons("Null")+str(blueteam[3][6])+"% *("+"W"+(str(blueteam[3][7]))+", "+"L"+str(blueteam[3][8])+")*\n"+
            self.lolicons("Null")+str(blueteam[4][6])+"% *("+"W"+(str(blueteam[4][7]))+", "+"L"+str(blueteam[4][8])+")*", inline=True)

        embed.add_field(name=":red_circle: Red Team", value=self.lolicons(redteam[0][1].capitalize())+"**"+redteam[0][3].capitalize()+"**\n"+
            self.lolicons(redteam[1][1])+"**"+redteam[1][3].title()+"**\n"+
            self.lolicons(redteam[2][1])+"**"+redteam[2][3].title()+"**\n"+
            self.lolicons(redteam[3][1])+"**"+redteam[3][3].title()+"**\n"+
            self.lolicons(redteam[4][1])+"**"+redteam[4][3].title()+"**\n", inline=True)
        embed.add_field(name=self.lolicons("Null"), value=self.lolicons("Null")+self.lolicons(redteam[0][4][0].lower().capitalize())+"**"+redteam[0][4][1]+"**  "+
            self.lolicons(redteam[0][5][0].lower().capitalize())+"**"+redteam[0][5][1]+"**\n"+
            self.lolicons("Null")+self.lolicons(redteam[1][4][0].lower().capitalize())+"**"+redteam[1][4][1]+"**  "+
            self.lolicons(redteam[1][5][0].lower().capitalize())+"**"+redteam[1][5][1]+"**\n"+
            self.lolicons("Null")+self.lolicons(redteam[2][4][0].lower().capitalize())+"**"+redteam[2][4][1]+"**  "+
            self.lolicons(redteam[2][5][0].lower().capitalize())+"**"+redteam[2][5][1]+"**\n"+
            self.lolicons("Null")+self.lolicons(redteam[3][4][0].lower().capitalize())+"**"+redteam[3][4][1]+"**  "+              #siguiente parche: hacer que las ligas I,II,V, unranked (doble espacio?)
            self.lolicons(redteam[3][5][0].lower().capitalize())+"**"+redteam[3][5][1]+"**\n"+                                    #terminen con un espacio asi quedan todas alineadas...
            self.lolicons("Null")+self.lolicons(redteam[4][4][0].lower().capitalize())+"**"+redteam[4][4][1]+"**  "+
            self.lolicons(redteam[4][5][0].lower().capitalize())+"**"+redteam[4][5][1]+"**\n", inline=True)
        embed.add_field(name=self.lolicons("Null"),value=self.lolicons("Null")+str(redteam[0][6])+"% *("+"W"+str(redteam[0][7])+", "+"L"+str(redteam[0][8])+")*\n"+
            self.lolicons("Null")+str(redteam[1][6])+"% *("+"W"+(str(redteam[1][7]))+", "+"L"+str(redteam[1][8])+")*\n"+
            self.lolicons("Null")+str(redteam[2][6])+"% *("+"W"+(str(redteam[2][7]))+", "+"L"+str(redteam[2][8])+")*\n"+
            self.lolicons("Null")+str(redteam[3][6])+"% *("+"W"+(str(redteam[3][7]))+", "+"L"+str(redteam[3][8])+")*\n"+
            self.lolicons("Null")+str(redteam[4][6])+"% *("+"W"+(str(redteam[4][7]))+", "+"L"+str(redteam[4][8])+")*", inline=True)
        await ctx.send(embed=embed)
        #embed=discord.Embed(title=maptype+" "+gametype+" "+"Game", description="Average Elo: "+"Solo/Duo:"+" "+avgsololeague+" "+avgsolonum+" , Flex: "+avgflexleague+" "+avgflexnum, color=colorh)
        #embed.set_thumbnail(url=icon)
        #embed.add_field(name=playersdata[0][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[0][1])]+")", value="**S:**".format()+playersdata[0][4]+" **F:**".format()+playersdata[0][5]+" WR:"+playersdata[0][6]+"%"+"(W"+playersdata[0][7]+",L"
        #+playersdata[0][8]+")", inline=True)
        #embed.add_field(name=playersdata[5][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[5][1])]+")", value="**S:**".format()+playersdata[5][4]+" **F:**".format()+playersdata[5][5]+" WR:"+playersdata[5][6]+"%"+"(W"+playersdata[0][7]+",L"
        #+playersdata[5][8]+")", inline=True)
        #embed.add_field(name=playersdata[1][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[1][1])]+")", value="**S:**".format()+playersdata[1][4]+" **F:**".format()+playersdata[1][5]+" WR:"+playersdata[1][6]+"%"+"(W"+playersdata[0][7]+",L"
        #+playersdata[1][8]+")", inline=True)
        #embed.add_field(name=playersdata[6][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[6][1])]+")", value="**S:**".format()+playersdata[6][4]+" **F:**".format()+playersdata[6][5]+" WR:"+playersdata[6][6]+"%"+"(W"+playersdata[6][7]+",L"
        #+playersdata[6][8]+")", inline=True)
        #embed.add_field(name=playersdata[2][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[2][1])]+")", value="**S:**".format()+playersdata[2][4]+" **F:**".format()+playersdata[2][5]+" WR:"+playersdata[2][6]+"%"+"(W"+playersdata[2][7]+",L"
        #+playersdata[2][8]+")", inline=True)
        #embed.add_field(name=playersdata[7][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[7][1])]+")", value="**S:**".format()+playersdata[7][4]+" **F:**".format()+playersdata[7][5]+" WR:"+playersdata[7][6]+"%"+"(W"+playersdata[7][7]+",L"
        #+playersdata[7][8]+")", inline=True)
        #embed.add_field(name=playersdata[3][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[3][1])]+")", value="**S:**".format()+playersdata[3][4]+" **F:**".format()+playersdata[3][5]+" WR:"+playersdata[3][6]+"%"+"(W"+playersdata[3][7]+",L"
        #+playersdata[3][8]+")", inline=True)
        #embed.add_field(name=playersdata[8][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[8][1])]+")", value="**S:**".format()+playersdata[8][4]+" **F:**".format()+playersdata[8][5]+" WR:"+playersdata[8][6]+"%"+"(W"+playersdata[8][7]+",L"
        #+playersdata[8][8]+")", inline=True)
        #embed.add_field(name=playersdata[4][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[4][1])]+")", value="**S:**".format()+playersdata[4][4]+" **F:**".format()+playersdata[4][5]+" WR:"+playersdata[4][6]+"%"+"(W"+playersdata[4][7]+",L"
        #+playersdata[4][8]+")", inline=True)
        #embed.add_field(name=playersdata[9][3].capitalize()+" ("+self.loldata("champsid")[str(playersdata[9][1])]+")", value="**S:**".format()+playersdata[9][4]+" **F:**".format()+playersdata[9][5]+" WR:"+playersdata[9][6]+"%"+"(W"+playersdata[9][7]+",L"
        #+playersdata[9][8]+")", inline=True)
        #await ctx.send(embed=embed)
                        #index:               0     1       2      3      4     5       6       7           8
                          #player data key:  [team, champ, summid, name, soloq, flex, winrate, totalwins, totallosses]
