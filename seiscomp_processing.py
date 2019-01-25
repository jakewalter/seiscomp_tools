#!/bin/env python
"""
Filename: seiscomp_processing.py
Purpose: Listen to the SeisComp3 event queue for events and
process as they come in.
NOTE: Code adapted from code on the SeisComp3 website.
Original Author: Bill Greenwood
Date: 20180331
Changes: Jake Walter
Date: 20181101
Further changes needed
"""
import datetime
import os
import subprocess
import sys
import traceback

from obspy import read_events
sys.path.append("/home/sysop/seiscomp3/lib/python/")
sys.path.append("/home/sysop/seiscomp3/lib/")
import seiscomp3.Client

sys.path.append("/home/sysop/test")
import event_processor
import ogs_logger
import time

LOG_FILE = "/home/sysop/test/seiscomp_test.log"
XML_COMMAND = ("scxmldump -d mysql://sysop:sysop@localhost/seiscomp3 -E {0} "
               "-PAMf -o {1}")

XML_ROOT_DIRECTORY = "/home/sysop/test/xml"
FILENAME = "{0}/{1}.xml"

class EventListener(seiscomp3.Client.Application):

    def __init__(self):
        """
        Initilization function. Sets inital state.
        """
        seiscomp3.Client.Application.__init__(self, len(sys.argv), sys.argv)
        self.logger = ogs_logger.set_logger(LOG_FILE, 10)
        self.setMessagingEnabled(True)
        self.setDatabaseEnabled(True, True)
        self.setPrimaryMessagingGroup(
            seiscomp3.Communication.Protocol.LISTENER_GROUP)
        self.addMessagingSubscription("EVENT")
        self.setMessagingUsername("")
        self.event_processor = event_processor.EventProcessor(self.logger)

    def process(self, event):
        """
        Main method to handle incomiing events.

        Arguemnts:
        @param {object} event - SeisComp3 event object.
        """
        now = datetime.datetime.utcnow()
        ts = now.strftime("%Y%m%d_%H%M%S")
        folder = now.strftime("{}/%Y/%m".format(XML_ROOT_DIRECTORY))
        try:
            if not os.path.isdir(folder):
                os.makedirs(folder)
        except os.error as error:
            info = traceback.format_exception(*sys.exc_info())
            for i in info:
                self.logger.error(i)
            return
        
        event_id = event.publicID()
        filename = FILENAME.format(folder, event_id)
        command = XML_COMMAND.format(event_id, filename)
        try:
            result = subprocess.call(command.split(" "))
        except subprocess.CalledProcessError as error:
            self.logger.exception(error)
            return

        if result != 0:
            self.logger.error("Calling command '%s' returned non-zero code %s",
                              command, result)
            return
	
	time.sleep(20)
        self.event_processor.process(filename)

    #The method name is not convention, however, it can't
    #be changed because it is part of seiscomp3.Client.Application
    def updateObject(self, parentID, object):
        # called if an updated object is received
        event = seiscomp3.DataModel.Event.Cast(object)
        if event:
            #print "received update for event %s" % event.publicID()
            self.logger.debug("received update for event %s", event.publicID())
            self.process(event)

    #The method name is not convention, however, it can't
    #be changed because it is part of seiscomp3.Client.Application
    def addObject(self, parentID, object):
        # called if a new object is received
        event = seiscomp3.DataModel.Event.Cast(object)
        if event:
            #print "received new event %s" % event.publicID()
            self.logger.debug("received new event %s", event.publicID())
            self.process(event)

    def run(self):
        self.logger.debug("EventListener started...")
        return seiscomp3.Client.Application.run(self)

app = EventListener()
sys.exit(app())
