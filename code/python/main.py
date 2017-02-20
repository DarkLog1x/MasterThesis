#!/usr/bin/python
import sys
import time
import os
import sys
import inspect
from os import environ as env
import subprocess

from novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session
from neutronclient.v2_0 import client

# loader = loading.get_plugin_loader('password')
# auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
# username=env['OS_USERNAME'],
# password=env['OS_PASSWORD'],
# project_name=env['OS_PROJECT_NAME'],
# user_domain_name=env['OS_USER_DOMAIN_NAME'],
# project_domain_name=env['OS_PROJECT_DOMAIN_NAME'])

# sess = session.Session(auth=auth)
# nova = client.Client('2.1', session=sess)
# print(nova.servers.list())


def main():
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client.Client(session=sess)
    netw = neutron.list_networks()

    print_values(netw, 'networks')


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
