#!/usr/bin/python
import subprocess
import re


def get_wireless_interface():
    """Returns the wireless interface device name, (e.g., en0 or en1)."""
    wireless_interface = None
    hardware_ports = subprocess.check_output(['/usr/sbin/networksetup',
                                              '-listallhardwareports'])
    match = re.search("(AirPort|Wi-Fi).*?(en\\d)", hardware_ports, re.S)
    if match:
        wireless_interface = match.group(2)
    return wireless_interface


def wireless_status(iface_name):
    """Determine current power state for wireless adapter."""
    command = ['/usr/sbin/networksetup', '-getairportpower',
               iface_name]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    wifi_power = (proc.communicate()[0].replace('\n', '')
                  .split(":")[1].replace(' ', ''))
    return wifi_power

print wireless_status(get_wireless_interface())
