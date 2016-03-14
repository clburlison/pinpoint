pinpoint
===

![pinpoint logo](/support_files/pinpoint-logo-wide.png)

A python script for finding your Mac.

Author: Clayton Burlison - https://clburlison.com  


# Info

:bangbang: Munkireport users [read this](https://github.com/clburlison/pinpoint/wiki/MunkiReport-Setup)! :bangbang:

This script uses Apple's [CoreLocation framework](https://developer.apple.com/library/ios/documentation/CoreLocation/Reference/CoreLocation_Framework/) to determine the approximate location of your Mac.

Limited to **10.8 - 10.11**. 

On each run Location Services will be enabled, and the system Python binary will be given access to Location Services (LS). Due to how LS and the CoreLocation framework interact the first run to enable all the services will take ~45 seconds. Sequential runs take about 8-12 seconds and have a pretty high accuracy.

After the run pinpoint will write a plist file containing the data from the run. By default this file ends up: 

```bash
/Library/Application\ Support/pinpoint/location.plist
```

More information can be found on the [Wiki](https://github.com/clburlison/pinpoint/wiki).

# Legal Notice
> pinpoint should only be installed on devices that you have authorization to do so on. Data collected from this project is directly uploaded to Apple, Inc. and Google, Inc. via geocoding APIs for in order to locate your Mac. 
>
> Usage of this project for illegal or immoral activities is deeply frowned upon. These activities could have consequences including fines and jail time depending on your location. I in no way endorse the usage of this project for these acts.

I am not a lawyer and all questions regarding the legality of this project within a specific organization should be taken up with a real lawyer.




# Credits
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
