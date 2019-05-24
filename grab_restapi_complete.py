#!/usr/bin/env python
import urllib
import zipfile
import os
#import smtplib

# Import the email modules we'll need
#from email.message import EmailMessage
#import subprocess
#pen the plain text file whose name is in textfile for reading.
#from twilio.rest import Client
import time
testfile = urllib.URLopener()
os.system("rm /home/analyst/www/staff/earthquake/complete.csv")
#https://ogsweb.ou.edu/api/earthquake?start=188201010000&end=201812312359&mag=0&format=csv
testfile = urllib.URLopener()
testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?start=201901010000&end=202001010000&mag=1&format=shp", "/home/analyst/scratch/earthquake.zip")
zip_ref = zipfile.ZipFile('/home/analyst/scratch/earthquake.zip', 'r')
zip_ref.extractall('/home/analyst/scratch/earthquake/')
zip_ref.close()
os.system("cp /home/analyst/scratch/earthquake/earthquake.shp /home/analyst/www/eq/catalog/2019/2019.shp")
os.system("cp /home/analyst/scratch/earthquake/earthquake.dbf /home/analyst/www/eq/catalog/2019/2019.dbf")
os.system("cp /home/analyst/scratch/earthquake/earthquake.prj /home/analyst/www/eq/catalog/2019/2019.prj")
os.system("cp /home/analyst/scratch/earthquake/earthquake.shx /home/analyst/www/eq/catalog/2019/2019.shx")
os.system("ogr2ogr -f KML /home/analyst/www/eq/catalog/2019/2019.kml /home/analyst/www/eq/catalog/2019/2019.shp")
time.sleep(5)
testfile = urllib.URLopener()
testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?start=201901010000&end=202001010000&mag=1&format=csv", "/home/analyst/www/eq/catalog/2019/2019.csv")


time.sleep(5)
testfile = urllib.URLopener()
testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?start=188201010000&end=202012312359&mag=0&format=shp", "/home/analyst/scratch/earthquake.zip")
zip_ref = zipfile.ZipFile('/home/analyst/scratch/earthquake.zip', 'r')
zip_ref.extractall('/home/analyst/scratch/earthquake/')
zip_ref.close()
os.system("cp /home/analyst/scratch/earthquake/earthquake.shp /home/analyst/www/eq/catalog/complete/complete.shp")
os.system("cp /home/analyst/scratch/earthquake/earthquake.dbf /home/analyst/www/eq/catalog/complete/complete.dbf")
os.system("cp /home/analyst/scratch/earthquake/earthquake.prj /home/analyst/www/eq/catalog/complete/complete.prj")
os.system("cp /home/analyst/scratch/earthquake/earthquake.shx /home/analyst/www/eq/catalog/complete/complete.shx")
os.system("ogr2ogr -f KML /home/analyst/www/eq/catalog/complete/complete.kml /home/analyst/www/eq/catalog/complete/complete.shp")
time.sleep(5)
testfile = urllib.URLopener()
testfile.retrieve("https://ogsweb.ou.edu/api/earthquake?start=188201010000&end=202012312359&mag=0&format=csv", "/home/analyst/www/staff/earthquake/complete.csv")
os.system("cp /home/analyst/www/staff/earthquake/complete.csv ~/www/eq/catalog/complete/")
