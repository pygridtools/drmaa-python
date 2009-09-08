#!/usr/bin/env python

import DRMAA

def main():
    """Query the system."""
    s=DRMAA.Session()
    print 'A DRMAA object was created'
    print 'Supported contact strings: ' + s.getContact()
    print 'Supported DRM systems: ' + str(s.getDRMSInfo())
    print 'Supported DRMAA implementations: ' + str(s.getDRMAAImplementation())
    
    
    s.init()
    print 'A session was started successfully'
    print 'Supported contact strings: ' + s.getContact()
    print 'Supported DRM systems: ' + str(s.getDRMSInfo())
    print 'Supported DRMAA implementations: ' + str(s.getDRMAAImplementation())
    print 'Version ' + str(s.getVersion())

    print 'Exiting'
    s.exit()
    

if __name__=='__main__':
    main()
