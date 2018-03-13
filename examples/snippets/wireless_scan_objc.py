#!/usr/bin/python
import objc

bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
objc.loadBundle('CoreWLAN',
                bundle_path=bundle_path,
                module_globals=globals())


def wireless_scan():
    """Scan available wireless networks.

    Returns:
        Sorted array of dictionaries with rssi, bssid, and ssid_str from
        strongest rssi value to weakest.

    """
    iface = CWInterface.interface()
    results, error = iface.scanForNetworksWithName_includeHidden_error_(
        None, True, None)
    if error:
        return error
    values = []
    for i in results:
        if i.ssid() is None:
            continue
        wifi_stats = {'RSSI': i.rssiValue(),
                      'BSSID': i.bssid(),
                      'SSID_STR': i.ssid()
                      }
        values.append(wifi_stats)
    return sorted(values, key=lambda k: k['RSSI'], reverse=True)


print wireless_scan()
