#!/usr/bin/python
import subprocess
import plistlib


def wireless_scan():
    """Scan available wireless networks.

    Returns:
        Sorted array of dictionaries with rssi, bssid, and ssid_str from
        strongest rssi value to weakest.

    """
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
    return sorted(values, key=lambda k: k['RSSI'], reverse=True)


print wireless_scan()
