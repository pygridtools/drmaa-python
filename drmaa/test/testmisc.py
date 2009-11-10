from unittest import TestCase
from drmaa import *

class Misc(TestCase):

    def setUp(self):
        self.s = Session()

    def test_drmaa_get_contact(self):
        """contact attribute works"""
        print self.s.contact

    def test_drmaa_version(self):
        """version attribute works"""
        print self.s.version

    def test_drmaa_get_DRM_system(self):
        """DRM system attribute works"""
        print self.s.drmsInfo

    def test_drmaa_get_DRMAA_implementation(self):
        """DRMAA implementation attribute works"""
        print self.s.drmaaImplementation
