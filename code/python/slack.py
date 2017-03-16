import os
import time
from slackclient import SlackClient
##
# Connect to Slack and print output!
##
AT_BOT = None
EXAMPLE_COMMAND = None


def SlackerConnect(incorrectVMS):
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
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        GroupName = incorrectVMS[0].split(": ")
        print slack_client.api_call("channels.join", name=GroupName[1])
        for vms in incorrectVMS:
            print slack_client.api_call(
                "chat.postMessage", channel=GroupName[1], text=vms, as_user=True)
        while True:
            command, channel = parse_slack_output(
                slack_client.rtm_read(), bot_id)
            if command and channel:
                handle_command(slack_client, command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
