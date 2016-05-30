#!/bin/bash

#startx &
PIDFILE=$HOME/tmp/.waze.pid

pushd /home/pi/data/waze/ >> /dev/null 2>&1

START=0
if [ -e "$PIDFILE" ]; then
    PID="$(cat $PIDFILE)"
    if ! ps -p $PID > /dev/null ; then
        # last process is not around
        echo "Clean up from last process [$PID]"
        rm $PIDFILE
        START=1
    else
        echo -n '.'
    fi
else
    START=1
fi

if [ "$(pidof waze_twitter)" ]; then
    START=0
fi



if [ $START -eq 1 ]; then
	sleep 10
	python waze_twitter.py >> 2>&1 &
	echo $! > $PIDFILE
	echo 'Running....'
fi




#!/bin/bash

# python3 waze_twitter.py -d ~/data/waze/ -q "waze,okcupid"
# python3 waze_twitter.py -d ~/data/waze/ -q okcupid


