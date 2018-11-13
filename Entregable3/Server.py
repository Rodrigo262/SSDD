#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example

class PrinterI(Example.Printer):
   n = 0
   def __init__(self, name):
      self.name = name

   def write(self, message, current = None):
       print("{0},{1}: {2}".format(self.name, self.n, message))
       sys.stdout.flush()
       self.n += 1
    

class Server(Ice.Application):
   def run(self, args):
      broker = self.communicator()
      properties = broker.getProperties()
      
      adapter = broker.createObjectAdapter("PrinterAdapter")
      id = Ice.stringToIdentity(properties.getProperty("Identity"))
      servant = PrinterI(properties.getProperty("Ice.ProgramName"))      
      proxy = adapter.add(servant, id)
      adapter.activate()
      
      print(proxy, flush=True)

      self.shutdownOnInterrupt()
      broker.waitForShutdown()

      return 0


if __name__ == '__main__':
    app = Server()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)