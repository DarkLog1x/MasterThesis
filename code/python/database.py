import tinydb
import os
from slacker import Slacker
##
# Will be called to add data to the db.json file. must send an ID followed by type of data and then by the data
##


def PrintList(instanceID, type,  data):
    db = tinydb.TinyDB('./db.json')
    instanceSearch = tinydb.Query()
    if db.search(instanceSearch.id == instanceID):
        db.update({type: data}, instanceSearch.id == instanceID)
    else:
        db.insert({'id': instanceID, type: data})

##
# Will read the config file
##


def ProperConfig():
    f = open('config', 'r').read().splitlines()
    commands = []
    for line in f:
        if line[0] is not '#':
            commands.append(line)

    return commands

#>>> db = TinyDB(storage=MemoryStorage)


def checkIfConfigIfFollowed(commands):
    db = tinydb.TinyDB('./db.json')
    key = tinydb.Query()
    incorrectVMS = []
    incorrectVMS.append("Tenant name: " + os.environ['OS_TENANT_NAME'])
    incorrectVMS.append("Tenant ID: " + os.environ['OS_PROJECT_NAME'])
    for command in commands:
        values = command.split(" - ")
        # print os.environ['HOME']
        #
        tmp = db.search(tinydb.where(values[0]) != values[1].strip())
        for items in tmp:
            it = "Server ID: " + \
                items['id'] + " | " + \
                values[0] + ": " + items[values[0]] + \
                " -- Should be = " + values[1]
            incorrectVMS.append(it)
    # for b in incorrectVMS:
        # print b

    return incorrectVMS


def SlackerConnect(incorrectVMS):
    f = os.environ['SLACK_KEY']
    slack = Slacker(f)
    try:
        slack.channels.create('#OSIDS')
    except:
        pass
    for message in incorrectVMS:
        slack.chat.post_message('#OSIDS', message)
