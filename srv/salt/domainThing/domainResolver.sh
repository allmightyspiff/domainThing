#! /bin/bash

PATH=/bin:/usr/bin:/sbin:/usr/sbin
DAEMON=/domainThing/domainResolver2.py
PIDFILE=/var/run/domainResolver.pid
HOME_DIR=/domainThing

test -x $DAEMON || exit 0

. /lib/lsb/init-functions

case "$1" in
  start)
     log_daemon_msg "Starting domainResolver"
     cd $HOME_DIR
     start_daemon -p $PIDFILE $DAEMON &
     log_end_msg $?
   ;;
  stop)
     log_daemon_msg "Stopping domainResolver"
     killproc -p $PIDFILE $DAEMON
     for pid in `ps x | grep domainResolver2 |grep -v grep |awk '{print $1}'`; 
        do 
            kill -9 $pid; 
        done      
     log_end_msg $?
   ;;
  force-reload|restart)
     $0 stop
     $0 start
   ;;
  status)
     cd $HOME_DIR
     tail -n 1 resolver.log && exit 0 || exit $?
   ;;
 *)
   echo "Usage: /etc/init.d/domainResolver {start|stop|restart|force-reload|status}"
   exit 1
  ;;
esac

exit 0