import requests
import re
from urllib import urlopen
from lxml import etree
from constants import CHARTBEAT_ENDPOINT, CHARTBEAT_OUTPUT_CHANNEL
from util import *
from app import send_attachment_message, send_basic_message


def validate(article):
    """Sends each article to the Cloudflare AMP validator API"""
    path = 'https://amp.cloudflare.com/q/%s' % article
    
    try:
      request = requests.get(path)
      request.raise_for_status()
    except requests.exceptions.RequestException as error:
      return 'error'

    document = request.json()

    # Fires pass/fail depending on the response from the API
    if document['valid'] is True:
      return {
        'article': document['source'],
        'valid': document['valid'],
        'message': 'Article Passed Validation',
      }

    if document['valid'] is False:
      for error in document['errors']:
          reason = error['error']
          line = str(error['line'])
          code = error['code']
          
      return {
        'article': document['source'],
        'valid': document['valid'],
        'reason': reason,
        'line': line,
        'code': code,
        'message': 'Article Failed Validation',
      }


def get_amp_path(url):
  """
    Attempts to read the `amphtml` meta tag in a html document to get
    the path to a valid amp document. If the document is already an amp
    document it passes through to the validate function.
  """

  # Append http:// to each request to make sure it can be read
  if 'https://' not in url and 'http://' not in url:
    url = 'http://' + url

  try:
    document = urlopen(url).read().decode('utf-8')
  except IOError:
    return 'invalid'

  tree = etree.HTML(document)
  html_attributes = tree.attrib

  if 'amp' in html_attributes.keys():
    # If amp is in the html attributes assume it's an AMP document
    path = url

  else: 
    # Otherwise read the link tag and return the amphtml attribute
    try:
      path = tree.xpath("//link[@rel='amphtml']")[0].get('href')
    except IndexError:
      return 'notfound'

  # Clean the string so it can be passed to the validator
  amp_path = re.sub('http?:\/\/|https?:\/\/|www\.', '', path)

  return amp_path


def validate_chartbeat_articles():
    """
      Validates the top articles provided from the
      Chartbeat API. Requires the Chartbeat endpoint
      to be populated in the constants file.
    """
    validated_articles = []

    try:
      request = requests.get(CHARTBEAT_ENDPOINT)
      request.raise_for_status()

    except requests.exceptions.RequestException as error:
      send_basic_message('There was an issue reaching the Chartbeat service: ```%s```' % (error), global_store['channel'])
      return 'error'
    
    response = request.json()
    
    for page in response['pages']:
      page_path = page['path']
      amp_path = get_amp_path(page_path)

      if amp_path != 'notfound' and amp_path != 'invalid':
        validated_article = validate(amp_path)
        validated_articles.append(validated_article)
  
    return total_articles(validated_articles)


def total_articles(validated_articles):
    passes = 0
    errors = 0

    # Tally each pass, only post a message if it's a failure.
    for article in validated_articles:
        if article['valid'] is True:
            passes = passes + 1

        if article['valid'] is False:
            errors = errors + 1
            send_attachment_message(article, global_store['channel'])
    
    update_passes(passes)
    update_errors(errors)

    total = {
      'errors': errors,
      'passes': passes
    }
    
    return total


def validate_chartbeat_schedule():
  """
    Scheduler task for Chartbeat testing
    if the configuration is setup correctly
  """
  if CHARTBEAT_OUTPUT_CHANNEL:
    update_channel(CHARTBEAT_OUTPUT_CHANNEL)
    validate_chartbeat_articles()

  return
