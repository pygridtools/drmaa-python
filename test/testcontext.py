'''
Tests related to with using context managers.
'''

from __future__ import absolute_import, print_function, unicode_literals

from drmaa import Session


def test_with_session():
    """'with' statement works with Session"""
    with Session() as s:
        print(s.version)
        print(s.contact)
        print(s.drmsInfo)
        print(s.drmaaImplementation)


def test_with_jt():
    """'with' statement works with JobTemplate"""
    s = Session()
    s.initialize()
    with s.createJobTemplate() as jt:
        jt.remoteCommand = 'sleep'
        jt.args = ['10']
        jid = s.runJob(jt)
        print(s.wait(jid))
    s.exit()
