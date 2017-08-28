#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

# Keep a running list of errors/passes
global_store = {
  'errors': 0,
  'passes': 0,
  'channel': None
}


def update_passes(passes):
  """ Updates the passes in the global store """
  global_store['passes'] = passes


def update_errors(errors):
  """ Updates the errors in the global store """
  global_store['errors'] = errors


def update_channel(channel):
  """ Updates the channel in the global store """
  global_store['channel'] = channel


def get_passes():
  """ Returns the passes in the global store """
  return global_store['passes']


def get_errors():
  """ Returns the errors in the global store """
  return global_store['errors']


def get_channel():
  """ Returns the channel in the global store """
  return global_store['channel']


def get_target_path(message):
  """ Splits a URL string from Slack """
  url = message.split(' ', 1)[1]
  url = url.split('|')[0]
  formatted_url = re.sub('\<|\>', '', url)

  return formatted_url
