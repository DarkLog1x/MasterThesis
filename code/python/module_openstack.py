import subprocess
import socket
import json
import os
import xml.etree.ElementTree
import database

##
# This modual will do all the work in running NMAP and extracting the needed data.
# A list of IP addressed is feed into the function
# Will call database.PrintList to add the found data into the list
##


def OpenStackData(nova_client, glance, neutron):
    tmpserverList = []
    server_list = nova_client.servers.list(detailed=True)
    for i in server_list:
        if i.image != "":
            image = glance.images.get(i.image['id'])
            database.MongoDBUpdate(
                i.id, "OpenStack_info", ("user_id", i.user_id))
            database.MongoDBUpdate(
                i.id, "OpenStack_info", ("image_id", image['id']))
            database.MongoDBUpdate(
                i.id, "OpenStack_info", ("image_name", image['name']))
            database.MongoDBUpdate(
                i.id, "OpenStack_info", ("updated_at", image['updated_at']))
            database.MongoDBUpdate(
                i.id, "OpenStack_info", ("created_at", image['created_at']))
