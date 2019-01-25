import os
import time
import pickle
import obspy
watchdir = '/home/sysop/output'

try:
    with open('/home/sysop/bin/change.pkl') as f:  # Python 3: open(..., 'rb')
        last = pickle.load(f)
except:
    last = set(os.listdir(watchdir))
#last = set()
while True:
    cur = set(os.listdir(watchdir))
    added = cur-last
    removed = last-cur
    if added: print 'added', added
    #if removed: print 'removed', removed
    last = set(os.listdir(watchdir))
    for add in added:
	print add[:11]
	eventid = add[:11]
	strtweet = '/home/sysop/textfiles/'+eventid+'.txt'
	event = obspy.read_events('/home/sysop/output/'+eventid+'_update.xml')
	try:
	    eventmag = event[0].preferred_magnitude().mag
	    if eventmag > 4.0:
	   	time.sleep(90)
	    event = obspy.read_events('/home/sysop/output/'+eventid+'_update.xml')
            eventmag = event[0].preferred_magnitude().mag
	    if eventmag > 4.0:
                time.sleep(90)
	    try:
	        with open(strtweet, 'r') as myfile:
	    	    str1a = myfile.read()
	        os.system("/home/sysop/bin/twitter_update_tweepy.py '%s'" % str1a)
	    except IOError:
	        print "Failed to tweet for "+eventid
	        pass
	except AttributeError:
	    print "Event issue for "+eventid
	    pass

    with open('/home/sysop/bin/change.pkl', 'w') as f:  # Python 3: open(..., 'wb')
    	pickle.dump(last, f)
    time.sleep(240)



#os.system("/home/sysop/bin/twitter_update_tweepy.py '%s'" % str1a)
