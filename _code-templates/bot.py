import os
import random
import asyncio

from dotenv import load_dotenv
from discord.ext import commands

import filehelper
import validatehelper

#utility bot
#tasks for each user -> save in userid.txt
#rng function -> specify range of values?
#yes or no coinflip

prefix = ".."
bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
version_number = "1"

load_dotenv(".env")
TOKEN = os.getenv('DISCORD_TOKEN')

TASKLIST_DIR = "/userdata/"
TASKLIST_PATH = ""

#on_ready(): print in debug console
@bot.event
async def on_ready():
    global TASKLIST_PATH
    TASKLIST_PATH = os.getcwd() + TASKLIST_DIR
    print('Utility Bot version %s' % version_number)
    print('Using TASKLIST_PATH: %s' % TASKLIST_PATH)
    print('Logged in as {0.user}'.format(bot))
    print('Bot started successfully.')

#handle adding tasks
@bot.command(name="addtask")
async def _addtask(ctx):
    await ctx.send("Enter the task that you want to keep track of:")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content != ""

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TiemoutError:
        await ctx.send("You didn't reply in time! (60s)")
        return

    msg_encoded = msg.content.encode("ascii", "ignore")
    validator = validatehelper.ValidateHelper(msg_encoded)
    if not validator.validateAddTask():
        await ctx.send("Illegal character(s) detected in task (<>/\{\}[\]~`) or task is empty (unicode characters are NOT allowed)!")
        return

    fileio = filehelper.FileHelper(TASKLIST_PATH,str(ctx.message.author.id))
    fileio.append(msg_encoded.decode('ascii'))

    await ctx.send("Task successfully added!")

    return

#handle deleting tasks
@bot.command(name="deltask")
async def _deltask(ctx, *argv):
    argc = len(argv)
    if argc > 1:
        await ctx.send("Please only include one argument!")
        return
    if argc < 1:
        await ctx.send("Correct usage: ..deltask <task #>")
    
    try:
        id = int(argv[0])
        if id < 1:
            raise ValueError("Invalid task ID")
    except ValueError:
        await ctx.send("Task # must be a positive integer!")

    fileio = filehelper.FileHelper(TASKLIST_PATH,str(ctx.message.author.id))
    try:
        ret = fileio.delete(id-1)
        if ret == 0:
            await ctx.send("Task successfully removed!")
        if ret == 1:
            await ctx.send("Task #"+str(id)+" does not exist!")
    except LookupError:
        await ctx.send("Internal error occurred :stressedSmoking:")

    return

#handle list tasks
@bot.command(name="tasks")
async def _tasks(ctx):
    fileio = filehelper.FileHelper(TASKLIST_PATH,str(ctx.message.author.id))
    task_arr = fileio.read()
    if len(task_arr) == 0:
        await ctx.send("You have no tasks!")
        return

    task_msg = "__{}'s Tasks__\n".format(ctx.message.author.mention)

    for id, task in enumerate(task_arr):
        task_msg = task_msg + "Task #" + str(id+1) + ": " + task + "\n"

    await ctx.send(task_msg)

#handle rng
@bot.command(name="rng")
async def _rng(ctx, *argv):
    argc = len(argv)
    if argc != 2:
        await ctx.send("Please include exactly 2 arguments! Correct usage: ..rng <start> <end>")
        return

    choice = random.randint(argv[0], argv[1])
    await ctx.send("The chosen number is "+str(choice))
    return

#handle coinflip
@bot.command(name="coinflip")
async def _coinflip(ctx):
    rng = random.random()
    if rng > 0.49:
        await ctx.send("**HEADS**")
    else:
        await ctx.send("**TAILS**")
    return

#handle help
'''
@bot.command(name="help")
async def _help(ctx):
    await ctx.send("**Commands:**\n\n**addtask** - Allows adding of tasks unique to user\n**deltask <task #>** - Allows deleting tasks unique to user\n**tasks** - Lists all the tasks of the user\n**rng <start> <end>** - Randomly chooses a number in the range specified, range is inclusive of both ends\n**coinflip** - Returns heads or tails")
    return
'''

bot.run(TOKEN)