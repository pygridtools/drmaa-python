# -----------------------------------------------------------
#  Copyright (C) 2009 StatPro Italia s.r.l. 
#                                                            
#  StatPro Italia                                            
#  Via G. B. Vico 4                                          
#  I-20123 Milano                                            
#  ITALY                                                     
#                                                            
#  phone: +39 02 96875 1                                     
#  fax:   +39 02 96875 605                                   
#                                                            
#  email: info@riskmap.net                                   
#                                                            
#  This program is distributed in the hope that it will be   
#  useful, but WITHOUT ANY WARRANTY; without even the        
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR   
#  PURPOSE. See the license for more details.                
# -----------------------------------------------------------

"""test module for the functional interface"""

from drmaa import *
import unittest
from nose.tools import assert_equal

def setup():
    "initialize DRMAA library"
    Session.initialize()

def teardown():
    "finalize DRMAA session"
    Session.exit()

def test_allocate():
    "job template allocation"
    jt = Session.createJobTemplate()
    Session.deleteJobTemplate(jt)

class SubmitBase(unittest.TestCase):

    def setUp(self):
        self.jt = jt = Session.createJobTemplate()
        jt.args = ['2']
        jt.remoteCommand = 'sleep'
        self.jid = Session.runJob(jt)

    def tearDown(self):
        Session.deleteJobTemplate(self.jt)

class Submit(SubmitBase):

    def test_run_bulk(self):
        """run bulk job"""
        jids = Session.runBulkJobs(self.jt, 1, 2, 1)

    def test_wait(self):
        """waiting for job completion"""
        jinfo = Session.wait(self.jid)
        #print jinfo

    def test_sync(self):
        """sync with a job"""
        Session.synchronize(self.jid)

    def test_control_terminate(self):
        """control/terminate works"""
        Session.control(self.jid, JobControlAction.TERMINATE)
        Session.synchronize(self.jid,
                            Session.TIMEOUT_WAIT_FOREVER,
                            False)
        try:
            Session.wait(self.jid, Session.TIMEOUT_WAIT_FOREVER)
        except Exception, e:
            assert e.message.startswith('code 24') # no rusage

class JobTemplateTests(unittest.TestCase):
    def setUp(self):
        self.jt = Session.createJobTemplate()

    def test_scalar_attributes(self):
        """scalar attributes work"""
        for name, value in [("remoteCommand"           ,'pippo'),
                            ("jobSubmissionState"      ,'drmaa_active'),
                            ("workingDirectory"        ,'pippo'),
                            ("jobCategory"             ,'pippo'),
                            ("nativeSpecification"     ,'-shell yes'),
                            ("blockEmail"              , False),
                            ("startTime"               ,'00:01'),
                            ("jobName"                 ,'pippo'),
                            ("inputPath"               ,'/tmp/input'),
                            ("outputPath"              ,'/tmp/output'),
                            ("errorPath"               ,'/tmp/error'),
                            ("joinFiles"               ,True),]:
                            #("transferFiles"           ,'i')
                            #("deadlineTime"            ,'10'),
                            #("hardWallclockTimeLimit"  ,'10:00'),
                            #("softWallclockTimeLimit"  ,'00:00:10'),]:
                            #("hardRunDurationLimit"    ,'00:01:00'),
                            #("softRunDurationLimit"    ,'00:01:00')]:
            setattr(self.jt, name, value)
            assert getattr(self.jt, name) == value

    def test_vector_attributes(self):
        """vector attributes work"""
        args = ['10', 'de', 'arglebargle']
        self.jt.args = args
        assert self.jt.args == args
        em = ['baz@quz.edu', 'foo@bar.com']
        self.jt.email = em
        assert self.jt.email == em

    def test_dict_attribute(self):
        """dict attributes work"""
        from os import environ
        self.jt.environment = environ
        assert environ == self.jt.environment

    def test_attribute_names(self):
        """attribute names work"""
        assert len(self.jt.attributeNames) > 0

    def tearDown(self):
        Session.deleteJobTemplate(self.jt)
