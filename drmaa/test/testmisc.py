from unittest import TestCase
from drmaa import *

class Misc(TestCase):

    def setUp(self):
        self.s = Session()

    def test_drmaa_get_contact(self):
        print self.s.contact

    def test_drmaa_version(self):
        print self.s.version

    def test_drmaa_get_DRM_system(self):
        print self.s.drmsInfo

    def test_drmaa_get_DRMAA_implementation(self):
        print self.s.drmaaImplementation

    def tearDown(self):
        self.s.exit()
