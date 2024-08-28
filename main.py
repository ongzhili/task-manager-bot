import datetime
import discord
from discord.ext import commands, tasks
import discord.ext.commands
from bot.tools import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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


# Token
token = ''

@tasks.loop(seconds = 10) # repeat after every 10 seconds
async def myLoop():
    print("ababababab")


# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='addtask', help = 'Adds a task to the task manager list. :calendar: Usage: !addtask <TASK> in <TIME>')
async def addtask(ctx, *, args):
    # Split at the last occurrence of " in "
    parts = args.rsplit(" in ", 1)
    
    if len(parts) != 2:
        await ctx.send("Invalid format. Please use: !addtask <TASK> in <TIME>")
        
    else:
        task, time = parts
        task = task.strip()
        time = time.strip()

        try:
            time_delta = parse_time_delta(time)
            due_time = datetime.datetime.now() + time_delta

            unix_timestamp = int(due_time.timestamp())
            
            # Format the due time
            formatted_due_time = due_time.strftime("%Y-%m-%d %I:%M %p")
            
            # Convert ctx.author.id to a string and remove any invalid characters
            author_id = str(ctx.author.id).replace('.', '_').replace('$', '_').replace('#', '_').replace('[', '_').replace(']', '_')

            ref = db.reference(f'users/{author_id}/tasks')
            if not ref.get():
                # If it doesn't exist, set an empty structure
                ref.set({})
            ref.push({
                'task': task,
                'time': formatted_due_time
            })
            
            await ctx.send(f"Task added: '{task}' to be completed by <t:{unix_timestamp}> (This should be in your local timezone)")

        except ValueError as e:
            
            await ctx.send(f"Error parsing time: {e}")

def parse_time_delta(time_string):
    # Parse time delta from strings like "2 days", "1 week", "3 hours", etc.
    match = re.match(r'(\d+)\s*(day|days|week|weeks|hour|hours|minute|minutes)', time_string, re.IGNORECASE)
    if match:
        amount, unit = match.groups()
        amount = int(amount)
        unit = unit.lower()
        
        if unit in ['day', 'days']:
            return datetime.timedelta(days=amount)
        elif unit in ['week', 'weeks']:
            return datetime.timedelta(weeks=amount)
        elif unit in ['hour', 'hours']:
            return datetime.timedelta(hours=amount)
        elif unit in ['minute', 'minutes']:
            return datetime.timedelta(minutes=amount)
    
    raise ValueError(f"Unable to parse time string: {time_string}")
# @bot.command(name='roll', help='Rolls a dice')
# async def rolling(ctx, args):
#     if (args.isnumeric()):
#         value = int(args)
#         await ctx.send("Rolled: " + str(random.randint(0, value)))
#     else:
#         await ctx.send("You can't roll with a non-numeric value")
@bot.command(name='8ball', help='Consults the magic 8-ball :8_ball: !8ball <Question>')
async def eball(ctx, args):
    # Gets 8ball response
        result = eightball(args)

        # Send result as embed
        if not result[0]:
            embed = discord.Embed(title="Invalid input for !8ball",
                                description=f"{result[1]}",
                                color=discord.Color.red())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"8Ball",
                                description=f"The 8ball has spoken:\n{result[1]}",
                                color=discord.Color.green())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
@eball.error
async def eball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Invalid input for !8ball",
                            description="You did not ask 8ball anything!",
                            color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)


@bot.command(name='roll', help='Rolls specified Y dice X times. !roll XdY')
async def roll(ctx, args):
    # Parse args, get result tuple
    result = roll_dice(args)
    
    # Send result as embed
    if not result[0]:
        embed = discord.Embed(title="Invalid input for !roll",
                              description=f"{result[1]}",
                              color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"Rolled dice(s)!",
                              description=f"Here are your dice rolls:\n{result[1]}",
                              color=discord.Color.green())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Invalid input for !roll",
                            description='Invalid argument!\nPlease use the format !flip X, where X is a number between 1-10',
                            color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

@bot.command(name='flip', help='Flip a coin X times. !flip X')
async def flip(ctx, args):
    # Parse args, get result tuple
    result = flip_coin(args)
    # Send result as embed
    if not result[0]:
        embed = discord.Embed(title="Invalid input for !flip",
                              description=f"{result[1]}",
                              color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"Flipped coin(s)!",
                              description=f"Here are your coinflip results:\n{', '.join(str(elem) for elem in result[1])}",
                              color=discord.Color.green())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

@bot.command(name='harass', help='Why')
async def harass(ctx):
    # Send the initial message and store the returned message object
    initial_message = await ctx.send(content=f'<@{ctx.author.id}>')

    # Create the embed
    embed = discord.Embed(title="Harass",
                          description=f'<@{ctx.author.id}>',
                          color=discord.Color.blue())

    # Edit the initial message with the embed
    await initial_message.edit(content=None, embed=embed)

@bot.command(name='whoami', help='User object information')
async def dox(ctx):
    toSend = f'{ctx.author.mention}\nGlobal_Name: {ctx.author.global_name}\nName: {ctx.author.name}\nID: {ctx.author.id}'
    await ctx.send(toSend)


@bot.command(name='ping', help='Pings the bot')
async def testing_text(ctx):
    await ctx.send("Pong")


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
with open("token.txt", "r") as f:
    token = f.readline()
    print(f"Read token: {token}")

myLoop.start()
# Run the bot
bot.run(token)