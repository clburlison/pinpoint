#!/usr/bin/python
# encoding: utf-8

# This script requires the tinys3 module which has a dependency on requests.
# You can install both with:
#   sudo pip install tinys3


import tinys3

S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''
ENDPOINT = 's3.amazonaws.com' # this is the US East standard endpoint
DEFAULT_BUCKET = 'my_super_awesome_bucket'
LOG_FILE = '/Library/Application Support/pinpoint/location.plist'

conn = tinys3.Connection(S3_ACCESS_KEY, 
                         S3_SECRET_KEY, 
                         tls=True,
                         endpoint=ENDPOINT,
                         default_bucket=DEFAULT_BUCKET)

f = open(LOG_FILE,'rb')
try:
    conn.upload('XXXXXXXXX.plist',f,
                headers={
                'x-amz-storage-class': 'REDUCED_REDUNDANCY'
                },
                public=False)
except requests.exceptions.ConnectionError, e:
    print "We ran into an error. We should log this someplace good."
    print e