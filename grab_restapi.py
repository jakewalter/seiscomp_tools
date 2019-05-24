#!/usr/bin/env python
import urllib
import zipfile
import os
#import smtplib

# Import the email modules we'll need
#from email.message import EmailMessage
#import subprocess
#pen the plain text file whose name is in textfile for reading.
from twilio.rest import Client
import time
accountSID = 'xx'
authToken = 'xx'
#twilioCli = TwilioRestClient(accountSID, authToken)

myTwilioNumber = 'xx'
myCellPhone = 'xx'
#testfile = urllib.URLopener()
os.system("rm /home/analyst/www/staff/earthquake/earthquake.zip")

testfile = urllib.URLopener()
try:
    testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?mag=1&offset=24&format=shp", "/home/analyst/www/staff/earthquake/earthquake.zip")
#    os.system("wget -O earthquakes.zip 'https://ogsweb.ou.edu/api/earthquake?mag=1&offset=24&format=shp'")
    time.sleep(5)
    testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?mag=1&offset=168&format=shp", "/home/analyst/www/staff/earthquake/earthquake7.zip")
    time.sleep(5)
    testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?mag=1&offset=720&format=shp", "/home/analyst/www/staff/earthquake/earthquake30.zip")
    #testfile = urllib.URLopener()
    time.sleep(5)
    testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?offset=24&mag=1&format=csv", "/home/analyst/www/eq/catalog/past24hours/past24hours.csv")
    time.sleep(5)
    testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?offset=168&mag=1&format=csv", "/home/analyst/www/eq/catalog/past7days/past7days.csv")
    time.sleep(5)
    testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?offset=720&mag=1&format=csv", "/home/analyst/www/eq/catalog/past30days/past30days.csv")
except IOError:
#    pass
    twilioCli = Client(accountSID, authToken)
    message = twilioCli.messages.create(body='REST API issue', from_=myTwilioNumber, to=myCellPhone)
#os.system("scp analyst@keokuk-priv:~/earthquake*zip /home/analyst/www/staff/earthquake/")
os.system("rm /home/analyst/www/staff/earthquake/earthquake.geojson")
zip_ref = zipfile.ZipFile('/home/analyst/www/staff/earthquake/earthquake.zip', 'r')
zip_ref.extractall('/home/analyst/www/staff/earthquake/')
zip_ref.close()
#zip_ref1 = zipfile.ZipFile('/home/analyst/www/staff/earthquake/earthquake7.zip', 'r')
#zip_ref1.extractall('/home/analyst/www/staff/earthquake/')
#zip_ref1.close()
os.system("cp /home/analyst/www/staff/earthquake/earthquake.shp /home/analyst/www/eq/catalog/past24hours/past24hours.shp")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.dbf /home/analyst/www/eq/catalog/past24hours/past24hours.dbf")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.prj /home/analyst/www/eq/catalog/past24hours/past24hours.prj")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.shx /home/analyst/www/eq/catalog/past24hours/past24hours.shx")
os.system("ogr2ogr -f KML /home/analyst/www/eq/catalog/past24hours/past24hours.kml /home/analyst/www/eq/catalog/past24hours/past24hours.shp")
os.system("ogr2ogr -f GeoJSON -t_srs crs:84 /home/analyst/www/staff/earthquake/earthquake.geojson /home/analyst/www/staff/earthquake/earthquake.shp")
#os.system("ogr2ogr -f CSV /home/analyst/www/eq/catalog/past24hours/past24hours.csv /home/analyst/www/eq/catalog/past24hours/past24hours.shp")
#ogr2ogr -f KML output.kml input.shp
#os.system("echo 'eqfeed_callback(' > temp")
#os.system("echo ')' > temp2")
os.system("rm /home/analyst/www/staff/earthquake/earthquake.jsonp")
os.system("cat /home/analyst/www/staff/earthquake/temp /home/analyst/www/staff/earthquake/earthquake.geojson /home/analyst/www/staff/earthquake/temp2 > /home/analyst/www/staff/earthquake/earthquake.jsonp")


os.system("rm /home/analyst/www/staff/earthquake/earthquake.geojson")
zip_ref1 = zipfile.ZipFile('/home/analyst/www/staff/earthquake/earthquake7.zip', 'r')
zip_ref1.extractall('/home/analyst/www/staff/earthquake/')
zip_ref1.close()
os.system("cp /home/analyst/www/staff/earthquake/earthquake.shp /home/analyst/www/eq/catalog/past7days/past7days.shp")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.dbf /home/analyst/www/eq/catalog/past7days/past7days.dbf")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.prj /home/analyst/www/eq/catalog/past7days/past7days.prj")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.shx /home/analyst/www/eq/catalog/past7days/past7days.shx")
os.system("ogr2ogr -f KML /home/analyst/www/eq/catalog/past7days/past7days.kml /home/analyst/www/eq/catalog/past7days/past7days.shp")
os.system("ogr2ogr -f GeoJSON -t_srs crs:84 /home/analyst/www/staff/earthquake/earthquake.geojson /home/analyst/www/staff/earthquake/earthquake.shp")
#os.system("ogr2ogr -f CSV /home/analyst/www/eq/catalog/past7days/past7days.csv /home/analyst/www/eq/catalog/past7days/past7days.shp")
#os.system("echo 'eqfeed_callback(' > temp")
#os.system("echo ')' > temp2")
os.system("rm /home/analyst/www/staff/earthquake/earthquake7days.jsonp")
os.system("cat /home/analyst/www/staff/earthquake/temp /home/analyst/www/staff/earthquake/earthquake.geojson /home/analyst/www/staff/earthquake/temp2 > /home/analyst/www/staff/earthquake/earthquake7days.jsonp")

#os.system("rm /home/analyst/www/staff/earthquake/earthquake.geojson")
zip_ref1 = zipfile.ZipFile('/home/analyst/www/staff/earthquake/earthquake30.zip', 'r')
zip_ref1.extractall('/home/analyst/www/staff/earthquake/')
zip_ref1.close()
os.system("cp /home/analyst/www/staff/earthquake/earthquake.shp /home/analyst/www/eq/catalog/past30days/past30days.shp")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.dbf /home/analyst/www/eq/catalog/past30days/past30days.dbf")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.prj /home/analyst/www/eq/catalog/past30days/past30days.prj")
os.system("cp /home/analyst/www/staff/earthquake/earthquake.shx /home/analyst/www/eq/catalog/past30days/past30days.shx")
os.system("ogr2ogr -f KML /home/analyst/www/eq/catalog/past30days/past30days.kml /home/analyst/www/eq/catalog/past30days/past30days.shp")
#os.system("ogr2ogr -f CSV /home/analyst/www/eq/catalog/past30days/past30days.csv /home/analyst/www/eq/catalog/past30days/past30days.shp")
#filenames = [/home/analyst/www/staff/earthquake/temp /home/analyst/www/staff/earthquake/earthquake.geojson /home/analyst/www/staff/earthquake/temp2]
#with open('path/to/output/file', 'w') as outfile:
#    for fname in filenames:
#        with open(fname) as infile:
#            outfile.write(infile.read())


