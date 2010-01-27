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

import unittest
from nose.tools import assert_equal
from drmaa import *
from drmaa import const as c
from os import environ

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
        jt.remoteCommand = 'python'
        jt.args = ['-c', "print 'hello from python!'"]
        if hasattr(self, 'jt_tweaks'):
            self.jt_tweaks()
        self.jid = Session.runJob(jt)

    def tearDown(self):
        Session.deleteJobTemplate(self.jt)

class EnvironmentTest(SubmitBase):

    def jt_tweaks(self):
        environ['PIPPO'] = 'aaaa'
        self.jt.args = (
            ["-c",
             "from os import environ as env; assert ('PIPPO' in env) and (env['PIPPO'] == 'aaaa')"])
        self.jt.jobEnvironment = environ

    def test_environment(self):
        """environment variables are correctly passed to submitted jobs"""
        jinfo = Session.wait(self.jid)
        assert jinfo.jobId == self.jid
        assert hasattr(jinfo, 'hasExited')
        print jinfo.exitStatus
        assert hasattr(jinfo, 'exitStatus') and jinfo.exitStatus == 0


class Submit(SubmitBase):

    def test_run_bulk(self):
        """run bulk job"""
        jids = Session.runBulkJobs(self.jt, 1, 2, 1)

    def test_wait(self):
        """waiting for job completion"""
        jinfo = Session.wait(self.jid)
        assert jinfo.jobId == self.jid
        assert hasattr(jinfo, 'hasExited')
        assert hasattr(jinfo, 'hasExited') and type(jinfo.hasExited) is bool
        assert hasattr(jinfo, 'hasSignal') and type(jinfo.hasSignal) is bool
        assert hasattr(jinfo, 'terminatedSignal') and type(jinfo.terminatedSignal) is str
        assert hasattr(jinfo, 'hasCoreDump') and type(jinfo.hasCoreDump) is bool
        assert hasattr(jinfo, 'wasAborted') and type(jinfo.wasAborted) is bool
        assert hasattr(jinfo, 'exitStatus') and type(jinfo.exitStatus) is int
        assert hasattr(jinfo, 'resourceUsage') and type(jinfo.resourceUsage) is dict

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
            assert e.args[0].startswith('code 24') # no rusage

class JobTemplateTests(unittest.TestCase):
    def setUp(self):
        self.jt = Session.createJobTemplate()

    def test_scalar_attributes(self):
        """scalar attributes work"""
        for name, value in [("remoteCommand", 'cat'),
                            ("jobSubmissionState", c.SUBMISSION_STATE_ACTIVE),
                            ("workingDirectory", JobTemplate.HOME_DIRECTORY),
                            #("jobCategory", '/tmp'),
                            ("nativeSpecification", '-shell yes'),
                            ("blockEmail", False),
                            #("startTime", '00:01'),
                            ("jobName", 'pippo'),
                            ("inputPath", ":%s" % c.PLACEHOLDER_HD),
                            ("outputPath", ":%s/pippo.out" % c.PLACEHOLDER_HD),
                            ("errorPath", ":%s/pippo.out" % c.PLACEHOLDER_HD),
                            ("joinFiles", True),]:
                            #("transferFiles"           ,'i')
                            #("deadlineTime"            ,'10'),
                            #("hardWallclockTimeLimit"  ,'10:00'),
                            #("softWallclockTimeLimit"  ,'00:00:10'),]:
                            #("hardRunDurationLimit"    ,'00:01:00'),
                            #("softRunDurationLimit"    ,'00:01:00')]:
            setattr(self.jt, name, value)
            assert getattr(self.jt, name) == value

    # skipping this. the parameters above have to be tweaked a bit
    def xtest_tmp(self):
        self.test_scalar_attributes()
        self.jt.args=['.colordb']
        jid=Session.runJob(self.jt)
        jinfo = Session.wait(jid)
        print jinfo

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
        from drmaa.const import ATTR_BUFFER
        self.jt.jobEnvironment = environ
        for x in environ:
            # attribute values could be truncated. For some reason,
            # GE returns the first 1014 chars available (!)
            assert_equal(environ[x][:ATTR_BUFFER-10],
                         self.jt.jobEnvironment[x][:ATTR_BUFFER-10])

    def test_attribute_names(self):
        """attribute names work"""
        assert len(self.jt.attributeNames) > 0

    def test_block_email(self):
        """blockEmail works"""
        self.jt.blockEmail = True
        assert self.jt.blockEmail == True
        self.jt.blockEmail = False
        assert self.jt.blockEmail == False

    def test_join_files(self):
        """joinFiles works"""
        self.jt.joinFiles = True
        assert self.jt.joinFiles == True
        self.jt.joinFiles = False
        assert self.jt.joinFiles == False

    def tearDown(self):
        Session.deleteJobTemplate(self.jt)
