#!/bin/bash

basedir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
seiscomp_root=/home/seiscomp/seiscomp3
d=`date -u +%Y-%m-%dT%H:%M:%S.%6NZ`
epoch=`date -u --date=$d +%s.%6N`

scxmldump -d mysql://sysop:sysop@localhost/seiscomp3 -E $1 -PMAfp |  xsltproc  $SEISCOMP_ROOT/share/xml/0.11/sc3ml_0.11__quakeml_1.2.xsl - | xsltproc --stringparam current-date $d --stringparam epoch $epoch  /home/sysop/bin/xsl/anss.xsl - | xsltproc /home/sysop/bin/xsl/delete.xsl - > /home/sysop/output/$1_delete.xml

#sysop@10.27.192.63
scp /home/sysop/output/$1_delete.xml sysop@10.27.192.63:/home/sysop/pdl/quakeml/
scp /home/sysop/output/$1_delete.xml analyst@keokuk.ogs.ou.edu:/home/analyst/pdl/quakeml/
