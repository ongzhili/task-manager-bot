from collections import defaultdict
import datetime
import discord
from discord.ext import commands, tasks
import discord.ext.commands
from bot.tools import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import sched
import time
import asyncio
from ossapi import Ossapi
from bot.task_manager.task_master import TaskChecker
from bot.task_manager.task_crud import TaskCrud

import re

import discord.ext

intents = discord.Intents.default()
intents.message_content = True

# Initialization Process: Discord bot + Firebase App

# Firebase API
cred = credentials.Certificate('firebase_key.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': "https://lelcoindb-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Discord Bot
bot = commands.Bot(command_prefix='!', intents=intents)
scr = sched.scheduler(time.time, time.sleep)

# Token
token = ''

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.load_extension('bot.fun.fun-master')
    await bot.add_cog(TaskChecker(bot, db))
    await bot.add_cog(TaskCrud(bot, db))

'''
Init: open token file and set token
'''
with open("token.txt", "r") as f:
    token = f.readline()
    print(f"Read token: {token}")


bot.run(token)