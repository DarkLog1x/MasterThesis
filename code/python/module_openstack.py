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

def OpenStackData(nova_client):
    tmpserverList = []
    server_list = nova_client.servers.list(detailed=True)
    print server_list
    for i in server_list:
        database.MongoDBUpdate(i.id, "OpenStack_info", ("user_id", i.user_id))
        database.MongoDBUpdate(
            i.id, "OpenStack_info", ("image_id", i.image['id']))
