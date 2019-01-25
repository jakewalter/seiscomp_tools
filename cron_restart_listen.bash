#!/bin/bash
#
MAILTO=""
PROCESS='seiscomp_processing.py'
if ps ax | grep -v grep | grep $PROCESS > /dev/null
then
echo "Seiscomp Listener running, EXIT"
exit
else
echo "$PROCESS is not running"
echo "start the process"
echo "Start $PROCESS !"
#echo "put in the start command here"
/home/sysop/bin/start_listen.bash &
fi
