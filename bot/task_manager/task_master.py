import asyncio
import datetime
import sched
import time
from discord.ext import commands, tasks
import discord

# async def setup(bot):
#     bot.add_cog(TaskChecker(bot))

class TaskChecker(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.scr = sched.scheduler(time.time, time.sleep)
        self.checkForDueTasks.start()
        self.start_task_loop.start()

    '''
    ## Task that checks for due tasks every minute

    Polls db for tasks due in the next minute, then builds a schedule to send a DM to those that have a due task.
    '''
    @tasks.loop(minutes = 1) # repeat after every 30 minutes
    async def checkForDueTasks(self):
        print("Checking for Tasks that are due in the next 1 minutes:")
        matching_entries = self.checker()

        def build_sched(matching_entries, scr):
            for entry in matching_entries:
                print(entry)
                scr.enterabs(entry['time'], 1, asyncio.create_task, argument=(self.send_dm(entry),))
        if matching_entries:
            print("Matching entries found:")
            build_sched(matching_entries, self.scr)
        else:
            print("No matching entries found.")


    @tasks.loop(seconds=1)
    async def start_task_loop(self):
        await self.run_scheduler()

    async def run_scheduler(self):
        while True:
            self.scr.run(blocking=False)  # Run the scheduler without blocking
            await asyncio.sleep(1)  # Sleep to prevent busy waiting
    '''
    Helper function to check for all tasks due in the next minute.
    '''
    def checker(self):
    # Get the current time
        WINDOW = 1
        now = datetime.datetime.now()
        now = now.replace(second=0, microsecond=0)
        now = now.timestamp()
        time_window = WINDOW * 60 

        # Get a reference to the 'users' node
        users_ref = self.db.reference('users')

        # Dictionary to store matching tasks
        matching_tasks = []

        # Iterate through all users
        all_users = users_ref.get()
        if all_users:
            for user_id, user_data in all_users.items():
                if 'tasks' in user_data:
                    for task_id, task_info in user_data['tasks'].items():
                        task_time = int(task_info['time'])
                        # Check if the task time is within the next 10 minutes
                        if now <= task_time < now + time_window:
                            matching_tasks.append({
                                'user_id': user_id,
                                'task_id': task_id,
                                'task': task_info['task'],
                                'time': task_time
                            })

        return matching_tasks
        
    async def send_dm(self, tsk):
        try:
            user = await self.bot.fetch_user(tsk['user_id'])
            await user.send(f'Reminder: {tsk["task"]}')
            print('Message sent to {user.name} successfully')
            ref = self.db.reference(f'users/{tsk["user_id"]}/tasks/{tsk["task_id"]}')
            ref.delete()
        except discord.HTTPException:
            print('Failed to send the message. The user may have DMs disabled.')
        except discord.NotFound:
            print('User not found. Please check the user ID.')
