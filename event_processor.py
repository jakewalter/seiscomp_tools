"""
Filename: event_processor.py
Purpose: Handle incoming events from seiscomp3.  Checks to
see if the event meets the criteria (listed below) to inserted
into the catalog.  If there is an event with same event id it
is deleted before the event is inserted.
Criteria to counted as an event:
    1. Analyst has classified it as an earthquake
        or outside of network interest. Automatically an
        event, no further checks.
    2. Event meets all of the following:
        a. Magnitude >= 2.0
        b. Associated phase count >= 10
        c. Mismatch score <= 0.75
Original Author: Bill Greenwood
Date: 20180331
Additions: Jake Walter
Date: 20181115
"""
###Requires lxml, decorator, sqlalchemy installed
from obspy import read_events
import psycopg2 as pgdb
import os
from twilio.rest import Client
import reverse_geocoder as rg
import datetime

CONNSTRING = ("dbname=earthquake host=xx "
              "user='xx' password='xx'")
accountSID = 'xx'
authToken = 'xx'
#twilioCli = TwilioRestClient(accountSID, authToken)

myTwilioNumber = '+1405xx'
myCellPhone = '+1405xx'

def textmyalert(message):
    twilioCli = Client(accountSID, authToken)
        #twilioCli.messages.create(body=message, from_=myTwilioNumber, to=myCellPhone)
    for name, number in NUMBERS.items():
        message = twilioCli.messages.create(to=number, from_=myTwilioNumber,body=message)
        #print message.sid
def isdst(utctime):
  begin={'2001':datetime.datetime(2001,4,1,8,0),
    '2002':datetime.datetime(2002,4,7,8,0),
    '2003':datetime.datetime(2003,4,6,8,0),
    '2004':datetime.datetime(2004,4,4,8,0),
    '2005':datetime.datetime(2005,4,3,8,0),
    '2006':datetime.datetime(2006,4,2,8,0),
    '2007':datetime.datetime(2007,3,11,8,0),
    '2008':datetime.datetime(2008,3,9,8,0),
    '2009':datetime.datetime(2009,3,8,8,0),
    '2010':datetime.datetime(2010,3,14,8,0),
    '2011':datetime.datetime(2011,3,13,8,0),
    '2012':datetime.datetime(2012,3,11,8,0),
    '2013':datetime.datetime(2013,3,10,8,0),
    '2014':datetime.datetime(2014,3,9,8,0),
    '2015':datetime.datetime(2015,3,8,8,0),
    '2016':datetime.datetime(2016,3,13,8,0),
    '2017':datetime.datetime(2017,3,12,8,0),
    '2018':datetime.datetime(2018,3,11,8,0),
    '2019':datetime.datetime(2019,3,10,8,0),
    '2020':datetime.datetime(2020,3,8,8,0)}
  end={'2001':datetime.datetime(2001,10,28,8,0),
    '2002':datetime.datetime(2002,10,27,7,0),
    '2003':datetime.datetime(2003,10,26,7,0),
    '2004':datetime.datetime(2004,10,31,7,0),
    '2005':datetime.datetime(2005,10,30,7,0),
    '2006':datetime.datetime(2006,10,29,7,0),
    '2007':datetime.datetime(2007,11,4,7,0),
    '2008':datetime.datetime(2008,11,2,7,0),
    '2009':datetime.datetime(2009,11,1,7,0),
    '2010':datetime.datetime(2010,11,7,7,0),
    '2011':datetime.datetime(2011,11,6,7,0),
    '2012':datetime.datetime(2012,11,4,7,0),
    '2013':datetime.datetime(2013,11,3,7,0),
    '2014':datetime.datetime(2014,11,2,7,0),
    '2015':datetime.datetime(2015,11,1,7,0),
    '2016':datetime.datetime(2016,11,6,7,0),
    '2017':datetime.datetime(2017,11,5,7,0),
    '2018':datetime.datetime(2018,11,4,7,0),
    '2019':datetime.datetime(2019,11,3,7,0),
    '2020':datetime.datetime(2020,11,1,7,0)}
  flag=False
  year="%i" % (utctime.year)
  if utctime >= begin[year] and utctime < end[year]:
    flag=True
  return flag






def localtime(utc_time):
    if isdst(utc_time):
       ltime= utc_time - datetime.timedelta(hours=5.0)
    else:
       ltime= utc_time - datetime.timedelta(hours=6.0)
    return ltime

def twitter_post(message1a,event_id):
    """ post earthquake to twitter"""
    #town,delta,azm=nearest_city(epicenter)
    #if isdst(r.origin_time):
    #    ltimestr="%s (CDT)" % (calc_localtime(r.origin_time))
    #else:
    #    ltimestr="%s (CST)" % (calc_localtime(r.origin_time))
    str1a = message1a
    #str="Magnitude %.1f at %s %.1f miles %s of %s; %.3f,%.3f,z=%.1fkm" % (r.preferred_magnitude()[0],ltimestr,delta,azm_desc(azm),town,r.latitude,r.longitude,r.depth)
    with open("/home/sysop/textfiles/"+event_id+".txt", "w") as tfile:
    	tfile.write(str1a)
    #os.system("/home/sysop/bin/twitter_update_tweepy.py '%s'" % str1a)
    print message1a
    return str
class EventProcessor(object):
    """ 
    Main class to process incoming events
    """
    MAGNITUDE_THRESHOLD = 1.5
    PHASE_COUNT_THRESHOLD = 10
    MISMATCH_THRESHOLD = 0.81
    REVIEWED_EVENTS = ['earthquake', 'outside of network interest']
    
    def __init__(self, logger):
        """
        Initilization function. Sets inital state.

        Arguemnts:
        @param {object} logger - Logger object.
        """
        self.logger = logger
        self.conn = None
        self.cursor = None
        self.event_id = None
        self.status = "Preliminary"
        self.magnitude = None
        self.magnitude_type = None
        self.mag_source = "OGS"
        
    def _connect_to_db(self):
        """
        Private method to connect to database.
        """
        try:
            self.conn = pgdb.connect(CONNSTRING)
            self.cursor = self.conn.cursor()
        except pgdb.Error as error:
            self.logger.exception(error)

    def _close_db_connection(self):
        """
        Private method to close conneciton to database.
        """
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except pgdb.Error as error:
            self.logger.exception(error)

    def _check_origin_and_mag(self, event):

        is_valid = True
        #Test for origin
        try:
            origin = event.preferred_origin() or event.origins[0]
        except IndexError:
            self.logger.error("Event with event id %s is missing "
                              "origin", self.event_id)
            origin = None
        #Test for origin
        try:
            magnitude = event.preferred_magnitude() or event.magnitudes[0]
        except IndexError:
            self.logger.error("Event with event id %s is missing "
                              "magnitude", self.event_id)
            magnitude = None
        #If there isn't an origin and a magnitude the
            #event can't be processed
        if origin is None or magnitude is None:
            is_valid = False
        return is_valid
         
    def process(self, xml):
        """
        Main process method. Contain the logic to determine
        whether or not to further process the event.
        """
        self.status = "Preliminary"
        self.magnitude = None
        self.magnitude_type = None
        self.mag_source = "OGS"

        try:
            events = read_events(xml)
        except Exception as error:
            self.logger.exception(error)
        
        self._connect_to_db()
        if self.conn is None:
            return
        
        for event in events:
            self.event_id = (event.resource_id.id).split("/")[-1]
            self.logger.debug("Processing event: %s", self.event_id)

            try:
                self._delete_event(self.event_id)
            except pgdb.Error as error:
		print error
    		print error.pgcode
    		print error.pgerror
    		print traceback.format_exc()
                self.logger.exception(error)
                self._close_db_connection()
                return

            #Test for origin and magnitude
            if not self._check_origin_and_mag(event):
                return
            magnitude = event.preferred_magnitude() or event.magnitudes[0]
            origin = event.preferred_origin() or event.origins[0]           
 
            try:
                event_type = event.event_type
		print event_type
            except AttributeError:
                event_type = None

            #This is an event the analyst has worked and said is not
                #an event
            if event_type == 'not existing':
                self.logger.info("Event %s has been deemed not real",
                                 self.event_id)
                return                

            
            #set the magnitude based on preferred mag or USGS comment
            self._set_magnitude(event, magnitude)
            #Set the process flag and event status
            process_event = False
            if event_type in self.REVIEWED_EVENTS:
                process_event = True
                self.status = "Reviewed"
            else:   
                process_event = self._test_origin(origin)
                self.status = "Preliminary"
                
            if process_event:
                try:
                    self._process_event(event, xml)
		    
		    event_id = (event.resource_id.id).split("/")[-1]
       	 	    origin = event.preferred_origin() or event.origins[0]
        	    magnitude = event.preferred_magnitude() or event.magnitudes[0]
                    
		    try:
            		    #result,county,state = self._get_state_and_county(origin["longitude"],
                            #                           origin["latitude"])
                        result,county,state = self._get_state_and_county(origin["longitude"],origin["latitude"])
                    	os.system('update.sh %s' % event_id)
                    	    #twilioCli = Client(accountSID, authToken)
                    	    #print origin.get('time')
                    	mylocaltime = localtime(origin.get('time'))
                   	message1=self.status+" M "+str(round(self.magnitude,1))+" earthquake in "+county+" County, "+state+" at "+mylocaltime.datetime.strftime('%H:%M:%S %m/%d')+" Oklahoma local time (UTC: "+origin.get('time').datetime.strftime('%H:%M:%S %m/%d')+")"
                    	message=self.status+" M "+str(round(self.magnitude,1))+" quake in "+county+" County, "+state+" at "+mylocaltime.datetime.strftime('%H:%M:%S %m/%d')+" Oklahoma local time (UTC: "+origin.get('time').datetime.strftime('%H:%M:%S %m/%d')+")"+" eventID "+event_id
                    	textmyalert(message)
                    	twitter_post(message1,event_id)
        	    except TypeError as error:
            		print "Not in AOI, so not added to messaging"
		   
		except pgdb.Error as error:
                    self.logger.exception(error)
                    self._close_db_connection()
                    return
            else:
                self.logger.info("event %s doesn't meet criteria.",
                                 self.event_id)
        self._close_db_connection()

    def _set_magnitude(self, event, magnitude):
        """
        Method to set the magnitude based on whether or
        not the analyst has added a comment.  If the
        analyst has added a USGS magnitude then the
        magnitude, magnitude type, and magnitude source
        are from the USGS.

        Arguments:
        @param {object} event - The event to check for comments.
        @param {object} magnitude - The magnitude to use if
            no comments related to USGS.
        """
        self.magnitude = float(magnitude.mag)
        self.magnitude_type = magnitude.magnitude_type
        self.magnitude_src = "OGS"
        comments = event.comments
        for comment in comments:
	    print comment.text
            if comment.text[:7] == "USGS Mw":
                comment = comment.text.split(" ")
                try:
                    self.magnitude = float(comment[2])
                except ValueError as error:
                    self.logger.warning("Magnitude is not valid: %s",
                                        comment[2])
                    continue
                
                self.magnitude_src = "USGS"
                self.magnitude_type = comment[1]
            #if comment.text[:7] == "USGS mbLg":
            #    comment = comment.text.split(" ")
            #    try:
            #        self.magnitude = float(comment[2])
            #    except ValueError as error:
            #        self.logger.warning("Magnitude is not valid: %s",
            #                            comment[2])
            #        continue
#
#                self.magnitude_src = "USGS"
#                self.magnitude_type = comment[1]

    def _test_origin(self, origin):
        """"
        Method to test whether or not to add the event
        to the database.

        Arguments:
        @param {object} origin - Origin object containing
            the necessary attributes to test for event.
        @return {bool} - If origin passes test True, otherwise
            False.
        """
        quality = origin.quality
        mag = self.magnitude  
        phase_cnt = quality.associated_phase_count 
        comments = origin.comments
        mismatch = None 
        
        for comment in comments:
            if "mismatchScore" in comment.resource_id.id:
                mismatch = float(comment.text)
        
        valid = True
        if mag < self.MAGNITUDE_THRESHOLD \
           or phase_cnt < self.PHASE_COUNT_THRESHOLD \
           or mismatch > self.MISMATCH_THRESHOLD:
            valid = False

        return valid
        
    def _delete_event(self, event_id):
        """
        Private method to delete event with given event_id
        from the database.

        Arguments:
        @param {str} event_id - Id of the event to remove.
        """
        sql = ("DELETE FROM earthquake_quake.quakes WHERE event_id=%s")
        values = (event_id, )
        self.logger.debug("Deleting event with id: %s", event_id)
        try:
            self.cursor.execute(sql, values)
        except pgdb.Error as error:
            raise pgdb.Error(error)    

#    def _get_state_and_county(self, lon, lat):
#        """
#        Function to get the State and County for the event.  Uses
#        the passed lat and lon to create a point and then check
#        to see if the point falls within the states and counties
#        in the database.
#
#        Arguments:
#        @param {float} lon - Longitude for the point
#        @param {float} lat - Latitude for the point
#        @return {list} - A list of length two. First position
#        is the county name and the second is the state name.
#        """
#        sql = ("SELECT counties.name as county, "
#               "states.name as state "
#               "FROM counties "
#               "INNER JOIN states ON counties.statefp = states.statefp "
#               "WHERE ST_Within("
#               "st_geomfromtext(%s, 4269),"
#               "counties.geom) LIMIT 1;"
#               )
#        
#        values = ("Point({} {})".format(lon, lat), )
#        try:
#            self.cursor.execute(sql, values)
#        except pgdb.Error as error:
#            raise pgdb.Error(error)
#
#        try:
#            result = self.cursor.fetchone()
#        except pgdb.Error as error:
#            raise pgdb.Error(error)
#        except Exception as error:
#            print error
#        if result is None:
#            raise TypeError("Not in AOI")
#        
#        return result
    def _get_state_and_county(self, lon, lat):
        try:
            #result = None
	    coordinates = (lat,lon)
	    #print coordinates
	    results = rg.search(coordinates)
	    try:
		county = results[0]['admin2'].split()[:1][0]
		state = results[0]['admin1']
	    except:
		state = None
		county = None
	    #state = results[0]['admin1']
	    if (lat>33 and lat <38 and lon>-103.5 and lon<-94):
	    	result = True
	    else:
		print "NOT AOI event"
		result = None
		raise TypeError("Not in AOI")
		#print "We are in the AOI"
	    #print result, Lat, Lon
        except pgdb.Error as error:
            raise pgdb.Error(error)
        except Exception as error:
            print error
        if result is None:
        #    print "Not in the AOI!!!!!!"
	    raise TypeError("Not in AOI")
       	    #print "We are NOT in the AOI" 
        return result,county,state
        
    def _process_event(self, event, xml):
        """
        Private method to process an event.  Handles getting
        all of the required fields from the event to place into
        database.

        Arguments:
        @param {object} - Event to process.
        @param {str} - Full path to xml file for the event.
        """
        event_id = (event.resource_id.id).split("/")[-1]
        origin = event.preferred_origin() or event.origins[0]
        magnitude = event.preferred_magnitude() or event.magnitudes[0]
        print event_id
        county = "null"
	state = "null"
        try:
            result,county,state = self._get_state_and_county(origin["longitude"],
                                                       origin["latitude"])
        except pgdb.Error as error:
            self.logger.exception(error)
            return
        except TypeError as error:
            self.logger.error("Lon %s, Lat: %s %s",
                              origin.get("longitude"), origin.get("latitude"),
                              error)
            return
            
        self.logger.info("Inserting event %s into database.", event_id)
        print county, state 
        sql = ("INSERT INTO earthquake_quake.quakes("
               "event_id, origintime, "
               "latitude, longitude, "
               "depth, err_lon, "
               "err_lat, "
               "err_depth, "
               "err_origintime, county, state, "
               "origin_src, "
               "prefmag, pmag_type, pmag_src, "
               "status, reafile, shape) "
               "VALUES ("
               "%s, %s,"
               "%s, %s, "
               "%s, %s, "
               "%s, "
               "%s, "
               "%s, %s, %s, "
               "%s, "
               "%s, %s, "
               "%s, "
               "%s, %s,"
               "st_geomfromtext(%s, 4269));")
	#print origin
	if origin.depth_errors['uncertainty'] == None:
	    origin.depth_errors['uncertainty'] = 0
        values = (
            event_id, origin.get('time').datetime,
            origin.get('latitude'), origin.get("longitude"),
            round(origin.get('depth') / 1000.0, 2), round(float(origin.longitude_errors['uncertainty']),2),
            round(float(origin.latitude_errors['uncertainty']),2),
            round(float(origin.depth_errors['uncertainty']/1000.0),2),
            origin.time_errors['uncertainty'], county, state,
            None, #origin_src
            round(self.magnitude, 1), self.magnitude_type,
            self.magnitude_src,
            self.status, xml,
            "Point({} {})".format(origin.get('longitude'),
                                  origin.get('latitude')))
 
        try:
            self.cursor.execute(sql, values)
	    #os.system('update.sh %s' % event_id)
	    #twilioCli = Client(accountSID, authToken)
            #mylocaltime = localtime(origin.get('time'))
	    #message1=self.status+" M "+str(round(self.magnitude,1))+" earthquake in "+county+" County, "+state+" at "+mylocaltime.datetime.strftime('%H:%M:%S %m/%d')+" Oklahoma local time (UTC: "+origin.get('time').datetime.strftime('%H:%M:%S %m/%d')+")"
	    #message=self.status+" M "+str(round(self.magnitude,1))+" quake in "+county+" County, "+state+" at "+mylocaltime.datetime.strftime('%H:%M:%S %m/%d')+" Oklahoma local time (UTC: "+origin.get('time').datetime.strftime('%H:%M:%S %m/%d')+")"+" eventID "+event_id
	    #twilioCli.messages.create(body=message, from_=myTwilioNumber, to=myCellPhone)
	    #textmyalert(message)
	    #twitter_post(message1)
        except pgdb.Error as error:
            raise pgdb.Error(error)
#	try:
#	    os.system('update.sh %s' % event_id)
#	except:
#	    pass
    

if __name__ == '__main__':
    """
    Just for testing purposes
    """
    import glob
    import ogs_logger

    logger = ogs_logger.set_logger("seiscomp_test.log", 20)

    event_processor = EventProcessor(logger)
    dirs = ["xml/2019/01/*ogs2019bdbd*.xml"]
    #dirs = ["scratch/*uzyo*"]
    #dirs = ["scratch/*xml"]
##    dirs = ["xml/2017/11/ogs2017wqql*.xml"]

    for directory in dirs:
        print directory
        for xml in glob.glob(directory):
            xml = xml.replace("\\", "/")
            if event_processor.process(xml) == 'stop':
                break
            
    print ".....Done"

