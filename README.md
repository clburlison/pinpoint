pinpoint
===

![pinpoint logo](/support_files/pinpoint-logo-wide.png)

Python based location script for enabling and finding your Mac.

Author: Clayton Burlison - https://clburlison.com  


#What does pinpoint do?
This script is limited to **10.8 - 10.11**. 

This script uses Apple's CoreLocation framework to determine the approximate latitude, and longitude of your Mac.

Currently, on each run Location Services will be enabled, and the system Python binary will be given access to Location Services (LS). Due to how LS and the CoreLocation framework interact the first run to enable all the services will take ~45 seconds. Sequential runs take about 8-12 seconds and have a pretty high accuracy.

After the run pinpoint will write a plist file containing the data from the run. By default this file ends up: 

```bash
/Library/Application\ Support/pinpoint/location.plist
```

More information can be found on the [Wiki](https://github.com/clburlison/pinpoint/wiki).

#Legal Notice
_coming soon_


#Credits
Based off of works by:  

| Author  |  Project Link |
|---|---|
| [@arubdesu](https://github.com/arubdesu) | https://gist.github.com/arubdesu/b72585771a9f606ad800 |
| [@pudquick](https://github.com/pudquick) | https://gist.github.com/pudquick/c7dd1262bd81a32663f0 |
| [@pudquick](https://github.com/pudquick) | https://gist.github.com/pudquick/329142c1740500bd3797 | 
| [@lindes](https://github.com/lindes)   | https://github.com/lindes/get-location/ | 
| [University of Utah, Marriott Library](https://github.com/univ-of-utah-marriott-library-apple) | [privacy_services_manager](https://github.com/univ-of-utah-marriott-library-apple/privacy_services_manager) |
| [Munki](https://github.com/munki) | [FoundationPlist.py](https://github.com/munki/munki/blob/master/code/client/munkilib/FoundationPlist.py) |
| [Google Inc.](https://github.com/macops) | [supervisor](https://github.com/munki/munki/blob/master/code/client/supervisor) |