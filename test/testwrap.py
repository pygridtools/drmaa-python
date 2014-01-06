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

"""
test module for the functional interface
"""

from __future__ import absolute_import, print_function, unicode_literals

import sys
import unittest
from os import environ

from nose.tools import eq_

from drmaa import Session, JobTemplate
from drmaa.const import (JobControlAction, JobSubmissionState, PLACEHOLDER_HD,
                         SUBMISSION_STATE_ACTIVE)


# Python 3 compatability help
if sys.version_info < (3, 0):
    bytes = str
    str = unicode


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
        jt.args = ['-c', "print('hello from python!')"]
        if hasattr(self, 'jt_tweaks'):
            self.jt_tweaks()
        self.jid = Session.runJob(jt)

    def tearDown(self):
        Session.deleteJobTemplate(self.jt)


class EnvironmentTest(SubmitBase):

    def jt_tweaks(self):
        environ['PIPPO'] = 'aaaa'
        self.jt.args = (["-c",
                         ("from os import environ as env; assert ('PIPPO' in " +
                          "env) and (env['PIPPO'] == 'aaaa')")])
        self.jt.jobEnvironment = environ

    def test_environment(self):
        """environment variables are correctly passed to submitted jobs"""
        jinfo = Session.wait(self.jid)
        eq_(jinfo.jobId, self.jid)
        assert hasattr(jinfo, 'hasExited')
        assert hasattr(jinfo, 'exitStatus') and jinfo.exitStatus == 0


class Submit(SubmitBase):

    def test_run_bulk(self):
        """run bulk job"""
        jids = Session.runBulkJobs(self.jt, 1, 2, 1)

    def test_wait(self):
        """waiting for job completion"""
        jinfo = Session.wait(self.jid)
        eq_(jinfo.jobId, self.jid)
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
        except Exception as e:
            assert e.args[0].startswith('code 24')  # no rusage


class JobTemplateTests(unittest.TestCase):

    def setUp(self):
        self.jt = Session.createJobTemplate()

    def test_scalar_attributes(self):
        """scalar attributes work"""
        for name, value in [("remoteCommand", 'cat'),
                            ("jobSubmissionState", SUBMISSION_STATE_ACTIVE),
                            ("workingDirectory", JobTemplate.HOME_DIRECTORY),
                            ("nativeSpecification", '-shell yes'),
                            ("blockEmail", False),
                            ("jobName", 'pippo'),
                            ("inputPath", ":%s" % PLACEHOLDER_HD),
                            ("outputPath", ":%s/pippo.out" % PLACEHOLDER_HD),
                            ("errorPath", ":%s/pippo.out" % PLACEHOLDER_HD),
                            ("joinFiles", True)]:
            setattr(self.jt, name, value)
            eq_(getattr(self.jt, name), value)

    # skipping this. the parameters above have to be tweaked a bit
    def xtest_tmp(self):
        self.test_scalar_attributes()
        self.jt.args = ['.colordb']
        jid = Session.runJob(self.jt)
        jinfo = Session.wait(jid)
        print(jinfo)

    def test_vector_attributes(self):
        """vector attributes work"""
        args = ['10', 'de', 'arglebargle']
        self.jt.args = args
        eq_(self.jt.args, args)
        em = ['baz@quz.edu', 'foo@bar.com']
        self.jt.email = em
        eq_(self.jt.email, em)

    def test_dict_attribute(self):
        """dict attributes work"""
        from drmaa.const import ATTR_BUFFER
        self.jt.jobEnvironment = environ
        for x in environ:
            # attribute values could be truncated. For some reason,
            # GE returns the first 1014 chars available (!)
            eq_(environ[x][:ATTR_BUFFER - 10],
                self.jt.jobEnvironment[x][:ATTR_BUFFER - 10])

    def test_attribute_names(self):
        """attribute names work"""
        assert len(self.jt.attributeNames) > 0

    def test_block_email(self):
        """blockEmail works"""
        self.jt.blockEmail = True
        assert self.jt.blockEmail
        self.jt.blockEmail = False
        assert not self.jt.blockEmail

    def test_join_files(self):
        """joinFiles works"""
        self.jt.joinFiles = True
        assert self.jt.joinFiles
        self.jt.joinFiles = False
        assert not self.jt.joinFiles

    def test_submission_state(self):
        """submission state attributes work"""
        self.jt.jobSubmissionState = JobSubmissionState.HOLD_STATE
        eq_(self.jt.jobSubmissionState, JobSubmissionState.HOLD_STATE)
        self.jt.jobSubmissionState = JobSubmissionState.ACTIVE_STATE
        eq_(self.jt.jobSubmissionState, JobSubmissionState.ACTIVE_STATE)

    def tearDown(self):
        Session.deleteJobTemplate(self.jt)
