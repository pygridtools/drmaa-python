#!/usr/bin/env python

import drmaa

def main():
    """Create a session, show that each session has an id,
    use session id to disconnect, then reconnect. Then exit"""
    s = drmaa.Session()
    s.initialize()
    print 'A session was started successfully'
    response = s.contact
    print 'session contact returns: ' + response
    s.exit()
    print 'Exited from session'

    s.initialize(response)
    print 'Session was restarted successfullly'
    s.exit()
    

if __name__=='__main__':
    main()
