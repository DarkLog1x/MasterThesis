#!/usr/bin/python
import sys
import time
import sched
import os

from subprocess import call
from slackclient import SlackClient
import CheckDatabase
import threading
from slacker import Slacker
import OpenStack_query as OSq

##
# Connect to Slack and print output!
##
AT_BOT = None
EXAMPLE_COMMAND = None
channelName = None


def main():
    become_daemon()
    incorrectVMS = CheckDatabase.DatabaseCheckFull()
    f = os.environ['SLACK_KEY']
    b = os.environ['SLACK_KEY_NOBOT']
    BOT_NAME = 'isaas'
    bot_id = None

    slack_client = SlackClient(f)

    api_call = slack_client.api_call("users.list")
    GroupName = incorrectVMS[0].split(": ")

    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print(
                    "Bot ID for '" + user['name'] + "' is " + user.get('id'))
                bot_id = user.get('id')

    else:
        print("could not find bot user with the name " + BOT_NAME)

    slack = Slacker(b)
    global channelName
    channelName = GroupName[1].replace(" ", "_")
    try:
        print slack.channels.create('#' + channelName)
    except:
        pass

    try:
        print slack.channels.invite('#' + channelName, bot_id)
    except:
        pass

    slackBot(slack_client, bot_id, incorrectVMS)
    # OSq.OpenStackQuery()
    repeatBot([], incorrectVMS, slack_client, channelName)


##
# Go this from
# https://stackoverflow.com/questions/1423345/can-i-run-a-python-script-as-a-service

def become_daemon(our_home_dir='.', out_log='/dev/null', err_log='/dev/null', pidfile='/var/tmp/daemon.pid'):
    """ Make the current process a daemon.  """

    try:
        # First fork
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed" (%d) %s\n' %
                             (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.chdir(our_home_dir)
        os.umask(0)

        # Second fork
        try:
            pid = os.fork()
            if pid > 0:
                # You must write the pid file here.  After the exit()
                # the pid variable is gone.
                fpid = open(pidfile, 'wb')
                fpid.write(str(pid))
                fpid.close()
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed" (%d) %s\n' %
                             (e.errno, e.strerror))
            sys.exit(1)

        si = open('/dev/null', 'r')
        so = open(out_log, 'a+', 0)
        se = open(err_log, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    except Exception, e:
        sys.stderr.write(str(e))


def repeatBot(incorrectVMS_old, incorrectVMS_new, slack_client, GroupName):
    incorrectVMS = CheckDatabase.DatabaseCheckChanges(
        incorrectVMS_old, incorrectVMS_new)
    if incorrectVMS:
        for line in incorrectVMS:
            slack_client.api_call(
                "chat.postMessage", channel=GroupName, text=line, as_user=True)
        incorrectVMS_old = incorrectVMS_new
        incorrectVMS_new = CheckDatabase.DatabaseCheckFull()
    else:
        incorrectVMS_new = CheckDatabase.DatabaseCheckFull()
    threading.Timer(
        20.0, repeatBot, [incorrectVMS_old, incorrectVMS_new, slack_client, GroupName]).start()


def handle_command(slack_client, command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    input = command.split(" ")
    print input[0]
    print channelName.lower()
    if input[0] != channelName.lower():
        return 0
    if input[1] == "vmproblems":
        response = CheckDatabase.DatabaseCheckSpecific(input[1])
    elif input[1] == "help":
        response = [
            "The following are accepted:\"openstackinfo (\"serverlist\", \"routerlist\", \" networklist\", \"securitygroups\")\", \"vmproblems *ID*\", \"vmdatabase *ID* \", \"vmstatus *key* *value*\" , \"fullreport\" ", "Example: @isaas foo_bar fullreport"]
    elif input[1] == "vmdatabase":
        response = CheckDatabase.DatabaseCheckGetFullDatabase(input[2])
    elif input[1] == 'vmstatus':
        response = CheckDatabase.FindSelected(input[2], input[3])
    elif input[1] == 'fullreport':
        response = CheckDatabase.DatabaseCheckFull()
    elif input[1] == 'openstackinfo':
        if input[2] == 'serverlist':
            response = OSq.OpenStackServerList()
        elif input[2] == 'routerlist':
            response = OSq.OpenStackRouterList()
        elif input[2] == 'networklist':
            response = OSq.OpenStackNetworkList()
        elif input[2] == 'securitygroups':
            response = OSq.OpenStackSeucurityGroups()
        else:
            response = [
                "Not a recognised OpenStack information command. Try \"serverlist\", routerlist\", \" networklist\", \"securitygroups\""]
    else:
        response = [
            "Not sure what you mean. The following are excepted:\"openstackinfo\" \"vmproblems *ID*\", \"vmdatabase *ID* \", \"vmstatus *key* *value*\" , \"fullreport\" "]
    for line in response:
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=line, as_user=True)
        time.sleep(0.5)


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
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        SlackChennelThread(slack_client, bot_id)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


def SlackChennelThread(slack_client, bot_id):
    threading.Timer(1.0, SlackChennelThread, [slack_client, bot_id]).start()
    try:
        command, channel = parse_slack_output(slack_client.rtm_read(), bot_id)
        if command and channel:
            handle_command(slack_client, command, channel)
    except:
        pass

#####
# Add Slacker to create the channel and join the bot to it


if __name__ == "__main__":
    main()
