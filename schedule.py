#!/usr/bin/python
# -*- coding: utf-8 -*-
from validate import getArticles, confirm
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import logging

# Scheduler
sched = BlockingScheduler()

# Logging
logging.basicConfig()

# Schedule Settings
@sched.scheduled_job('interval', minutes=60)
def timed_job():
    """Sets up the schedule to run every x minutes"""
    print 'Scheduled task has started.'
    getArticles()
    confirm()


# Begin Schedule
print 'Application is now scheduled'
sched.start()
