import os
import pymongo
from pymongo import MongoClient
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


def dbConnect():
    client = MongoClient('localhost', 27017)
    db = client.vm_database
    return db.vms_tmp

# This is the function that will be called to see if the confige provided
# is followed


def MongoDBCreate(ServerList):
    vms = dbConnect()
    for server in ServerList:
        vms.update_one({"ID": server}, {"$set": {"ID": server}}, upsert=True)


def MongoDBUpdate(instanceID, type,  data):
    key = {"ID": instanceID}
    data = {"$set": {type + "." + data[0]: data[1]}}
    vms = dbConnect()
    try:
        post_id = vms.update_one(key, data, upsert=True)
    except:
        pass


def MongoDBDrop():
    vms = dbConnect()
    vms.drop()


def MongoDBswitch():
    client = MongoClient('localhost', 27017)
    db = client.vm_database
    db.vms.drop()
    client.admin.command('copydb',
                         fromdb='vms_tmp',
                         todb='vms')


def MongoDBClean(ServerList):
    vms = dbConnect()
    i = vms.find()
    for vm in i:
        if vm['ID'] not in ServerList:
            vms.remove({"ID": vm['ID']})

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
# if the server id is no more drop it formt he database
#
