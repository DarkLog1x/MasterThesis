import os
from novaclient import client as client_nova
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session
from neutronclient.v2_0 import client as client_neutron
from os import environ as env
import json
from bson.json_util import dumps
##
# Will read the config file
##


def OpenStackServerList():
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client_neutron.Client(session=sess)
    nova_client = client_nova.Client('2.1', session=sess)

    server_list = nova_client.servers.list(detailed=True)
    retlist = []
    for i in server_list:
        retlist.append(i.id)
    return retlist


def OpenStackRouterList():
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client_neutron.Client(session=sess)
    nova_client = client_nova.Client('2.1', session=sess)

    routers_list = neutron.list_routers(retrieve_all=True)
    bartmp = dumps(routers_list)
    dumpIn = json.loads(bartmp)
    out = json.dumps(dumpIn, indent=4, sort_keys=True)
    retlist = []
    retlist.append(out)
    return retlist
    # server_list = nova_client.servers.list(detailed=True)
    # retlist = []
    # for i in server_list:
    # retlist.append(i.id)
    # return retlist


def OpenStackNetworkList():
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client_neutron.Client(session=sess)
    nova_client = client_nova.Client('2.1', session=sess)

    network_list = neutron.list_networks()
    retlist = []
    retlist.append(network_list)
    return retlist


def OpenStackSeucurityGroups():
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client_neutron.Client(session=sess)
    nova_client = client_nova.Client('2.1', session=sess)

    securitygroup_list = neutron.list_security_groups()
    retlist = []
    retlist.append(securitygroup_list)
    return retlist


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

# Look at image name on opnestack server show (id of server) to ge the image of the vm  openstack image show (id of vm)
#
# ###
# look at slack bot -- if they can compunicate back
#
# ###
# openstack network list
