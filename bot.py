import discord
from discord.ext import commands
from bot.tools import *

intents = discord.Intents.default()
intents.message_content = True
# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Token
token = ''

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# @bot.command(name='roll', help='Rolls a dice')
# async def rolling(ctx, args):
#     if (args.isnumeric()):
#         value = int(args)
#         await ctx.send("Rolled: " + str(random.randint(0, value)))
#     else:
#         await ctx.send("You can't roll with a non-numeric value")

@bot.command(name='roll', help='Rolls specified dice X times. !roll XdY')
async def roll(ctx, args):
    ## Sanitize args
    verifyString = "^[1-10]d[1-20]$"
    
    result = roll_dice()
    embed=discord.Embed

@bot.command(name='harass', help='Why')
async def harass(ctx):
    await ctx.send(f'<@{ctx.author.id}>')

@bot.command(name='whoami', help='User object information')
async def dox(ctx):
    toSend = f'{ctx.author.mention}\nGlobal_Name: {ctx.author.global_name}\nName: {ctx.author.name}\n ID: {ctx.author.id}'
    await ctx.send(toSend)


@bot.command(name='ping', help='Pings the bot')
async def testing_text(ctx):
    await ctx.send("Pong")

# Command to add a task
@bot.command(name='addtask', help='Adds a task to the list.')
async def add_task(ctx, *, task):
    # Here you would add the task to your database or in-memory data structure
    await ctx.send(f'Task added: {task}')

# Command to assign a task
@bot.command(name='assign', help='Assigns a task to a user.')
async def assign_task(ctx, task_id: int, user: discord.Member):
    # Here you would assign the task to the user in your database or in-memory data structure
    await ctx.send(f'Task {task_id} assigned to {user.name}')

# Command to mark a task as completed
@bot.command(name='complete', help='Marks a task as completed.')
async def complete_task(ctx, task_id: int):
    # Here you would mark the task as completed in your database or in-memory data structure
    await ctx.send(f'Task {task_id} marked as completed')

'''
Init: open token file and set token
'''
def __init__(self, *args, **kwargs):
    with open("token.txt", "r") as f:
        token = f.read()
        print(f"Read token: {token}")

# Run the bot
bot.run(token)