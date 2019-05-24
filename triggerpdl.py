import os
import time
import pickle
#import obspy
watchdir = '/home/sysop/outgoing_quakeml'
import time, os, stat

def file_age_in_seconds(pathname):
    return time.time() - os.stat(pathname)[stat.ST_MTIME]
#scp /home/sysop/output/$1_update.xml analyst@keokuk.ogs.ou.edu:/home/analyst/etc/quakeml/
#scp /home/sysop/output/$1_update.xml analyst@keokuk.ogs.ou.edu:/home/analyst/pdl/quakeml/
try:
    with open('/home/sysop/bin/triggerpdl.pkl') as f:  # Python 3: open(..., 'rb')
        history = pickle.load(f)
except:
    history = set(os.listdir(watchdir))
#last = set()
while True:
    try:
        with open('/home/sysop/bin/triggerpdl.pkl') as f:  # Python 3: open(..., 'rb')
            history = pickle.load(f)
    except:
        history = set(os.listdir(watchdir))
    cur = set(os.listdir(watchdir))
    added = cur-history
    #removed = last-cur
    if added: print 'added', added
    #if removed: print 'removed', removed
    #last = set(os.listdir(watchdir))
    for current in cur:
        print current[:11]
        eventid = current[:11]
        secs_since_write = file_age_in_seconds('/home/sysop/outgoing_quakeml/'+eventid+'_update.xml')
        print secs_since_write
	if (eventid+'_update.xml') not in history:
	    #os.system("mv /home/sysop/outgoing_quakeml/'%s'_update.xml /home/sysop/test/scratch/" %eventid)
	    os.system("scp /home/sysop/outgoing_quakeml/'%s'_update.xml analyst@keokuk.ogs.ou.edu:/home/analyst/pdl/quakeml/" %eventid)
	    os.system("scp /home/sysop/outgoing_quakeml/'%s'_update.xml sysop@10.27.192.63:/home/sysop/pdl/quakeml/" %eventid)
	    os.system("rm /home/sysop/outgoing_quakeml/'%s'_update.xml" %eventid) 
	    print "First write to PDL on new event"
	    history.add(eventid+'_update.xml')
	if secs_since_write > 120:
        #eventid = current[:11]
	#strtweet = '/home/sysop/textfiles/'+eventid+'.txt'
	#os.system("scp /home/sysop/output/'%s'_update.xml analyst@keokuk.ogs.ou.edu:/home/analyst/pdl/quakeml/" %eventid)
            #os.system("mv /home/sysop/outgoing_quakeml/'%s'_update.xml /home/sysop/test/scratch/" %eventid)
	#event = obspy.read_events('/home/sysop/output/'+eventid+'_update.xml')
            os.system("scp /home/sysop/outgoing_quakeml/'%s'_update.xml analyst@keokuk.ogs.ou.edu:/home/analyst/pdl/quakeml/" %eventid)
            os.system("scp /home/sysop/outgoing_quakeml/'%s'_update.xml sysop@10.27.192.63:/home/sysop/pdl/quakeml/" %eventid)
	    os.system("rm /home/sysop/outgoing_quakeml/'%s'_update.xml" %eventid)
	    print "older event moved to PDL"
	    history.add(eventid+'_update.xml')
	    #print history
	#try:
	#    eventmag = event[0].preferred_magnitude().mag
	#    if eventmag > 4.0:
	#   	time.sleep(90)
	#    event = obspy.read_events('/home/sysop/output/'+eventid+'_update.xml')
        #    eventmag = event[0].preferred_magnitude().mag
	#    if eventmag > 4.0:
        #        time.sleep(90)
	#    event = obspy.read_events('/home/sysop/output/'+eventid+'_update.xml')
        #    eventmag = event[0].preferred_magnitude().mag
	#    try:
	#        with open(strtweet, 'r') as myfile:
	#    	    str1a = myfile.read()
	#        os.system("/home/sysop/bin/twitter_update_tweepy.py '%s'" % str1a)
	#    except IOError:
	#        print "Failed to tweet for "+eventid
	#        pass
	#except AttributeError:
	#    print "Event issue for "+eventid
	#    pass

    	with open('/home/sysop/bin/triggerpdl.pkl', 'w') as f:  # Python 3: open(..., 'wb')
    	    pickle.dump(history, f)
    #time.sleep(5)
    #print 'heartbeat'
#else:
#    secs_since_write = file_age_in_seconds('/home/sysop/outgoing_quakeml/'+eventid+'_update.xml')
#    if secs_since_write > 120:
#	    #event = obspy.read_events('/home/sysop/output/'+eventid+'_update.xml'
    #    os.system("mv /home/sysop/outgoing_quakeml/'%s'_update.xml /home/sysop/test/scratch/" %eventid)
    #    print "Written after delay"
    #else:
    time.sleep(10)
    #print "Heartbeat"#	print "Wait 120 s because file too new"




#os.system("/home/sysop/bin/twitter_update_tweepy.py '%s'" % str1a)
