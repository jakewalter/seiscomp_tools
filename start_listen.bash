#!/bin/bash
#source /home/seismo/snew/COM/SEISAN.bash
export SEISCOMP_ROOT=/home/sysop/seiscomp3
export PATH=/home/sysop/seiscomp3/bin:$PATH
export LD_LIBRARY_PATH=/home/sysop/seiscomp3/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/sysop/seiscomp3/lib/python:$PYTHONPATH
#export MANPATH=/home/seismo/seiscomp3/share/man:$MANPATH
# Setup SC2SEI
#export SC2SEI_TOP=/home/yourdir/SC2SEI
#export ARCHIVE_TOP=/home/seiscomp3-dir/seiscomp3/var/lib/archive
PATH=/home/sysop/bin:$PATH
cd /home/sysop/test
python seiscomp_processing.py >> listen.log 2>&1 &
#/usr/bin/nohup python seiscomp_processing.py &
