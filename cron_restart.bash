#!/bin/bash
#
MAILTO=""
PROCESS='seiscomp_processing.py'
if ps ax | grep -v grep | grep $PROCESS > /dev/null
then
echo "SC2SEI running, EXIT"
exit
else
echo "$PROCESS is not running"
echo "start the process"
echo "Start $PROCESS !"
#echo "put in the start command here"
/home/sysop/test/SC2SEI/par/start_sc2sei.bash &
fi
