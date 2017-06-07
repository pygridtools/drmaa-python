#!/usr/bin/env python

from __future__ import print_function
import drmaa


def main():
    """Create a session, show that each session has an id,
    use session id to disconnect, then reconnect. Then exit"""
    s = drmaa.Session()
    s.initialize()
    print('A session was started successfully')
    response = s.contact
    print('session contact returns: ' + response)
    s.exit()
    print('Exited from session')

    s.initialize(response)
    print('Session was restarted successfully')
    s.exit()
    

if __name__=='__main__':
    main()
