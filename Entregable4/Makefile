all:

clean:
	$(RM) *~
	$(RM) -r db

start:  icebox.config icestorm.config
	@if ! [ -d db ]; then mkdir db; fi
	icebox --Ice.Config=icebox.config &
	sleep 3
	icestormadmin --Ice.Config=icestorm.config -e "create PrinterTopic"

stop: icestorm.config
	icestormadmin --Ice.Config=icestorm.config -e "destroy PrinterTopic"
	killall icebox

run-publisher:  icestorm.config
	./Server.py --Ice.Config=server.config

run-subscriber: icestorm.config
	./Statistics.py --Ice.Config=statistics.config

shutdown_systemctl:
	sudo systemctl stop icegridregistry
	sudo systemctl stop icegridnode
