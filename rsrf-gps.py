import urllib
import time
import logging
import requests
import gzip
import shutil
import subprocess
import sys, os

from datetime import datetime, date, timedelta

try: 
    logmessagestart = 'rsrf-gps.py: ' + str(datetime.now()) + ": "

    yesterday = datetime.now() - timedelta(1)
    day_of_year = yesterday.timetuple().tm_yday

    print logmessagestart + yesterday.strftime("%m%d%y %H:%M:%S")
    print logmessagestart + 'day of year: ' + str(day_of_year)

    latlng = "37.776319,-122.416417,100"

    GPSurl = "ftp://cddis.gsfc.nasa.gov/gnss/data/daily/" + str(yesterday.strftime("%Y")) + "/brdc/brdc" + str('%03d' % yesterday.timetuple().tm_yday) + "0." + str(yesterday.strftime("%y")) + "n.Z"

    print logmessagestart + GPSurl

    satFile = urllib.URLopener()
    satFile.retrieve(GPSurl, "yesterday_sat_file.z")

    outfilename = "yesterday_sat_file"

    bashCommand = "gzip -d -f yesterday_sat_file.z"

    p = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()

    yesterday = datetime.now() - timedelta(1)

    yesterdayTime = str(yesterday.strftime("%Y/%m/%d,%H:%M:%S"))

    bladegpsCommand = "./bladegps -e yesterday_sat_file -l " + latlng + " -d 86400 -t " + yesterdayTime

    print logmessagestart + bladegpsCommand

    p = subprocess.Popen(bladegpsCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    errorInfo = str(exc_type) + ' ' + str(fname) + ' Line number:' + str(exc_tb.tb_lineno) 
    logging.warning('rsrf-gps/run.py: %s, Failure: %s', str(datetime.now()), str(e))
    print(errorInfo)
    emailData = {"from": "eFemto Monitor - Nerdwallet <efemto-monitor-nerdwallet@repeaterstore.com>",
                  "to": "Sina <sina@repeaterstore.com>",
                  "subject": "GPS Warning",
                  "text": errorInfo + '\n' + str(e) }
    requests.post("https://api.mailgun.net/v3/mg.repeaterstore.com/messages", auth=("api", "key-ae46fc26914330c3bd4e751d0ec859ee"), data=emailData)
