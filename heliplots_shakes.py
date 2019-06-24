#!/usr/bin/python

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from obspy import read
from obspy.core.utcdatetime import UTCDateTime
from datetime import datetime
import pytz
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.core.event.catalog import Catalog
from datetime import timedelta
from obspy import Stream
from obspy.clients.fdsn.mass_downloader import CircularDomain, Restrictions, MassDownloader

#import datetime
#client = Client('IRIS')
#cat += iris.get_events(starttime=t1, endtime=t2, latitude=YOUR_LATITUDE,
#                           longitude=YOUR_LONGITUDE, maxradius=15)
LATITUDE = 35.48648649
# negative longitude indicates western hemisphere
LONGITUDE = -97.51380573

t2 = UTCDateTime.now()
t1 = t2 - timedelta(days=1)

cat = Catalog()
cat2 = Catalog()

try:
    usgs = Client("USGS")
    cat += usgs.get_events(starttime=t1, endtime=t2, latitude=LATITUDE,
                           longitude=LONGITUDE, maxradius=2,minmagnitude=2)
except:
    pass


try:
    usgs = Client("USGS")
    cat2 += usgs.get_events(starttime=t1, endtime=t2, minmagnitude=7)
except:
    pass


now = UTCDateTime.now()
yr = now.year
day = now.strftime('%Y.%j')
skip = 60 * 5 # the number of seconds to skip back
short = now - (60*5) # datetime of analysis stary
tz = int(datetime.now(pytz.timezone('America/Chicago')).strftime('%z'))/100
fmin = 0.1 # min frequency
fmax = 25 # max freq (should not exceed 25)
fminbp = .7 # lower bandpass limit
fmaxbp = 20 # upper bandpass limit

# output locations and filenames
outdir = '/home/analyst/www/eq/shake_heliplot'
#heli = os.path.join(outdir, day + '.pdf')
#spec = os.path.join(outdir, 'spec.png')
#specband = os.path.join(outdir, 'spec-band.png')

#mseedloc = '/opt/data/archive/' + str(yr) + '/' + net + '/' + sta + '/' + ch + '.D/' + net + '.' + sta + '.' + loc + '.' + ch + '.D.' + day

# read meta values from miniseed
#st = read(mseedloc)

temp = (UTCDateTime(now)-86400)
temp1 = UTCDateTime(now)
#yr1 = temp.strftime("%Y")
#month1 = temp.strftime("%m")
#day1 = temp.strftime("%d")
#hr1 = temp.strftime("%H")
#yr2 = temp1.strftime("%Y")
#month2 = temp1.strftime("%m")
#day2 = temp1.strftime("%d")
#hr2 = temp1.strftime("%H")
#os.system('echo "%s,%s,%s,%s,00,00,00 %s,%s,%s,%s,00,00,00 OK FNO * *" | capstool -H 10.27.192.71:18002 -o temp.mseed' % (yr1,month1,day1,hr1,yr2,month2,day2,hr2))
#
#st = read('temp.mseed')
start = UTCDateTime(temp)
start = UTCDateTime(datetime(temp.year,temp.month,temp.day,temp.hour,0,0))
end = UTCDateTime(temp1)
#domain = CircularDomain(latitude=LATITUDE,longitude=LONGITUDE,minradius=0.0, maxradius=2)
#restrictions = Restrictions(starttime=temp, endtime=temp1, network="AM",reject_channels_with_gaps=True,minimum_interstation_distance_in_m=10E3)
##mdl = MassDownloader()
#mdl = MassDownloader(providers=['http://fdsnws.raspberryshakedata.com'])
#mdl.download(domain, restrictions, mseed_storage="/Users/jwalter/shake/waveforms",stationxml_storage="/Users/jwalter/shake/stations",threads_per_client=3,print_report=False)
client = Client('https://fdsnws.raspberryshakedata.com/')

ok_sta = client.get_stations(network='AM', channel='SHZ',latitude=LATITUDE,longitude=LONGITUDE,starttime=start, endtime=end,minradius=0.0, maxradius=2,level='channel')
cat3 = cat2+cat

for sta in ok_sta[0]:
    print(sta.code)
    try:
        st = client.get_waveforms(network='AM', station=sta.code,location='00', channel='SHZ', starttime=start, endtime=end)
        st.merge()
        for tr in st:
            if isinstance(tr.data, np.ma.masked_array):
                tr.data = tr.data.filled()
        #print('Downloaded')
        st.trim(start,end)
        sbp = st.filter('bandpass', freqmin=fminbp, freqmax=fmaxbp, zerophase=True)
        #spu = st.slice(starttime=short, endtime=now) # slice for main spectrogram
        #sps = sbp.slice(starttime=short, endtime=now) # slice for bandpass spectrogram
        
        heli = os.path.join(outdir, sta.code + '.pdf')
        net = str(sbp[0].stats.network)
        sta1 = str(sbp[0].stats.station)
        loc = str(sbp[0].stats.location)
        ch = str(sbp[0].stats.channel)
        startt = str(sbp[0].stats.starttime)
        sr = str(sbp[0].stats.sampling_rate)
        sbp.plot(type='dayplot', interval=60,title=net + '.' + sta1 + '.' + loc + '.' + ch + ' - ' + str(temp1.year)+ '/'+str(temp1.month)+ '/'+str(temp1.day) + ' ' + str(temp1.hour)+':'+str(temp1.minute)+' - Bandpass: 0.7-20Hz', vertical_scaling_range=None, outfile=heli, events=cat3, color=['k'],time_offset=tz,size=(1200, 800),number_of_ticks=7,one_tick_per_line=True)
        #sbp.plot(type='dayplot', interval=60,title=net + '.' + sta1 + '.' + loc + '.' + ch + ' - ' + str(temp1.year)+ '/'+str(temp1.month)+ '/'+str(temp1.day) + ' ' + str(temp1.hour)+':'+str(temp1.minute)+' - Bandpass: 0.7-20Hz', vertical_scaling_range=None, outfile=heli, events=cat3, color=['k'],time_offset=tz,size=(1000, 800),number_of_ticks=7,one_tick_per_line=True)
        #print(heli)
    except:
        pass
#
#inv = client.get_stations(starttime=starttime, endtime=endtime,network="AM", loc="00", channel="*Z",latitude=catdf['lat'][idx1],longitude=catdf['lon'][idx1],minradius=0.0, maxradius=maxrad,level="station")
##mdl.download(domain, restrictions, mseed_storage="/Users/jwalter/python/waveforms",stationxml_storage="/Users/jwalter/python/stations",threads_per_client=3,print_report=False)
#waveform = "/Users/jwalter/shake/waveforms"
#st = Stream()
#for (path, dirs, files) in os.walk(waveform):
#    for file in files:
#        tmpfile = os.path.join(path,file)
#        tmp = read(tmpfile)
##        inv = read_inventory('/Users/jwalter/python/stations/' + tmp[0].stats.network + '.' + tmp[0].stats.station + '.xml', format="STATIONXML")
##        sta_lat = inv.networks[0].stations[0].latitude
##        sta_lon = inv.networks[0].stations[0].longitude
##        #st3_1 = st.select(network=tr.stats.network,stati
##        tmp[0].stats.distance = gps2dist_azimuth(sta_lat,sta_lon, catdf['lat'][idx1],catdf['lon'][idx1])[0]
##        epi_dist1, az1, baz1 = gps2dist_azimuth(catdf['lat'][idx1], catdf['lon'][idx1], sta_lat, sta_lon)
##        tt0s,dtt0 = ray_trace_s(catdf.depth[idx1] / 1000,epi_dist1 / 1000) #check for vs model
##        tt0p,dtt0 = ray_trace_p(catdf.depth[idx1] / 1000,epi_dist1 / 1000)
##        st += tmp
#        sbp = tmp.copy() # copy for bandpass
#
#        
#        
#tr = client.get_waveforms(network='OK', station='FNO',
#                                 location='*', channel='HHZ',
#                                 starttime=start, endtime=end)
#ok_sta = client.get_stations(network='OK', channel='?H?',level='channel')
#for sta in ok_sta[0]:
#    print(sta)
#st = tr

#

#del sbp
#
## Plot the Spectrogram
## for reference-the old way of doing it:
## spec = sp.spectrogram(log=False, title='AM.RCB43 ' + str(sp[0].stats.starttime), outfile='/opt/data/obs/spec15.png', dbscale=False, cmap='viridis') #for reference
#
## filter (demean/constant)
#sp = spu.detrend(type='constant')
#ss = sps.detrend(type='constant')
#del spu
#del sps
#
### ---------------------------- ##
## make spectrogram figure 1
#sfig1 = plt.figure(figsize=(16,6), dpi=100)
#ax1 = sfig1.add_axes([0.068, 0.75, 0.85, 0.2]) #[left bottom width height]
#ax2 = sfig1.add_axes([0.068, 0.1, 0.85, 0.6], sharex=ax1)
#ax3 = sfig1.add_axes([0.931, 0.1, 0.03, 0.6])
#
## labels
#startt = str(sp[0].stats.starttime)
#endt = str(sp[0].stats.endtime)
#sfig1.suptitle(net + '.' + sta + '.' + loc + '.' + ch + ' - ' + startt + '--' + endt + ' - samplerate: ' + sr + 'Hz - range: 0-25Hz')
#ax1.set_ylabel('Counts')
#ax2.set_xlabel('Time [s]')
#ax2.set_ylabel('Frequency [Hz]')
#ax3.set_ylabel('Energy density [dimensionless]') # doesn't work
#
## make time vector
#t = np.arange(sp[0].stats.npts) / sp[0].stats.sampling_rate
#
## plot waveform (top subfigure)
#ax1.plot(t, sp[0].data, 'k')
#
## plot spectrogram (bottom subfigure)
#sfig1 = sp[0].spectrogram(show=False, axes=ax2, log=False, dbscale=False, cmap='viridis')
#mappable = ax2.images[0]
#plt.colorbar(mappable=mappable, cax=ax3)
#
#ax2.set_ylim(fmin, fmax)
#
#plt.savefig(spec)
#
#del sp
#
### ---------------------------- ##
## make spectrogram figure 2
#sfig2 = plt.figure(figsize=(16,4), dpi=100)
#ax1 = sfig2.add_axes([0.068, 0.600, 0.85, 0.3]) #[left bottom width height]
#ax2 = sfig2.add_axes([0.068, 0.115, 0.85, 0.4], sharex=ax1)
#ax3 = sfig2.add_axes([0.932, 0.115, 0.03, 0.4])
#
## labels
#sfig2.suptitle(net + '.' + sta + '.' + loc + '.' + ch + ' - ' + startt + ' - samplerate: ' + sr + 'Hz - bandpass: 0.7-2.0Hz')
#ax1.set_ylabel('Counts')
#ax2.set_xlabel('Time [s]')
#ax2.set_ylabel('Frequency [Hz]')
#ax3.set_ylabel('Energy density [dimensionless]') # doesn't work
#
## make time vector
#t = np.arange(ss[0].stats.npts) / ss[0].stats.sampling_rate
#
## plot waveform (top subfigure)
#ax1.plot(t, ss[0].data, 'k')
#
## plot spectrogram (bottom subfigure)
#sfig2 = ss[0].spectrogram(show=False, axes=ax2, log=False, dbscale=False, cmap='viridis')
#mappable = ax2.images[0]
#plt.colorbar(mappable=mappable, cax=ax3)
#
#ax2.set_ylim(fminbp, fmaxbp)
#
#plt.savefig(os.path.join(specband))
