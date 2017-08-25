#!/usr/bin/python
# -*- coding: utf-8 -*-
BOT_ID = str(os.environ.get('BOT_ID'))
SLACK_BOT_TOKEN = str(os.environ.get('SLACK_BOT_TOKEN'))
AT_BOT = "<@" + BOT_ID + ">"


# Chartbeat Endpoints
CHARTBEAT_ENDPOINT = str(os.environ.get('CHARTBEAT_ENDPOINT'))
CHAETBEAT_OUTPUT_CHANNEL = str(os.environ.get('CHARTBEAT_OUTPUT_CHANNEL'))
CHARTBEAT_INTERVAL_TIME = int(os.environ.get('CHARTBEAT_INTERVAL_TIME'))


# Commands
VALIDATE_CHARTBEAT_COMMAND = 'chartbeat validate'
VALIDATE_CHARTBEAT_LAST_COMMAND = 'chartbeat last'
VALIDATE_COMMAND = 'validate'
HELP_COMMAND = 'help'
