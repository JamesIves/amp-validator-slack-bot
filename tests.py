#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from constants import *
from util import *

class BaseTest(unittest.TestCase):
  def test_get_errors(self):
    # It should return an int with the current error count
    self.assertEqual(get_errors(), 0)

  def test_get_passes(self):
    # It should return an int with the current pass count
    self.assertEqual(get_passes(), 0)

  def test_update_channel(self):
    # It should return a string with the current channel
    update_channel('#dev-channel')
    self.assertEqual(get_channel(), '#dev-channel')

  def test_update_errors(self):
    # It should update the error count and return
    # an int with the updated count
    update_errors(5)
    self.assertEqual(get_errors(), 5)

  def test_update_passes(self):
    # It should update the pass count and return
    # an int with the updated count
    update_passes(5)
    self.assertEqual(get_passes(), 5)

  def test_target_path(self):
    # It should return the second space seperated word
    # and strip out the | and everything after it
    # used by Slack
    self.assertEqual(get_target_path('validate https://jamesiv.es/|https://jamesiv.es'),
     'https://jamesiv.es/')
  

if __name__ == '__main__':
    unittest.main()