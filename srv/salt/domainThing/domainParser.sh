#! /bin/bash

PATH=/bin:/usr/bin:/sbin:/usr/sbin
DAEMON=/domainThing/domainParser.py
PIDFILE=/var/run/domainParser.pid
HOME_DIR=/domainThing

test -x $DAEMON || exit 0

. /lib/lsb/init-functions

case "$1" in
    start)
        log_daemon_msg "Starting $DAEMON"
        cd $HOME_DIR
        start_daemon -p $PIDFILE $DAEMON &
        log_end_msg $?
    ;;
    stop)
        log_daemon_msg "Stopping DAEMON"
        for pid in `ps x | grep domainParser.py |grep -v grep |awk '{print $1}'`; 
        do 
            kill -9 $pid; 
        done      
        log_end_msg $?
    ;;
    status)
        cd $HOME_DIR
        PROCS=`ps x | grep -c domainParser.py`
        if [ "$PROCS" -gt "1" ]
        then
            echo "[OK] $DAEMON is running";
            exit 0 
        else
            echo "[FAIL] $DAEMON isn't running";
            exit 1
        fi
    ;;
    *)
        echo "Usage: /etc/init.d/domainParser {start|stop|status}"
        exit 1
   ;;
esac

exit 0