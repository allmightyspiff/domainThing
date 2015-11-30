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
     start_daemon -p $PIDFILE $DAEMON
     log_end_msg $?
   ;;
  stop)
     log_daemon_msg "Stopping domainResolver"
     killproc -p $PIDFILE $DAEMON
     PID=`ps x |grep feed | head -1 | awk '{print $1}'`
     kill -9 $PID       
     log_end_msg $?
   ;;
  force-reload|restart)
     $0 stop
     $0 start
   ;;
  status)
     status_of_proc -p $PIDFILE $DAEMON atd && exit 0 || exit $?
   ;;
 *)
   echo "Usage: /etc/init.d/domainResolver {start|stop|restart|force-reload|status}"
   exit 1
  ;;
esac

exit 0