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
from slackclient import SlackClient
import CheckDatabase
import threading

##
# Connect to Slack and print output!
##
AT_BOT = None
EXAMPLE_COMMAND = None


def main():
    environmentVariables()
    auth = get_credentials()
    sess = session.Session(auth=auth)
    neutron = client_neutron.Client(session=sess)
    nova_client = client_nova.Client('2.1', session=sess)

    ServerList = DeviceList(neutron, nova_client)
    incorrectVMS = CheckDatabase.DatabaseCheckFull(ServerList)

    f = os.environ['SLACK_KEY']
    BOT_NAME = 'isaas'
    bot_id = None

    slack_client = SlackClient(f)

    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                bot_id = user.get('id')

    else:
        print("could not find bot user with the name " + BOT_NAME)

    # starterbot's ID as an environment variable

    # constants
    slackBot(slack_client, bot_id, incorrectVMS)


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


def handle_command(slack_client, command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    EXAMPLE_COMMAND = "do"
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output, bot_id):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    AT_BOT = "<@" + bot_id + ">"
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                    output['channel']
    return None, None


def slackBot(slack_client, bot_id, incorrectVMS):
    READ_WEBSOCKET_DELAY = 5
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        SlackChennelThread(slack_client, bot_id)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


def SlackChennelThread(slack_client, bot_id):
    threading.Timer(1.0, SlackChennelThread, [slack_client, bot_id]).start()
    command, channel = parse_slack_output(
        slack_client.rtm_read(), bot_id)
    if command and channel:
        handle_command(slack_client, command, channel)


if __name__ == "__main__":
    main()
