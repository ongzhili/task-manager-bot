import datetime
import re
from discord.ext import commands

'''
When given a time string (e.g 5 hours 3 minutes), parses it into a timedelta
'''
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

'''
Converts the due time to a unix timestamp
'''
def duedate_in_unix_timestamp(time_delta):
    due_time = datetime.datetime.now().replace(second=0, microsecond=0) + time_delta
    unix_timestamp = int(due_time.timestamp())
    return unix_timestamp