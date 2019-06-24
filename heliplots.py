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

LATITUDE = 35.48648649
# negative longitude indicates western hemisphere
LONGITUDE = -97.51380573

outdir = '/home/analyst/www/eq/heliplot'
#heli = os.path.join(outdir, day + '.pdf')


#usgs = Client("USGS")
t2 = UTCDateTime.now()
t1 = t2 - timedelta(days=2)

cat = Catalog()
cat2 = Catalog()

try:
    usgs = Client("USGS")
    cat += usgs.get_events(starttime=t1, endtime=t2, latitude=LATITUDE,
                           longitude=LONGITUDE, maxradius=2,minmagnitude=1.5)
except:
    pass


#try:
#    cat2 += usgs.get_events(starttime=t1, endtime=t2, minmagnitude=6)
#except:
#    pass

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

temp = (UTCDateTime(now)-86400)
temp1 = UTCDateTime(now)
start0 = UTCDateTime(datetime(temp.year,temp.month,temp.day,temp.hour,0,0))
os.system("scp keokuk-priv:~/scratch/temp.mseed /home/analyst/scratch/")
st = read('/home/analyst/scratch/temp.mseed')
st.merge()
cat3 = cat
for tr in st:
    net = str(tr.stats.network)
    sta = str(tr.stats.station)
    loc = str(tr.stats.location)
    ch = str(tr.stats.channel)
    startt = str(tr.stats.starttime)
    sr = str(tr.stats.sampling_rate)
    heli = os.path.join(outdir, sta + '.pdf')
    #tr.merge()
    if isinstance(tr.data, np.ma.masked_array):
        tr.data = tr.data.filled()
    tr.trim(start0,tr.stats.endtime)
    sbp = tr.filter('bandpass', freqmin=fminbp, freqmax=fmaxbp, zerophase=True)
    print(tr.stats.starttime)
    # make main and bandpass helicorders
    #st.plot(type='dayplot', title=net + '.' + sta + '.' + loc + '.' + ch + ' - ' + str(temp.year)+ '/'+str(temp.month)+ '/'+str(temp.day) + ' - rate: ' + sr + 'Hz - range: 0-25Hz', vertical_scaling_range=10e3, outfile=heli, color=['k'], time_offset=tz,size=(1000, 600))
    try:
        sbp.plot(type='dayplot', interval=60,title=net + '.' + sta + '.' + loc + '.' + ch + ' - ' + str(temp1.year)+ '/'+str(temp1.month)+ '/'+str(temp1.day) + ' ' + str(temp1.hour)+':'+str(temp1.minute)+' - Bandpass: 0.7-20Hz', vertical_scaling_range=None, outfile=heli, events=cat3, color=['k'],time_offset=tz,size=(1200, 800),number_of_ticks=7,one_tick_per_line=True)
	#sbp.plot(type='dayplot', interval=60, title=net + '.' + sta + '.' + loc + '.' + ch + ' - ' + str(temp.year)+ '/'+str(temp.month)+ '/'+str(temp.day) + ' - Bandpass: 0.7-20Hz', vertical_scaling_range=None, outfile=heli, events=cat3, color=['k'],time_offset=tz,size=(1000, 800),number_of_ticks=7,one_tick_per_line=True)
    except:
        pass
    #del st
    #del sbp
    #


#
#    
#    
#
##import datetime
#client = Client('IRIS')
##cat += iris.get_events(starttime=t1, endtime=t2, latitude=YOUR_LATITUDE,
##                           longitude=YOUR_LONGITUDE, maxradius=15)
#
#
#net = 'AM' # network. usually AM "amateur"
#sta = 'RAE8E' # station callsign. 5 uppercase alphanumeric characters beginning with R
#ch = 'SHZ' # channel. should be either SHZ or EHZ depending on the model
#loc = '00' # location. usually 00
#
#
#
## output locations and filenames
#
##spec = os.path.join(outdir, 'spec.png')
##specband = os.path.join(outdir, 'spec-band.png')
#
##mseedloc = '/opt/data/archive/' + str(yr) + '/' + net + '/' + sta + '/' + ch + '.D/' + net + '.' + sta + '.' + loc + '.' + ch + '.D.' + day
#
## read meta values from miniseed
##st = read(mseedloc)
#
#temp = (UTCDateTime(now)-86400)
#temp1 = UTCDateTime(now)
##yr1 = temp.strftime("%Y")
##month1 = temp.strftime("%m")
##day1 = temp.strftime("%d")
##hr1 = temp.strftime("%H")
##yr2 = temp1.strftime("%Y")
##month2 = temp1.strftime("%m")
##day2 = temp1.strftime("%d")
##hr2 = temp1.strftime("%H")
##os.system('echo "%s,%s,%s,%s,00,00,00 %s,%s,%s,%s,00,00,00 OK FNO * *" | capstool -H 10.27.192.71:18002 -o temp.mseed' % (yr1,month1,day1,hr1,yr2,month2,day2,hr2))
##
##st = read('temp.mseed')
#start = UTCDateTime(temp)
#start = UTCDateTime(datetime(temp.year,temp.month,temp.day,temp.hour,0,0))
#end = UTCDateTime(temp1)
#
#tr = client.get_waveforms(network='OK', station='FNO',
#                                 location='*', channel='HHZ',
#                                 starttime=start, endtime=end)
#ok_sta = client.get_stations(network='OK', channel='?H?',level='channel')
#for sta in ok_sta[0]:
#    print(sta)
#st = tr
#net = str(st[0].stats.network)
#sta = str(st[0].stats.station)
#loc = str(st[0].stats.location)
#ch = str(st[0].stats.channel)
#startt = str(st[0].stats.starttime)
#sr = str(st[0].stats.sampling_rate)
##
#sbp = st.copy() # copy for bandpass
#sbp = sbp.filter('bandpass', freqmin=fminbp, freqmax=fmaxbp, zerophase=True)
##spu = st.slice(starttime=short, endtime=now) # slice for main spectrogram
##sps = sbp.slice(starttime=short, endtime=now) # slice for bandpass spectrogram
#
#cat3 = cat2+cat
## make main and bandpass helicorders
##st.plot(type='dayplot', title=net + '.' + sta + '.' + loc + '.' + ch + ' - ' + str(temp.year)+ '/'+str(temp.month)+ '/'+str(temp.day) + ' - rate: ' + sr + 'Hz - range: 0-25Hz', vertical_scaling_range=10e3, outfile=heli, color=['k'], time_offset=tz,size=(1000, 600))
#sbp.plot(type='dayplot', title=net + '.' + sta + '.' + loc + '.' + ch + ' - ' + str(temp.year)+ '/'+str(temp.month)+ '/'+str(temp.day) + ' - rate: ' + sr + 'Hz - bandpass: 0.7-20Hz', vertical_scaling_range=3e3, outfile=heliband, events=cat3, color=['k'],time_offset=tz,size=(1000, 800))
##del st
##del sbp
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
