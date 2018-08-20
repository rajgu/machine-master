#!/bin/bash

size=$(tput cols)
if [ "$size" -lt "256" ]; then
	echo "Resolution too low, it need to be at least 256 cols"
	exit 1
fi

if [ -z "$1" ]; then
	./cron.sh 'make_the_m' &
fi

if [ "$1" == 'make_the_m' ]; then
	processess=$(pgrep 'cron.sh' | wc -l)
	if [ "$processess" -gt "2" ]; then
		echo "Process already running"
		exit 2
	fi
	while [ '1' == '1' ]; do
		./cron.sh 'make_the_magic' > /dev/null &
		sleep 900
	done
else
	if [ "$1" == 'make_the_magic' ]; then
		STP_LIST=$(./updater.py get_stp_list)
		COUNT=$(echo $STP_LIST | wc -w)
		SLEEP=$(expr 900 / $COUNT)
		for stp in $STP_LIST; do
			./updater.py $stp > /dev/null &
			sleep $SLEEP
		done
	fi
fi
