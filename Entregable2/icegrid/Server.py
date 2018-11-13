#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Printer.ice')
import Example

class PrinterI(Example.Printer):
   n = 0

   def write(self, message, current = None):
       print("{0}: {1}".format(self.n, message))
       sys.stdout.flush()
       self.n += 1
    

class Server(Ice.Application):
   def run(self, args):
      broker = self.communicator()
      servant = PrinterI()

      adapter = broker.createObjectAdapter("PrinterAdapter")
      proxy = adapter.add(servant,
                          broker.stringToIdentity("printer1"))

      print(proxy, flush=True)

      adapter.activate()
      self.shutdownOnInterrupt()
      broker.waitForShutdown()

      return 0


if __name__ == '__main__':
    app = Server()
    exit_status = app.main(sys.argv)
    sys.exit(exit_status)
