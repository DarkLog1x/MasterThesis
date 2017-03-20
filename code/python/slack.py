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

##
# Connect to Slack and print output!
##
AT_BOT = None
EXAMPLE_COMMAND = None


def main():
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
    try:
        slack.channels.create('#' + GroupName)
    except:
        pass

    try:
        slack.channels.invite('#' + GroupName, bot_id)
    except:
        pass

    slackBot(slack_client, bot_id, incorrectVMS)
    # repeatBot([], incorrectVMS, slack_client, GroupName[1])


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
    if input[0] == "vmproblems":
        response = CheckDatabase.DatabaseCheckSpecific(input[1])
        for line in response:
            slack_client.api_call("chat.postMessage", channel=channel,
                                  text=line, as_user=True)
    elif input[0] == "vmdatabase":
        response = CheckDatabase.DatabaseCheckGetFullDatabase(input[1])
        for line in response:
            slack_client.api_call("chat.postMessage", channel=channel,
                                  text=line, as_user=True)
    elif input[0] == 'vmstatus':
        response = CheckDatabase.FindSelected(input[1], input[2])
        for line in response:
            slack_client.api_call("chat.postMessage", channel=channel,
                                  text=line, as_user=True)
    elif input[0] == 'fullreport':
        response = CheckDatabase.DatabaseCheckFull()
        for line in response:
            slack_client.api_call("chat.postMessage", channel=channel,
                                  text=line, as_user=True)
    else:
        response = "Not sure what you mean. The following are excepted: \"vmproblems *ID*\", \"vmdatabase *ID* \", \"vmstatus\" , \"fullreport\" "
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
