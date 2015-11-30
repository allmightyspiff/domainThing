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
        for pid in `ps x | grep domainResolver2 |grep -v grep |awk '{print $1}'`; 
        do 
            kill -9 $pid; 
        done      
        log_end_msg $?
    ;;
    status)
        cd $HOME_DIR
        PROCS=`ps x | grep -c domainResolver2.py`
        if [ "$PROCS" -gt "1" ]
        then
            tail -n 1 resolver.log && exit 0 || exit $?
        else
            echo "$DAEMON isn't running";
            exit 1
        fi
    ;;
    *)
        echo "Usage: /etc/init.d/domainResolver {start|stop|status}"
        exit 1
   ;;
esac

exit 0