import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


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

# Run the bot
bot.run('MTIyNDMzNzg4MjQ2MzA4MDU1OQ.GZoVw-.NzjyeYXkyg6YcoggYNj8z2ID67xLZ21UnbK_OU')