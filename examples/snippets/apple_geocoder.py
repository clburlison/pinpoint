#!/usr/bin/python
from CoreLocation import (CLLocationManager,
                          CLLocation,
                          kCLDistanceFilterNone,
                          kCLLocationAccuracyBest)
from Foundation import (NSRunLoop,
                        NSDate,
                        NSObject,
                        NSBundle)


class MyLocationManagerDelegate(NSObject):
    """CoreLocation delegate for handling location lookups. This class
    is required for python to properly start/stop lookups with location
    services."""
    is_authorized = CLLocationManager.authorizationStatus()
    is_enabled = CLLocationManager.locationServicesEnabled()

    def init(self):
        """Define location manager settings for lookups."""
        self = super(MyLocationManagerDelegate, self).init()
        if not self:
            return
        self.locationManager = CLLocationManager.alloc().init()
        self.locationManager.setDelegate_(self)
        self.locationManager.setDistanceFilter_(kCLDistanceFilterNone)
        self.locationManager.setDesiredAccuracy_(kCLLocationAccuracyBest)
        self.locationManager.startUpdatingLocation()
        return self

    def locationManager_didUpdateToLocation_fromLocation_(self, manager,
                                                          newloc, oldloc):
        """Splits location data into separate pieces for processing later."""
        lat = newloc.coordinate().latitude
        lon = newloc.coordinate().longitude
        verAcc = newloc.verticalAccuracy()
        horAcc = newloc.horizontalAccuracy()
        altitude = newloc.altitude()
        time = newloc.timestamp()
        gmap = (r"https://www.google.com/maps/place/{0},{1}"
                "/@{0},{1},18z/data=!3m1!1e3".format(str(lat), str(lon)))
        plist = dict(
            Altitude=int(altitude),
            CurrentStatus=str("Successful"),
            GoogleMap=str(gmap),
            LastLocationRun=str(time),
            Latitude=str(lat),
            LatitudeAccuracy=int(verAcc),
            Longitude=str(lon),
            LongitudeAccuracy=int(horAcc),
        )
        print("Successful lookup request: {0}, {1}".format(
              plist['Latitude'], plist['Longitude']))

    def locationManager_didFailWithError_(self, manager, err):
        """Handlers errors for location manager."""
        if self.is_enabled is True:
            if self.is_authorized == 3:
                status = "Unable to locate"
            if self.is_authorized == 2:
                status = "Denied"
            if self.is_authorized == 1:
                status = "Restricted"
            if self.is_authorized == 0:
                status = "Not Determined"
        else:
            status = "Location Services Disabled"
        print(status)

finder = MyLocationManagerDelegate.alloc().init()
NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(5))
