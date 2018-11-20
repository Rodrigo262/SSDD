#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import IceStorm
Ice.loadSlice('Example.ice')
import Example


KEY = 'IceStorm.TopicManager.Proxy'
TOPIC_NAME = 'ExampleTopic'


class Consumer(Example.Events):
    def __init__(self):
        self.statistics = {}
        
    def send(self, message, current=None):
        print("Event received: {0}".format(message))


class Subscriber(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        # Get topic manager
        topic_mgr_proxy = broker.propertyToProxy(KEY)
        if topic_mgr_proxy is None:
            print('Property {0} not set'.format(KEY))
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

        # Create subscriber
        servant = Consumer()
        adapter = broker.createObjectAdapter("SubscriberAdapter")
        subscriber = adapter.addWithUUID(servant)

        # Subscribe to topic
        qos = {}
        topic.subscribeAndGetPublisher(qos, subscriber)

        # Wait until end
        print ('Waiting events... {}'.format(subscriber))
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0


sys.exit(Subscriber().main(sys.argv))
