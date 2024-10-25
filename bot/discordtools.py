'''
Converts discord formatted id to firebase key
'''
def discord_id_to_firebase_entry(authorid):
    return str(authorid).replace('.', '_').replace('$', '_').replace('#', '_').replace('[', '_').replace(']', '_')

'''
Sorts the given task list by due time
'''
def tasks_sorted_by_time(tasks):
    return sorted(tasks.items(), key=lambda x: x[1]['time'])

'''
Returns a string representation of the given list of tasks
'''
def stringify_tasks(tasks):
    tasks = dict(tasks_sorted_by_time(tasks))
    body = ""
    for idx, (task_id, task) in enumerate(tasks.items()):
        body += f"{idx + 1}: '{task['task']}' by <t:{int(task['time'])}>\n"
    return body