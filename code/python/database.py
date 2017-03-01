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
    for command in commands:
        values = command.split(" - ")
        # what = values[1].split("\n")
        # print what[0]
        # print values[1].strip()
        tmp = db.search(tinydb.where(values[0]) != values[1].strip())
        print values[0]
        print values[1]
        print tmp[0]
        print len(tmp)
