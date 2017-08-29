#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import schedule
from slackclient import SlackClient
from constants import *
from validate import *
from util import *

slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
        Handles any generic command that is pointed
        towards the bot.
    """
    if command.startswith(VALIDATE_COMMAND):
        # Validates an individual AMP document.
        url = get_target_path(command)
        amp_url = get_amp_path(url)

        if amp_url == 'invalid':
            send_basic_message('Either the URL you included was invalid or there wasn issue reading the address.', channel)

        if amp_url == 'notfound':
            send_basic_message('An AMP document could be found at the provided address', channel)

        else:
            amp_validation_results = validate(amp_url)
            
            if amp_validation_results == 'error':
                send_basic_message('Unable to reach the Cloudflare service, please try again', channel)

            else:
                send_attachment_message(amp_validation_results, channel)

    if command.startswith(VALIDATE_CHARTBEAT_COMMAND):
        # Validates the most recent articles from Chartbeat
        if CHARTBEAT_ENDPOINT:
            update_channel(channel)
            send_basic_message('Validating the top performing articles from Chartbeat, this may take a moment...', channel)
            total = validate_chartbeat_articles()

            # Error handling, makes sure that
            if total is not 'error':
                send_basic_message('Validated %s articles and found %s errors.' % (total['errors'] + total['passes'], total['errors']), channel)

        else:
            send_basic_message('Chartbeat is not properly configured, please refer to the documentation...', channel)

    if command.startswith(VALIDATE_CHARTBEAT_LAST_COMMAND):
        # Provides the results of the most recent Chartbeat check
        errors = get_errors()
        passes = get_passes()

        if CHARTBEAT_ENDPOINT:
            send_basic_message('The last time I ran I checked %s articles and found %s errors.' % (errors + passes, errors), channel)

        else:
            send_basic_message('Chartbeat is not properly configured, please refer to the documentation...', channel)

    if command.startswith(HELP_COMMAND):
        payload = [
            {
                "fallback": "AMP Validator by James Ives",
                "color": "#83c7ea",
                "pretext": "Feedback and Issues can be reported here: https://github.com/JamesIves/amp-validator-slack-service/issues",
                "author_name": "James Ives",
                "author_link": "https://jamesiv.es",
                "title": "AMP Validator",
                "title_link": "https://api.slack.com/",
                "text": "The following commands are available.",
                "fields": [
                    {
                        "title": "validate <url>",
                        "value": "Running the validate command followed by a valid url will test the page against the AMP validator.",
                        "short": "false"
                    },
                    {
                        "title": "chartbeat validate",
                        "value": "If Chartbeat is configured this command will validate the top performing pages according to Chartbeat.",
                        "short": "false"
                    },
                    {
                        "title": "chartbeat last",
                        "value": "Returns the results from the last time the chartbeat validator ran.",
                        "short": "false"
                    }
                ],
                "thumb_url": "http://i.imgur.com/0IXuhlZ.png",
                "footer": "https://github.com/JamesIves/amp-validator-slack-service",
                "footer_icon": "http://i.imgur.com/0IXuhlZ.png",
                "ts": int(time.time())
            }
        ]
        
        send_attachment_message(payload, channel)


def send_attachment_message(data, channel):
    """ Sends an attachment message using the Slack API. """
    ts = int(time.time())
    payload = data

    if 'valid' in data:
        print('found valid')
        if data['valid'] is True:
            # Sends a valid message payload
            payload = [
                {
                    "fallback": "Article passed AMP validation!",
                    "color": "#32CD32",
                    "author_name": "AMP Validator",
                    "author_link": "https://validator.ampproject.org/",
                    "author_icon": "http://i.imgur.com/1o63W1s.png",
                    "title": "No AMP Errors Found :beers:",
                    "title_link": "%s" % (data['article']),
                    "text": "The provided document came back with no validation errors. :tada:",
                    "footer": "https://github.com/JamesIves/amp-validator-slack-service",
                    "footer_icon": "http://i.imgur.com/0IXuhlZ.png",
                    "ts": ts
                }
            ]

        if data['valid'] is False:
            # Sends an invalid message payload
            payload = [
                {
                    "fallback": "AMP Error found on line %s for article %s - %s - %s" % (data['line'], data['article'], data['reason'], data['code']), 
                    "color": "#ff0000",
                    "author_name": "AMP Validator",
                    "author_link": "https://validator.ampproject.org/",
                    "author_icon": "http://i.imgur.com/THkGPdN.png",
                    "title": "%s on line %s! :x:" % (data['code'], data['line']),
                    "title_link": "%s" % (data['article']),
                    "text": "%s" % (data['reason']),
                    "footer": "https://github.com/JamesIves/amp-validator-slack-service",
                    "footer_icon": "http://i.imgur.com/0IXuhlZ.png",
                    "ts": ts
                }
            ]

    else:
        payload = data
    

    slack_client.api_call("chat.postMessage", channel=channel,
            attachments=payload, as_user=True)


def send_basic_message(message, channel):
    """ Sends a basic message with the Slack API """
    slack_client.api_call("chat.postMessage", channel=channel,
            text=message, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1

    if slack_client.rtm_connect():

        # Check if interval checking is setup, otherwise inform the user.
        if CHARTBEAT_ENDPOINT and CHARTBEAT_OUTPUT_CHANNEL and CHARTBEAT_INTERVAL_TIME:
            print('This is on')
            schedule.every(CHARTBEAT_INTERVAL_TIME).minutes.do(validate_chartbeat_schedule)

        else: 
            print('Chartbeat data cannot be found, please refer to the documentation.')

        print('Launch succesful, waiting for input...')

        while True:
            schedule.run_pending()
            time.sleep(1)
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")