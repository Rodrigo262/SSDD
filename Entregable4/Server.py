#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import Ice, IceStorm
Ice.loadSlice('Printer.ice')
import Example

class PrinterI(Example.Printer):
   n = 0
   def __init__(self, name, pstatistics):
      self.name = name
      self.statistics = pstatistics

   def write(self, message, current = None):

       print("{0}, {1}: {2}".format(self.name, self.n, message))

       sys.stdout.flush()

       self.n += 1
       
       self.statistics.notify(self.name)

class Server(Ice.Application):
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'

        proxy = self.communicator().propertyToProxy(key)

        if proxy is None:

            print("property {0} not set".format(key))

            return None
        print("using icestorm in: '%s'" % key)

        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, args):
        topic_mgr = self.get_topic_manager() #proxy to topic
        if not topic_mgr:
            print(': invalid proxy')
            return 2
        topic_name = "PrinterTopic"
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        publisher = topic.getPublisher()
        statistics = Example.StatisticsPrx.uncheckedCast(publisher)

        ic = self.communicator()

        properties = ic.getProperties()

        adapter = ic.createObjectAdapter("PrinterAdapter")

        servant = PrinterI(properties.getProperty("Ice.ProgramName"), statistics)

        proxy = adapter.add(servant, ic.stringToIdentity("Printer1"))

        adapter.activate()

        print(proxy, flush=True)

        self.shutdownOnInterrupt()

        ic.waitForShutdown()
        return 0

if __name__ == '__main__':
    app = Server()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)

