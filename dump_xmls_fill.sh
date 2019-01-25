#!/bin/sh
for i in `scevtls -d mysql://sysop:XXX@localhost/seiscomp3 --modified-after "2018-12-15 00:00:00"`;
do
	scxmldump -d mysql://sysop:XXXX@localhost/seiscomp3 -E $i -PAMf -o $i.xml
done
