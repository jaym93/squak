# File: server.py
# Author: Jayanth M (jayanth6@gatech.edu)
# Created: 23-12-2016 12:48 PM
# Project: squak

from tokens import *
from intent_parser import *
import os
import time
from slackclient import SlackClient
import re

BOT_NAME = 'homie'
AT_BOT = "<@"+BOT_ID+">"

slack_client = SlackClient(API_TOKEN)

### USE BELOW TEMPLATE TO CALL SLACK RTM APIS
# pp.pprint(slack_client.api_call("users.list"))

### THIS SCRIPT FINDS BOT_ID FOR THE DEFINED BOT
# if __name__ == "__main__":
#     api_call = slack_client.api_call("users.list")
#     if api_call.get('ok'):
#         # retrieve all users so we can find our bot
#         users = api_call.get('members')
#         for user in users:
#             if 'name' in user and user.get('name') == BOT_NAME:
#                 print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
#     else:
#         print("could not find bot user with the name " + BOT_NAME)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if re.match(r'Hello .*', command, re.I):
        response = "Hello yourself"
    elif re.match(r'Hey .*', command, re.I):
        response = "Hello"
    elif re.match(r'Yo .*', command, re.I):
        response = "Yo, what's up?"
    else:
        response = parse_intent(command)
        print(response)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    # print(output_list)
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Homie is up and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")