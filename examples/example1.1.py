#!/usr/bin/env python

import DRMAA

def main():
    """Create a session, show that each session has an id,
    use session id to disconnect, then reconnect. Then exit"""
    s=DRMAA.Session()
    s.init()
    print 'A session was started successfullly'
    response = s.getContact()
    print 'getContact() returns: ' + response
    s.exit()
    print 'Exited from session'

    s.init(response)
    print 'Session was restarted successfullly'
    s.exit()
    

if __name__=='__main__':
    main()
