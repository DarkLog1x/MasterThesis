import os
import pymongo
from pymongo import MongoClient
from novaclient import client as client_nova
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session
from neutronclient.v2_0 import client as client_neutron
import inspect
from os import environ as env
import subprocess
import json
from bson.json_util import dumps
from environmentVariables import environmentVariables
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


def dbConnect():
    client = MongoClient('localhost', 27017)
    db = client.vm_database
    return db.vms


def ConfigCheck(commands, serverID):
    incorrectVMS = []
    vms = dbConnect()
    for command in commands:
        values = command.split(" - ")
        area = values[0].split(":")
        tmp = vms.find(
            {"$and": [{area[0] + "." + area[1].strip(): {"$ne": values[1].strip()}}, {"ID": serverID}]})
        for item in tmp:
            try:
                it = "Server ID: " + item['ID'] + " | " + area[1] + ": " + \
                    item[area[0]][
                        area[1].strip()] + " -- Should be = " + values[1]
                incorrectVMS.append(it)
            except:
                pass
    return incorrectVMS


def ConfigCheckInversePorts(commands, serverID):
    incorrectVMS = []
    vms = dbConnect()
    portlist = []

    for command in commands:
        values = command.split(": ")
        area = values[1].split(" - ")
        portlist.append(area)

    contents = vms.find({"ID": serverID})
    for item in contents:
        try:
            for port in item['ports']:
                tmp = [port, item['ports'][port]]
                if tmp not in portlist:
                    it = "Server ID: " + \
                        item['ID'] + " | " + port + " has been found " + \
                        item['ports'][port] + " and is not in the config"
                    incorrectVMS.append(it)
        except:
            pass
    return incorrectVMS


def FindSelected(key, value):
    incorrectVMS = []
    vms = dbConnect()

    incorrectVMS = []
    listoutput = vms.find({key: value})
    tmp1 = dumps(listoutput)
    tmp = json.loads(tmp1)
    for i in tmp:
        incorrectVMS.append(i["ID"] + " -- " + key + ": " + value)
    return incorrectVMS


def DatabaseCheckGetFullDatabase(ServerID):
    incorrectVMS = []
    vms = dbConnect()

    incorrectVMS = []
    incorrectVMS.append("Tenant name: " + os.environ['OS_TENANT_NAME'])
    incorrectVMS.append("Tenant ID: " + os.environ['OS_PROJECT_NAME'])

    listoutput = vms.find({"ID": ServerID})
    bartmp = dumps(listoutput)
    dumpIn = json.loads(bartmp)
    out = json.dumps(dumpIn, indent=4, sort_keys=True)
    incorrectVMS.append(out)
    return incorrectVMS


def DatabaseCheckSpecific(ServerID):
    vms = dbConnect()

    commands = ProperConfig()
    incorrectVMS = []
    incorrectVMS.append("Tenant name: " + os.environ['OS_TENANT_NAME'])
    incorrectVMS.append("Tenant ID: " + os.environ['OS_PROJECT_NAME'])
    incorrectVMS += ConfigCheck(commands, ServerID)
    incorrectVMS += ConfigCheckInversePorts(commands, ServerID)
    return incorrectVMS
    # incorrectVMS = database.checkIfConfigIfFollowed(commands)
    # database.SlackerConnect(incorrectVMS)


def DatabaseCheckFull():
    environmentVariables()
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client_neutron.Client(session=sess)
    nova_client = client_nova.Client('2.1', session=sess)

    ServerList = DeviceList(neutron, nova_client)

    commands = ProperConfig()
    incorrectVMS = []
    incorrectVMS.append("Tenant name: " + os.environ['OS_TENANT_NAME'])
    incorrectVMS.append("Tenant ID: " + os.environ['OS_PROJECT_NAME'])
    for vm in ServerList:
        incorrectVMS.append("--Server With ID: " + vm)
        incorrectVMS += ConfigCheck(commands, vm)
        incorrectVMS += ConfigCheckInversePorts(commands, vm)
    incorrectVMS.append("##############################")
    return incorrectVMS
    # incorrectVMS = database.checkIfConfigIfFollowed(commands)
    # database.SlackerConnect(incorrectVMS)


def DatabaseCheckChanges(incorrectVMS_old, incorrectVMS_new):
    s = set(incorrectVMS_old)
    incorrectVMS = [x for x in incorrectVMS_new if x not in s]
    return incorrectVMS


def get_credentials():
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                    username=env['OS_USERNAME'],
                                    password=env['OS_PASSWORD'],
                                    project_name=env['OS_PROJECT_NAME'],
                                    user_domain_name=env[
                                        'OS_USER_DOMAIN_NAME'],
                                    project_domain_name=env['OS_PROJECT_DOMAIN_NAME'])
    return auth


def DeviceList(neutron, nova_client):
    list = {}
    server_list = nova_client.servers.list(detailed=True)
    ip_list = nova_client.floating_ips.list()
    for server in server_list:
        list.setdefault(server.id, [])
        list[server.id].append(server.name)
    for ip in ip_list:
        if(ip.instance_id != None):
            list[ip.instance_id].append(ip.fixed_ip)
            list[ip.instance_id].append(ip.ip)
    return list
