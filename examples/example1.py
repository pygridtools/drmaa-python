#!/usr/bin/env python

import drmaa

def main():
    """Create a drmaa session and exit"""
    s=drmaa.Session()
    s.initialize()
    print 'A session was started successfully'
    s.exit()

if __name__=='__main__':
    main()
