# Credits: This is a modified version of the python script from https://github.com/akrherz/iem/blob/master/scripts/asos/iem_scraper_example.py
# Modified by: Po-Yan Tsang

import json
import time
import datetime
import csv
# Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

# Number of attempts to download data
MAX_ATTEMPTS = 6
# HTTPS here can be problematic for installs that don't have Lets Encrypt CA
SERVICE = "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"


def download_data(uri):
    """Fetch the data from the IEM
    The IEM download service has some protections in place to keep the number
    of inbound requests in check.  This function implements an exponential
    backoff to keep individual downloads from erroring.
    Args:
      uri (string): URL to fetch
    Returns:
      string data
    """
    attempt = 0
    while attempt < MAX_ATTEMPTS:
        try:
            data = urlopen(uri, timeout=300).read().decode('utf-8')
            if data is not None and not data.startswith('ERROR'):
                return data
        except Exception as exp:
            print("download_data(%s) failed with %s" % (uri, exp))
            time.sleep(5)
        attempt += 1

    print("Exhausted attempts to download, returning empty data")
    return ""


def get_stations_from_filelist(filename):
    """Build a listing of stations from a simple file listing the stations.
    The file should simply have one station per line.
    """
    stations = []
    for line in open(filename):
        stations.append(line.split(',')[0].strip())
    return stations


def main():
    """Our main method"""
    # timestamps in UTC to request data for
    startts = datetime.datetime(2014, 3, 1)
    endts = datetime.datetime(2018, 11, 1)

    # customizing the URL to get comma-delimited CSV without header, and only temperature, wind speed, and precip info
    service = SERVICE + "data=tmpf&data=sped&data=p01i&data=gust_mp&tz=Etc/UTC&format=onlycomma&latlon=no&direct=no&report_type=1&report_type=2&"

    # restricting time period to March-2014 to November-2018
    service += startts.strftime('year1=%Y&month1=%m&day1=%d&')
    service += endts.strftime('year2=%Y&month2=%m&day2=%d&')

    # Two examples of how to specify a list of stations
    stations = get_stations_from_filelist("airports.csv")
    count=0
    for station in stations:
        if count==0:
            print('skip reading header in airports.csv')
        else:
            uri = '%s&station=%s' % (service, station)
            print('Downloading: %s' % (station, ))
            data = download_data(uri)
            outfn = './data/%s_2017_weather.csv' % (station)
            out = open(outfn, 'w')
            out.write(data)
            out.close()
        count+=1

main()
