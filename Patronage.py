import gspread
import re
import random
from utilities import *

credentials = {
    "type": "service_account",
    "project_id": "undaunteddiscordbot",
    "private_key_id": "b815b93c7e0bba1070d4a2c875e4994f02d43f39",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4eHKbjM5qeK4k\n7Wu18aGFM/QQ7HjSKNk3/qpGgA0cdPVM6iSTD/Eew+/WkttRrWn211NjLDkq86GX\nemTOeTuajoUcuitWRwOR19N79qL66RZUBZoGnlA1z/3pQfX8mrxhn7KFVBOA66fy\nArf+UoKoKZQ2Qe8G8LIQxfM+ZT9zF5k1KfmKR6bvqB38L3MRMSPStSxbFzylkwJH\n9Czq+LNnIyYmyfB0qPBYwMlEDT2aPi7hzWXku9iX2qQwua0+lYOSeVyPeFfm3JJX\nwP+/iON4DU3Qq+5BBe67shoz2CbGtDphF3fHX0i6gxWv7fvaYta0xyGYXMVdYD1W\n8sftBDKPAgMBAAECggEAF0siUbEEiZ5GgyQ1wypJVowaaB6sHQGKeE8gijl2Ll84\ncGdqieVr8ZIVUXeG2Tf4FvLWtUGq0FkmUP3kB8x4McqIVXnOqhzafwqNSmx45Q0U\nxDRW4DoSb9EdQ1yQZr7VRdCIFtzof5GCSgV83VDm7bweWoGV4L75BTQxxHG9gtdD\nJJ5BAwkGLblR5j9gqU1jYLhMN/WjK8BIyBrfAvIHANjv4rLK+jjj4Ut5h4CxsxpW\n/Aqwti7T0NwiCLERhbIENkNxbFd7hr4q+yjoCW23LCUbjnx1XdiIlJuKbty8iQsu\nBYNKXvolEHv8FEzKdSSz9Nvi4esl6Hm9Dg7pBiJuRQKBgQD4Gd1L21w3q49kdh16\no0j4GKtzy2dxxVbNi3OMcUYbvX3TwUees0iG+WBcX2I9TRTzsDUbRW4oZftGJ88s\nriTwO1aV2CzDTMBgnalkqVjP9c6/RlRgpHsjB8K2ujqIkTxeH+vbQzzO4Fj98ff3\nl+PGttktlxEkdKy/Roek8T/uqwKBgQC+V/czrvMRom6Ugh4RltEGrdgicVgemqYk\nDO2LVlKWlXZ2zW26FQcxXA5AuB13/nZFd7vfvzIoC6OK/QS6a10DITJIwbE0ex9/\nUQK0DlqAAEN8EcoAJzm32pmHMTE90rvGhFnQ4VsZw9vnQjIBqcw52DmYsSCSpO8m\nJ29bUGu7rQKBgBADa1soD22wbxLm5MQzodQRk49nw4d+WzntFEouTX4g3uw5/2to\n2veLRQLxTR/zx7Rq3SKjepa07mD61M5ndw7iZZZKW6lHXOtfgb1ziL3zeaKy4WNT\nencqWxD8OCb0aNcSbGC8mEIqDNRnN8ANV7BNwPrGU17tAPFflgW5ZIz9AoGAbsIT\nB1D7Abzp6aKZSpTexqssBEa+BvjoSjv3kcfGQPdxuompGsmXqOIvLPu1shgwzBVz\nDixcTC8RmBPIx40nz2VmtC15JteqKVSDZTCg+rCslCppx5MLo+8gvSkjxRy1xTtI\nZCJt910fvb6oCI28V8B5K1+OW6Z7vlDeHF18gvUCgYBJZ0B6zhIdGyCBQ+I4gDxh\n1FfviL35Wz0qJxHnyEAnjm4X33p6jDzNyVrwr6lJyL3ixFm77y7Qes6asF9s61UF\n51GJrjLRCcC+9X1WSmB1rGM+W76SUXKBxrwj0mNe922rm+lgJPRAx7jkjVvAeRMe\nkFtJXHo5iVWUSEVV5MW6lw==\n-----END PRIVATE KEY-----\n",
    "client_email": "undaunted@undaunteddiscordbot.iam.gserviceaccount.com",
    "client_id": "112647756200358490521",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/undaunted%40undaunteddiscordbot.iam.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(credentials)
sh = gc.open("Guardian and Patronage Doc")
patronage_tables = sh.worksheet("Patronage Tasks")
guardians = sh.worksheet("Guardian Table")
wander = sh.worksheet("Wander Events")


def get_legend_personality(legend):
    criteria = re.compile('(?i)^' + legend + "$")  # get all the cells with the name of the legend in them in column 1
    matches = patronage_tables.find(criteria, in_column=1)
    if matches is None:  # checks for a non-existent legend. Exits the code if so.
        return "A legend with this name could not be found. Please make sure that the legend's name is spelled correctly."
    selected_task = matches.row  # Selects random task row among the valid options
    personality = "__**" + legend.title() + "**__\n" + "**Personality:** " + patronage_tables.cell(selected_task, 2).value
    return personality


def get_patronage_task(legend, category):
    criteria = re.compile('(?i)^' + legend + "$")  # get all the cells with the name of the legend in them in column 1
    matches = patronage_tables.findall(criteria, in_column=1)
    if len(matches) == 0:  # checks for a non-existent legend. Exits the code if so.
        return ["A legend with this name could not be found. Please make sure that the legend's name is spelled "
                "correctly."]
    # Continues with selection process.
    options = []  # Possible options for random selection
    for op in matches:
        if patronage_tables.cell(op.row, 3).value == category.title():
            options.append(op.row)  # Adds the row with the matching request category to the possible options
    selected_task = random.choice(options)  # Selects random task row among the valid options
    sub_tasks_l = patronage_tables.get_values("E{0}:V{0}".format(selected_task))
    sub_tasks = [item for sublist in sub_tasks_l for item in sublist]
    subtask = "**" + patronage_tables.cell(selected_task, 4).value + "**\n" + random.choice(sub_tasks)  # Selects the sub task
    personality = "__**" + legend.title() + "**__\n" + "**Personality:** " + patronage_tables.cell(selected_task, 2).value
    subtask_array = segment_text(subtask, "Legend")
    personality_array = [personality]
    return personality_array + subtask_array

def get_guardian_info(area):
    criteria = re.compile('(?i)^' + area + "$")
    matches = guardians.findall(criteria, in_column=1)
    if len(matches) == 0:
        return "There is no location by this name with a guardian present."
    else:
        match = random.choice(matches)
        row = match.row
        ret_val = guardians.cell(row, 2).value
        ret_val += guardians.cell(row, 3).value
        return ret_val
      
def get_wander_event():
    wander_event_effects = wander.col_values(2)
    wander_event_names = wander.col_values(1)
    index = random.randrange(1, len(wander_event_names))
    name = "**" + wander_event_names[index] + "**"
    effect =  "\n\n" + wander_event_effects[index]
    ret_string = name
    ret_string += effect
    return ret_string


"""
test_string = patronage_tables.cell(1, 1).value
test_array = test_string.split("\n")
for i in test_array:
    print(i)
"""