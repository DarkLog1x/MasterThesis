import tinydb
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
    f = open('config', 'r')
    commands = []
    for line in f:
        if line[0] is not '#':
            commands.append(line)

    return commands


def checkIfConfigIfFollowed(commands):
    db = tinydb.TinyDB('./db.json')
    key = tinydb.Query()
    for command in commands:
        values = command.split(" - ")
        print values
        db.search(tinydb.where('port: 22').field.exists())
