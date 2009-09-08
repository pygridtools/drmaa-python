#!/usr/bin/env python

import DRMAA

def main():
    """Create a DRMAA session and exit"""
    s=DRMAA.Session()
    print 'A DRMAA object was created'
    s.init()
    print 'A session was started successfully'
    s.exit()

if __name__=='__main__':
    main()
