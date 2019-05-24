
import obspy
import sys

#print sys.argv[1]
ev = obspy.read_events(sys.argv[1])
#print ev
ev[0].preferred_magnitude().magnitude_type = str(sys.argv[2])
ev[0].preferred_magnitude().creation_info.agency_id = 'US'
ev[0].preferred_magnitude().mag = str(sys.argv[3])
#print ev[0].preferred_magnitude()
#ev[0].preferred_magnitude().mag = round(ev[0].preferred_magnitude().mag,2)
try:
    ev[0].preferred_magnitude().mag_errors.uncertainty = None
except:
    pass
#print round(ev[0].preferred_magnitude().mag,2) + '+/-' round(ev[0].preferred_magnitude().mag_errors.uncertainty,2)
ev.write(sys.argv[1], format="QUAKEML")
