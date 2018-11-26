#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import Ice
import IceStorm
Ice.loadSlice('Printer.ice')
import Example

class PrinterI(Example.Printer):
    def write(self, message, current=None):
        print("event received: {0}".format(message))
        sys.stdout.flush()

class StatisticsI(Example.Statistics):
    def __init__(self):
        self.statistics = {}

    def notify(self, printerId, current=None):
        print("notification from {0}".format(printerId))

        if printerId in self.statistics:
            self.statistics[printerId] += 1
        else:
            self.statistics[printerId] = 1
        print(self.statistics)
        sys.stdout.flush()

class Subscriber(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'

        proxy = self.communicator().propertyToProxy(key)

        if proxy is None:
            print("property {0} not set".format(key))
            return None
        print("using icestorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        topic_mgr = self.get_topic_manager() #proxy to topic

        if not topic_mgr:
            print(': invalid proxy')
            return 2

        ic = self.communicator()

        servant = StatisticsI()

        adapter = ic.createObjectAdapter("StatisticsAdapter")

        subscriber = adapter.addWithUUID(servant)

        topic_name = "PrinterTopic"
        qos = {}
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        print('waiting events... {}'.format(subscriber))

        adapter.activate()

        self.shutdownOnInterrupt()

        ic.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0
sys.exit(Subscriber().main(sys.argv))
