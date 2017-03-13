import tinydb
import os
from slacker import Slacker
from collections import Counter
import pymongo
from pymongo import MongoClient

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


##
# Connect to Slack and print output!
##

def SlackerConnect(incorrectVMS):
    f = os.environ['SLACK_KEY']
    slack = Slacker(f)
    try:
        slack.channels.create('#OSIDS')
    except:
        pass
    slack.chat.post_message('#OSIDS', "##############################")
    for message in incorrectVMS:
        slack.chat.post_message('#OSIDS', message)
    slack.chat.post_message('#OSIDS', "##############################")


def MongoDBConnection(instanceID, type,  data):
    client = MongoClient()
    db = client.database
    key = {"ID": instanceID}
    data = {type:
            {data[0]: data[1]}}
    db.update_one(key, data, {upsert: true})


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
