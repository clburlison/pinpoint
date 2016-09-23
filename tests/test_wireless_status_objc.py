#!/usr/bin/python
import objc

bundle_path = '/System/Library/Frameworks/CoreWLAN.framework'
objc.loadBundle('CoreWLAN',
                bundle_path=bundle_path,
                module_globals=globals())


def mac_has_wireless(self):
    """Check to see if this Mac has a wireless NIC. If it doesn't the
    CoreLocation lookup will fail."""
    iface_name = CWInterface.interfaceNames()
    # The first interface can be assumed to be the airport card.
    # This step isn't needed but is helpful.
    iface_name = iface_name.itervalues().next()
    return True if iface_name else False


def wireless_status():
    """Determine current power state for wireless adapter."""
    iface = CWInterface.interface()
    wifi_power = iface.powerOn()
    wifi_power = "On" if wifi_power == 1 else "Off"
    return wifi_power

print wireless_status()
