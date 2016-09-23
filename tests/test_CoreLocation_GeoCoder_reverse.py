#!/usr/bin/python
from CoreLocation import CLLocation
from CoreLocation import CLGeocoder
from Foundation import NSLog, NSRunLoop, NSDate

location = CLLocation.alloc().initWithLatitude_longitude_(37.331762, -122.030561)
address = "1 Infinite Loop, Cupertino, CA 95014"

class ReverseLookup(object):
    def myCompletionHandler(placemarks, error):
        if error is not None:
            print error
        else:
            print placemarks

    # Convert coordinates to address
    geocoder = CLGeocoder.alloc().init()
    geocoder.reverseGeocodeLocation_completionHandler_(location, myCompletionHandler)
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(1))

    # Convert street address into coordinates
    geocoder.geocodeAddressString_completionHandler_(address, myCompletionHandler)
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(1))

ReverseLookup()
