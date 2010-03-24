#!/usr/bin/env python

import drmaa

def main():
    """Query the system."""
    s = drmaa.Session()
    s.initialize()
    print 'A DRMAA object was created'
    print 'Supported contact strings: ' + s.contact
    print 'Supported DRM systems: ' + str(s.drmsInfo)
    print 'Supported DRMAA implementations: ' + str(s.drmaaImplementation)
    print 'Version ' + str(s.version)

    print 'Exiting'
    s.exit()
    
if __name__=='__main__':
    main()
