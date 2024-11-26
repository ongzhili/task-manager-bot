from collections import defaultdict
import datetime
import re
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

# async def setup(bot):
#     bot.add_command(addtask)
#     bot.add_command(view)
#     bot.add_command(delete)
#     bot.add_command(changedate)

class TaskCrud(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name='addtask', help = 'Adds a task to the task manager list. :calendar: Usage: !addtask <TASK> in <TIME>')
    async def addtask(self, ctx, *, args):
        # Split at the last occurrence of " in "
        parts = args.rsplit(" in ", 1)
        
        if len(parts) != 2:
            raise commands.BadArgument("Invalid format! Please use the format: <TASK> in <TIME>.")
            
        else:
            task, time = parts
            task = task.strip()
            time = time.strip()

            try:
                time_delta = parse_time_delta(time)
                due_time = datetime.datetime.now().replace(second=0, microsecond=0) + time_delta
                unix_timestamp = int(due_time.timestamp())
                
                # Convert ctx.author.id to a string and remove any invalid characters
                author_id = str(ctx.author.id).replace('.', '_').replace('$', '_').replace('#', '_').replace('[', '_').replace(']', '_')

                ref = self.db.reference(f'users/{author_id}/tasks')
                if not ref.get():
                    # If it doesn't exist, set an empty structure
                    ref.set({})

                entry = ref.push({
                    'task': task,
                    'time': unix_timestamp
                })
                embd=discord.Embed(title="Task Added!",
                    description="'{}' to be completed by <t:{}> (This should be in your local timezone)".format(task, unix_timestamp),
                    color=discord.Color.green())
                await ctx.send(embed=embd)

            except ValueError as e:
                raise commands.BadArgument("Error parsing time: {}".format(e))

    @addtask.error
    async def addtask_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=":warning: Invalid input for !addtask",
                                description="You did not assign anything!",
                                color=discord.Color.red())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=":warning: Invalid input for !addtask",
                                description=str(error),
                                color=discord.Color.red())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @commands.command(name='view', help='Shows current reminders. !view')
    async def view(self, ctx):
        ref = self.db.reference(f'users/{ctx.author.id}/tasks')                 
        tasks = ref.get()
        if tasks:
            # task[0] = id, task[1] = the items -- in tasks.items()
            tasks = dict(sorted(tasks.items(), key=lambda x: x[1]['time']))
            body = ""
            for idx, (task_id, task) in enumerate(tasks.items()):
                body += f"{idx + 1}: '{task['task']}' by <t:{int(task['time'])}>\n"
            embed = discord.Embed(title="Reminders:",
                                description=body,
                                color=discord.Color.green())
                
        else:
            embed = discord.Embed(title="No Reminders!",
                                description="Looks clear!",
                                color=discord.Color.green())
            
        await ctx.send(embed=embed)

    @commands.command(name='delete', help='Deletes a reminder from the list. !delete <task_number> deletes the <task_number>th upcoming due date. Will not work for tasks due soon')
    async def delete(self, ctx, args):
        try:
            index = int(args)
        except ValueError as e:
            raise commands.BadArgument("{} is not a valid index!".format(args))

        if index <= 0:
            embed = discord.Embed(title="Error!",
                                description=f"Can't delete negative index tasks!",
                                color=discord.Color.red())
        else:
            ref = self.db.reference(f'users/{ctx.author.id}/tasks')                 
            tasks = ref.get()
            if tasks:
                # task[0] = id, task[1] = the items -- in tasks.items()
                tasks = sorted(tasks.items(), key=lambda x: x[1]['time'])
                if index > len(tasks):
                    embed = discord.Embed(title="Error!",
                                        description=f"Can't delete {index}th task if you only have {len(tasks)} tasks!",
                                        color=discord.Color.red())
                else:
                    # -1 because it is 1-indexed
                    task = tasks[index - 1]
                    ref.child(task[0]).delete()
                    embed = discord.Embed(title="Success!",
                                        description = f"Deleted **{task[1]['task']}** that was due in **<t:{int(task[1]['time'])}>**!",
                                        color=discord.Color.green())
                    
            else:
                embed = discord.Embed(title="Error!",
                                    description="Can't delete reminders if you don't have any!",
                                    color=discord.Color.red())
            
        await ctx.send(embed=embed)

    @delete.error
    async def delete_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=":warning: Invalid input for !delete",
                                description=str(error),
                                color=discord.Color.red())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title=":warning: Invalid input for !delete",
                                description="You did not specify any arguments!",
                                color=discord.Color.red())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)


    @commands.command(name='extend', help='Extends a reminder\'s due date. !Extend `<task_number>` in `<new_time_delta>` extends the `<task_number>`th upcoming task\'s due date by `<new_time_delta>`. Will not work for tasks due soon')
    async def changedate(self, ctx, *, args):
        index, time_delta = args.rsplit(" by ", 1)
        index = int(index)
        time_delta = parse_time_delta(time_delta).total_seconds()
        if index <= 0:
            embed = discord.Embed(title="Error!",
                                description=f"Can't delete negative index tasks!",
                                color=discord.Color.red())
        else:
            ref = self.db.reference(f'users/{ctx.author.id}/tasks')                 
            tasks = ref.get()
            if tasks:
                # task[0] = id, task[1] = the items -- in tasks.items()
                tasks = sorted(tasks.items(), key=lambda x: x[1]['time'])
                if index > len(tasks):
                    embed = discord.Embed(title="Error!",
                                        description=f"Can't delete {index}th task if you only have {len(tasks)} tasks!",
                                        color=discord.Color.red())
                else:
                    # -1 because it is 1-indexed
                    task = tasks[index - 1]
                    ref.child(task[0]).delete()
                    new_time = int(int(task[1]['time']) + time_delta)
                    entry = ref.push({
                        'task': task[1]['task'],
                        'time': new_time
                    })
                    embed = discord.Embed(title="Success!",
                                        description = f"Extended **{task[1]['task']}** to be due in **<t:{new_time}>**!",
                                        color=discord.Color.green())
                    
            else:
                embed = discord.Embed(title="Error!",
                                    description="Can't delete reminders if you don't have any!",
                                    color=discord.Color.red())
            
        await ctx.send(embed=embed)


def parse_time_delta(time_string):
    # Initialize a total timedelta
    total_delta = datetime.timedelta()
    
    # Regular expression to match time components
    pattern = r'(\d+)\s*(day|days|week|weeks|h|hour|hours|minute|minutes|min)'
    
    # Find all matches in the input string
    matches = re.findall(pattern, time_string, re.IGNORECASE)

    if not matches:
        raise commands.BadArgument("Invalid time format. Please use formats like '2 days', '1 hour and 3 minutes', etc.")
    
    for amount, unit in matches:
        amount = int(amount)
        unit = unit.lower()
        
        if unit in ['day', 'days']:
            total_delta += datetime.timedelta(days=amount)
        elif unit in ['week', 'weeks']:
            total_delta += datetime.timedelta(weeks=amount)
        elif unit in ['hour', 'hours', 'h']:
            total_delta += datetime.timedelta(hours=amount)
        elif unit in ['minute', 'minutes', 'min']:
            total_delta += datetime.timedelta(minutes=amount)

    return total_delta
