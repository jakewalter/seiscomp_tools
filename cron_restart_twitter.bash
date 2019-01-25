#!/bin/bash
#
MAILTO=""
PROCESS='changes.py'
if ps ax | grep -v grep | grep $PROCESS > /dev/null
then
echo "Twitter listener running, EXIT"
exit
else
echo "$PROCESS is not running"
echo "start the process"
echo "Start $PROCESS !"
#echo "put in the start command here"
/home/sysop/bin/start_changes.bash &
fi
