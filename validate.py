#!/usr/bin/python
# -*- coding: utf-8 -*-
from settings import SLACK_WEBHOOK_PATH
from settings import ARTICLE_LIST_PATH
import sys
import requests
import json
import slackweb

# Slack Webhook URL: This is found in the Slack team settings
slack = slackweb.Slack(url=SLACK_WEBHOOK_PATH)

# Error/Pass counts
errors = 0
passes = 0

def passed():
    """Incriments the passes counter if an article passes validation"""
    global passes
    passes = passes + 1


def failed(article):
    """If an article fails validation send a payload to Slack with the information"""
    global errors
    global time
    errors = errors + 1
    article_source = article['source']
    article_errors = article['errors']

    # Loops over all errors in the object
    for error in article_errors:
        reason = error['error']
        line = str(error['line'])
        code = error['code']

        if code != 'WARNING_TAG_REQUIRED_BY_MISSING':
            attachments = []
            attachment = {"fallback": "AMP Error found on line %s for article %s - %s - %s" % (line, article_source, reason, code), "title": "AMP Error Found: %s :x:" % (code), "title_link": "%s" % (article_source), "color": "#ff0000", "pretext": "An AMP error has been located on line %s. This error is causing the AMP document to not validate. If you're unsure how to resolve this error please refer to a developer. The next test will run in one hour." % (line), "text": "%s" % (reason), "footer": "News Organization", "footer_icon": "https://www.ampproject.org/static/img/amp_favicon.png?v=3"}
            attachments.append(attachment)
            slack.notify(attachments=attachments)

    print 'The following article object failed validation --  %s' % article


def validate(article):
    """Sends each article to the Cloudflare AMP validator API"""
    path = 'https://amp.cloudflare.com/q/%s' % article
    request = requests.get(path)
    document = request.json()

    # Fires pass/fail depending on the response from the API
    if document['valid'] == True:
        passed()

    if document['valid'] == False:
        failed(document)


def getArticles():
    """Gets a list of articles from the most-read endpoint"""

    # Makes sure that requests is able to get data and if not throw an exception
    try:
        request = requests.get(ARTICLE_LIST_PATH)
        request.raise_for_status()

    except requests.exceptions.RequestException as error:
        attachments = []
        attachment = {"fallback": "Unexpected Error Occured", "title": "Something serious went wrong. The validator was unable to reach the Chartbeat service and therefore could not check AMP validation. Alerting the @developers", "color": "#ffff00", "text": "%s" % (error), "footer": "News Organization", "footer_icon": "https://www.ampproject.org/static/img/amp_favicon.png?v=3"}
        attachments.append(attachment)
        slack.notify(attachments=attachments)
        print error
        sys.exit(1)

    # If no status error was found assume it was a 200
    # REPLACE: Modify the 'content_elements' label to match the array which contains your list of top articles
    request_json = request.json()
    for article in request_json['content_elements']:
        canonical_url = article['canonical_url']
        # REPLACE: Use %s to build a template for your AMP URL's. (This builds the path before it gets given to Cloudflare)
        amp_url = 'example.com%s?outputType=amp-type' % canonical_url
        validate(amp_url)


def confirm():
    """If there are no AMP errors found alert the Slack channel and remind them that the next test will run in an hour (Based on schedule)"""
    global errors
    global passes
    articles = str(passes)

    if errors == 0:
        attachments = []
        attachment = {"fallback": "The validator tested the top %s articles and found no errors. The next test will run in one hour." % (articles), "title": "No AMP Errors Found :beers:", "color": "#32CD32", "text": "The AMP validator tested against the top %s articles according to Chartbeat and found no errors. The next test will run in one hour." % (articles), "footer": "News Organization", "footer_icon": "https://www.ampproject.org/static/img/amp_favicon.png?v=3"}
        attachments.append(attachment)
        slack.notify(attachments=attachments)
        print 'All articles validated succesfully'

    # If a large amount of errors are found send an alert to the developer team
    if errors >= 4:
        attachments = []
        attachment = {"fallback": "The validator has detected a large amount of errors", "title": "The validator has detected a large amount of AMP errors!", "color": "#ffa500", "pretext": "@developers", "text": "Due to the large amount of errors detected the developer team has been alerted. The next test will run in one hour.", "footer": "News Organization", "footer_icon": "https://www.ampproject.org/static/img/amp_favicon.png?v=3"}
        attachments.append(attachment)
        slack.notify(attachments=attachments)
        print 'Large amount of AMP errors detected'


# Init Application
getArticles()
confirm()
