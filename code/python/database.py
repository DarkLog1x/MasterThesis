import tinydb
import os
from collections import Counter
import pymongo
from pymongo import MongoClient
from slack import SlackerConnect
##
# Will be called to add data to the db.json file. must send an ID followed by type of data and then by the data
##


def PrintList(instanceID, type,  data):
    db = tinydb.TinyDB('./db.json')
    instanceSearch = tinydb.Query()
    key = {"ID": instanceID}
    data = {type: {data[0]: data[1]}}
    if db.search(instanceSearch.id == instanceID):
        db.update({type: [{data[0]:data[1]}]}, instanceSearch.id == instanceID)
    else:
        db.insert(key, data)


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


##
# This is the function that will be called to see if the confige provided is followed
##

def checkIfConfigIfFollowed(commands):
    db = tinydb.TinyDB('./db.json')
    key = tinydb.Query()
    incorrectVMS = []
    incorrectVMS.append("Tenant name: " + os.environ['OS_TENANT_NAME'])
    incorrectVMS.append("Tenant ID: " + os.environ['OS_PROJECT_NAME'])
    commandList = []
    for command in commands:
        values = command.split(" - ")
        commandList.append(values[0])
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
    contents = db.table('_default').all()

    schema = Counter(frozenset(doc.keys()) for doc in contents)
    keyList = []
    for i in schema.iteritems():
        for j in i[0]:
            if j not in commandList and j not in ['id', 'ip_internal', 'ip_external']:
                if j not in keyList:
                    keyList.append(j)
    for i in keyList:
        tmp = db.search(tinydb.where(i) == 'open')
        for items in tmp:
            it = "Server ID: " + \
                items['id'] + " | " + \
                i + " has been found " + items[i] + " and is not in the config"
            incorrectVMS.append(it)

    return incorrectVMS


def MongoDBCreate(ServerList):
    client = MongoClient('localhost', 27017)
    db = client.vm_database
    vms = db.vms
    for server in ServerList:
        vms.update_one({"ID": server}, {"$set": {"ID": server}}, upsert=True)


def MongoDBUpdate(instanceID, type,  data):
    client = MongoClient('localhost', 27017)
    db = client.vm_database
    key = {"ID": instanceID}
    data = {"$set": {type + "." + data[0]: data[1]}}
    print key
    print data
    vms = db.vms
    try:
        post_id = vms.update_one(key, data, upsert=True)
    except:
        pass


def ConfigCheck(commands, serverID):
    client = MongoClient('localhost', 27017)
    db = client.vm_database
    incorrectVMS = []
    vms = db.vms
    for command in commands:
        values = command.split(" - ")
        area = values[0].split(":")
        # print os.environ['HOME']
        #
        tmp = vms.find(
            {"$and": [{area[0] + "." + area[1].strip(): {"$ne": values[1].strip()}}, {"ID": serverID}]})
        for item in tmp:
            it = "Server ID: " + item['ID'] + " | " + area[1] + ": " + \
                item[area[0]][area[1].strip()] + " -- Should be = " + values[1]
            incorrectVMS.append(it)
    return incorrectVMS


def ConfigCheckInversePorts(commands, serverID):
    client = MongoClient('localhost', 27017)
    db = client.vm_database
    incorrectVMS = []
    vms = db.vms
    portlist = []

    for command in commands:
        values = command.split(": ")
        area = values[1].split(" - ")
        portlist.append(area)

    contents = vms.find({"ID": serverID})
    for item in contents:
        for port in item['ports']:
            tmp = [port, item['ports'][port]]
            if tmp not in portlist:
                it = "Server ID: " + \
                    item['ID'] + " | " + port + " has been found " + \
                    item['ports'][port] + " and is not in the config"
                incorrectVMS.append(it)
    return incorrectVMS


def DatabaseCheckFull(serverlist):
    commands = ProperConfig()
    incorrectVMS = []
    incorrectVMS.append("Tenant name: " + os.environ['OS_TENANT_NAME'])
    incorrectVMS.append("Tenant ID: " + os.environ['OS_PROJECT_NAME'])
    for vm in serverlist:
        incorrectVMS.append("--Server With ID: " + vm)
        incorrectVMS += ConfigCheck(commands, vm)
        incorrectVMS += ConfigCheckInversePorts(commands, vm)
    SlackerConnect(incorrectVMS)
    # incorrectVMS = database.checkIfConfigIfFollowed(commands)
    # database.SlackerConnect(incorrectVMS)


###
# Set a config flag for the admin to be able to choose what type of informatation is sent
# is it all of the information
# or only the changes
# make a slack channel for each project id
#
# #####
# does slack go over ssl
# Look at image name on opnestack server show (id of server) to ge the image of the vm  openstack image show (id of vm)
#
# ###
# look at slack bot -- if they can compunicate back
#
# ###
# openstack network list
#
# ###
# MongoDB for database
#
# #####
# Look at security groups
#
