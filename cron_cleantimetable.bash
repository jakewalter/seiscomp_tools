#!/bin/bash
#
ps -ef | grep 'load_timetable' | grep -v grep | awk '{print $2}' | xargs -r kill -9
