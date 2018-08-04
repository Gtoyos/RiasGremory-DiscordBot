
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

class Akinator:
    """Play Akinator with Rias!"""

    def __init__(self, bot: Red):
        self.bot = bot

    @staticmethod
    def getanswer(answer):
        with open(os.path.dirname(os.path.abspath(__file__))+"/akinatordata.json", "r") as handler:
            raw = handler.read()
            if answer == "all":
                return json.loads(raw)["answers"]
            else:
                return json.loads(raw)["answers"][answer]

    @staticmethod
    def anstostrint(ans: str):
        ans = ans.lower()
        if ans in self.getanswer("yes"):
            return "0"
        if ans in self.getanswer("no"):
            return "1"
        if ans in self.getanswer("idk"):
            return "2"
        if ans in self.getanswer("probably"):
            return "3"
        if ans in self.getanswer("probablynot"):
            return "4"
        else:
            return "-1"

    @staticmethod
    def wslinks(type):
        with open(os.path.dirname(os.path.abspath(__file__))+"/akinatordata.json", "r") as handler:
            raw = handler.read()
            return json.loads(raw)["links"][type]

    @commands.guild_only()
    @commands.command()
    async def akinator(self,ctx):
        """
        Play Akinator whith Rias!
        """
        try:
            akinator_session = requests.get(self.wslinks("NEW_SESSION_URL")+str(hash(ctx.author))+"&constraint=ETAT<>'AV'")
        except Exception as e:
            print("Exception in new session. {}".format(e))
            akinator_session = requests.get(self.wslinks("NEW_SESSION_URL")+"weirdname&constraint=ETAT<>'AV'")    #if ws throws an error if name is too weird
        akinator_data = akinator_session.json()
        try:
            if akinator_data["completion"] == "OK":
                success = True
            else:
                success = False
        except:
            success = False
        if not success:
            await ctx.send("There was an issue with conecting to Akinator's service :confused:")
            raise Exception("Error: Akinator ws failed")
        game_over = False
        can_guess = False
        guessed_wrong_once = False
        a_sym = self.getanswer("all")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while not game_over:
            while not can_guess:
                await ctx.send("Question "+str(int(akinator_data['parameters']['step_information']['step'])+1)+": "+akinator_data["parameters"]["step_information"]["question"])
                ans_ok = False
                while not ans_ok:
                    try:
                        answer = await ctx.bot.wait_for("message", timeout=15.0, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send("You are taking too long to answer, baka. If you want to play again you will have to invoke `akinator` again. 	(・_・ヾ ")
                        break
                    if answer in a_sym["yes"] or answer in a_sym["no"] or answer in a_sym["idk"] or answer in a_sym["probably"] or answer in a_sym["probablynot"]:
                        ans_ok = True
                    else:
                        pass
                response = self.anstostrint(answer)
                params = {
                    "session": akinator_data['parameters']['identification']['session'],
                    "signature": akinator_data['parameters']['identification']['signature'],
                    "step": akinator_data['parameters']['step_information']['step'],
                    "answer": response
                }
                session = akinator_data["parameters"]["identification"]["session"]
                signature = akinator_data["parameters"]["identification"]["signature"]

                akinator_session = requests.get(self.wslinks("ANSWER_URL")+str(hash(ctx.author))+"&constraint=ETAT<>'AV'", params=params)
                #culd passs player and etat as params too!
                akinator_data = akinator_session.json()
                if int(float(akinator_data["parameters"]["progression"])) > 91 and not guessed_wrong_once:
                    can_guess = True

            params = {
                "session": session,
                "signature": signature,
                "step": akinator_data["parameters"]["step"]
            }
            guess_session = requests.get(self.wslinks("GET_GUESS_URL")+str(hash(ctx.author))+"&constraint=ETAT<>'AV'", params=params)
            guess_data = guess_session.json()

            name = guess_data["parameters"]["elements"][0]["element"]["name"]
            desc = guess_data["parameters"]["elements"][0]["element"]["description"]
            img =  guess_data["parameters"]["elements"][0]["element"]["absolute_picture_path"]

            await ctx.send("Is this your character?")
            embed = discord.Embed(colour=ctx.guild.me.top_role.colour,title=name,description="*"+desc+"*")
            embed.set_image(url=img)

            ans_ok = False
            while not ans_ok:
                try:
                    answer = await self.bot.wait_for("message",check=check,timeout=15)
                except asyncio.TimeoutError:
                    await ctx.send("You are taking too long to answer, baka. If you want to play again you will have to invoke `akinator` again. 	(・_・ヾ ")
                    break
                if answer in a_sym["yes"] or answer in a_sym["no"] or answer in a_sym["idk"] or answer in a_sym["probably"] or answer in a_sym["probablynot"]:
                    ans_ok = True
                else:
                    pass
            if answer.lower() in a_sym["yes"]:
                await ctx.send("I guessed right! Thanks for playing with me uwu")
                akinator_r = requests.get(self.wslinks("CHOICE_URL")+str(hash(ctx.author))+"&constraint=ETAT<>'AV'", params=params)
                game_over = True
                break

            elif answer.lower() in a_sym["no"]:
                await ctx.send("Oh no! (・_・;). I will ask you a few more questions then.")
                params = {
                    "session": session,
                    "signature": signature,
                    "step": akinator_data['parameters']['step'],
                    "forward_answer": response
                }
                akinator_r = requests.get(self.wslinks("EXCLUSION_URL")+str(hash(ctx.author))+"&constraint=ETAT<>'AV'", params=params)
                can_guess= False
                guessed_wrong_once = True
            else:
                pass

    @commands.command()
    async def akinators(self, ctx):
        def msg_check(m):
            return m.author == ctx.author
        answer = await self.bot.wait_for("message", timeout=15.0, check=msg_check)
