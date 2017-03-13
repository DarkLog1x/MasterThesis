#!/usr/bin/python
import sys
import time
import sched
import os
import sys
import inspect
from os import environ as env
import subprocess

from novaclient import client as client_nova
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session
from neutronclient.v2_0 import client as client_neutron
from subprocess import call
import module_nmap
import module_sshscan
import database
from twisted.internet import task
from twisted.internet import reactor


##
# Mian function that will run the code. This is run via a cron job!
##
def main():
    environmentVariables()
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client_neutron.Client(session=sess)
    nova_client = client_nova.Client('2.1', session=sess)

    ServerList = DeviceList(neutron, nova_client)
    module_nmap.nmapscan(ServerList)
    # module_sshscan.sshscan(ServerList, 2)
    # module_sshscan.sshscan(ServerList, 1)
    # commands = database.ProperConfig()
    # incorrectVMS = database.checkIfConfigIfFollowed(commands)
    # database.SlackerConnect(incorrectVMS)


##
# This will set the needed environment varibables
# This needs to be filled out to match the rc file form OpenStack
##

def environmentVariables():
    f = open('keys', 'r').read().splitlines()
    os.environ["OS_PASSWORD"] = f[1]
    os.environ["SLACK_KEY"] = f[0]
    os.environ["OS_AUTH_URL"] = "https://smog.uppmax.uu.se:5000/v3"
    os.environ["OS_TENANT_ID"] = "bfe0cca393a5473189c05f22a731bfd0"
    os.environ["OS_TENANT_NAME"] = "c2015003"
    os.environ["OS_PROJECT_NAME"] = "c2015003"
    os.environ["OS_USERNAME"] = "aleko"
    os.environ["OS_USER_DOMAIN_NAME"] = "Default"
    os.environ["OS_PROJECT_DOMAIN_NAME"] = "Default"
    os.environ["OS_IDENTITY_API_VERSION"] = "3"
    os.environ["OS_AUTH_VERSION"] = "3"
    os.environ["OS_REGION_NAME"] = "UPPMAX"


##
# This will return a list of server name, internal ip, and floating ip.
##

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


##
# Loads the credinetials into the runtime
##

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


##
# Bellow are helper print functiosn that are used in viewing the OpenStack information
##

def printVlaues():
    # This will get and print the networks
    print("######networks#######")
    netw = neutron.list_networks()
    print_values(netw, 'networks')

    # This will get and print the routes
    print("############routers############")
    routers_list = neutron.list_routers(retrieve_all=True)
    print_values(routers_list, 'routers')

    # This will get and print the servers
    print("############servers############")
    server_list = nova_client.servers.list(detailed=True)
    print_servers(server_list)

    # This will get the floating ips
    print("################Floating IPS##############")
    ip_list = nova_client.floating_ips.list()
    print_values_ip(ip_list)

    # This will print all the hosts
    print("##############Hosts##################")
    host_list = nova_client.hosts.list()
    print_hosts(host_list)


def print_servers(server_list):
    for servers in server_list:
        print("-" * 35)
        print("server_name : %s" % servers.name)
        print("server_id : %s" % servers.id)
        print("-" * 35)


def print_hosts(host_list):
    for host in host_list:
        print("-" * 35)
        print("host_name : %s" % host.host_name)
        print("service : %s" % host.service)
        print("zone : %s" % host.zone)
        print("-" * 35)


def print_values_ip(ip_list):
    ip_dict_lisl = []
    for ip in ip_list:
        print("-" * 35)
        print("fixed_ip : %s" % ip.fixed_ip)
        print("id : %s" % ip.id)
        print("instance_id : %s" % ip.instance_id)
        print("ip : %s" % ip.ip)
        print("pool : %s" % ip.pool)


def print_values(val, type):
    if type == 'ports':
        val_list = val['ports']
    if type == 'networks':
        val_list = val['networks']
    if type == 'routers':
        val_list = val['routers']
    for p in val_list:
        for k, v in p.items():
            print("%s : %s" % (k, v))
        print('\n')


def print_values_server(val, server_id, type):
    if type == 'ports':
        val_list = val['ports']

    if type == 'networks':
        val_list = val['networks']
    for p in val_list:
        bool = False
        for k, v in p.items():
            if k == 'device_id' and v == server_id:
                bool = True
        if bool:
            for k, v in p.items():
                print("%s : %s" % (k, v))
            print('\n')


if __name__ == "__main__":
    main()
