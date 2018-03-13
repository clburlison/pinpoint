#!/usr/bin/python
import subprocess
import re
import plistlib
import logging
import os
import json
import tempfile
from urllib2 import urlopen, URLError, HTTPError

plist = dict(Latitude=str(37.331762),
             Longitude=str(-122.030561))


def download_file(url):
    """Download a simple file from the Internet."""
    logging.info("Download file from Google")
    try:
        temp_file = os.path.join(tempfile.mkdtemp(), 'tempdata')
        f = urlopen(url)
        with open(temp_file, "wb") as local_file:
            local_file.write(f.read())
        logging.info("Download successful")
    except HTTPError, e:
        logging.debug("HTTP Error: %s, %s", e.code, url)
    except URLError, e:
        logging.debug("URL Error: %s, %s", e.reason, url)
    try:
        file_handle = open(temp_file)
        data = file_handle.read()
        file_handle.close()
    except (OSError, IOError):
        logging.debug("Couldn't read %s", temp_file)
        return False
    try:
        os.unlink(temp_file)
        os.rmdir(os.path.dirname(temp_file))
    except (OSError, IOError):
        pass
    return data


def address_lookup(plist):
    """Resolve coordinates to a street address."""
    service = 'google'
    api_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='
    logging.info("Doing a reverse lookup via: {0}".format(service))
    lat = plist['Latitude']
    lon = plist['Longitude']
    if service == 'google':
        try:
            url = '%s%s,%s' % (api_url, lat, lon)
            data = download_file(url)
            obj = json.loads(data)
            address = obj["results"][0]["formatted_address"]
        except:
            address = 'Google reverse lookup failed.'
            logging.warn(address)
    return address

print address_lookup(plist)
