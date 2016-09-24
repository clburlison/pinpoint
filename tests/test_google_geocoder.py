#!/usr/bin/python
import subprocess
import re
import plistlib
import logging
import os
import json
import tempfile
from urllib2 import urlopen, URLError, HTTPError


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


def get_wireless_interface():
    """Returns the wireless interface device name, (e.g., en0 or en1)."""
    wireless_interface = None
    hardware_ports = subprocess.check_output(['/usr/sbin/networksetup',
                                              '-listallhardwareports'])
    match = re.search("(AirPort|Wi-Fi).*?(en\\d)", hardware_ports, re.S)
    if match:
        wireless_interface = match.group(2)
    return wireless_interface


def wireless_status():
    """Determine current power state for wireless adapter."""
    iface_name = get_wireless_interface()
    command = ['/usr/sbin/networksetup', '-getairportpower',
               iface_name]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    wifi_power = (proc.communicate()[0].replace('\n', '')
                  .split(":")[1].replace(' ', ''))
    return wifi_power


def wireless_scan():
    """Scan for current networks and return a sorted list of dictionary
    objects."""
    ssid_scan = subprocess.check_output(
                    ['/System/Library/PrivateFrameworks/'
                     'Apple80211.framework/Versions/A/'
                     'Resources/airport', '-s', '--xml']
                     )
    ssid_scan = plistlib.readPlistFromString(ssid_scan)
    values = []
    for i, val in enumerate(ssid_scan):
        wifi_stats = {'RSSI': val.get('RSSI'),
                      'BSSID': val.get('BSSID'),
                      'SSID_STR': val.get('SSID_STR')
                      }
        values.append(wifi_stats)

    # Sort our values by RSSI to increase accuracy of location
    return sorted(values, key=lambda k: k['RSSI'], reverse=True)

if wireless_status() == "On":
    scan = wireless_scan()
    api_url = ('https://maps.googleapis.com/maps/api'
               '/browserlocation/json?browser=firefox')
    count = 0
    for i, val in enumerate(scan):
        api_url += ('&wifi=mac:{0}&ssid:{1}&ss:{2}'.format(
                     val.get('BSSID'),
                     val.get('SSID_STR'),
                     val.get('RSSI')))
        count += 1
        if count == 5:
            break

    data = download_file(api_url)
    obj = json.loads(data)
    print obj["location"]["lat"]
    print obj["location"]["lng"]
