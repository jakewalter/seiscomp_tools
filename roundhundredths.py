
import obspy
import sys

#print sys.argv[1]
ev = obspy.read_events(sys.argv[1])
ev[0].preferred_magnitude().mag = round(ev[0].preferred_magnitude().mag,2)
try:
    ev[0].preferred_magnitude().mag_errors.uncertainty = round(ev[0].preferred_magnitude().mag_errors.uncertainty,2)
except:
    pass
#print round(ev[0].preferred_magnitude().mag,2) + '+/-' round(ev[0].preferred_magnitude().mag_errors.uncertainty,2)
ev.write(sys.argv[1], format="QUAKEML")
