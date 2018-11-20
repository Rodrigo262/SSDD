#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import IceStorm
Ice.loadSlice('Example.ice')
import Example


KEY = 'IceStorm.TopicManager.Proxy'
TOPIC_NAME = 'ExampleTopic'


class Publisher(Ice.Application):

   def run(self, args):
      broker = self.communicator()

      # Get topic manager
      topic_mgr_proxy = self.communicator().propertyToProxy(KEY)
      if topic_mgr_proxy is None:
         print("property {0} not set".format(KEY))
         return 1
      topic_mgr = IceStorm.TopicManagerPrx.checkedCast(topic_mgr_proxy)
      if not topic_mgr:
         print(': invalid proxy')
         return 2

      # Get topic
      try:
         topic = topic_mgr.retrieve(TOPIC_NAME)
      except IceStorm.NoSuchTopic:
         topic = topic_mgr.create(TOPIC_NAME)
         
      publisher = Example.EventsPrx.uncheckedCast(topic.getPublisher())

      # Shot events
      for event_no in range(10):
         print('Sending event #%s' % event_no)
         publisher.send('Event #%s' % event_no)

      # Bye
      return 0


if __name__ == '__main__':
    app = Publisher()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)
