shutdown_systemctl:
	sudo systemctl stop icegridregistry
	sudo systemctl stop icegridnode


node1:
	mkdir -p /tmp/db/node1
	mkdir -p /tmp/db/registry
	icegridnode --Ice.Config=node1.config

node2:
	mkdir -p /tmp/db/node2
	icegridnode --Ice.Config=node2.config

copy_binaries:
	mkdir -p /tmp/Printer
	cp Server.py /tmp/Printer
	cp Server-UUID.py /tmp/Printer
	cp Client.py /tmp/Printer
	cp Printer.ice /tmp/Printer
	icepatch2calc /tmp/Printer

