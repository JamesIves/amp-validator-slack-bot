#!/usr/bin/python
# -*- coding: utf-8 -*-
from constants import SLACK_BOT_TOKEN
from slackclient import SlackClient

# This should be replaced with the name of your bot user.
BOT_NAME = 'amp-validator'

slack_client = SlackClient(SLACK_BOT_TOKEN)

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')

        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("The BOT_ID token for " + user['name'] + "' is " + user.get('id'))
    else:
        print("Unable to find a user with the name " + BOT_NAME)