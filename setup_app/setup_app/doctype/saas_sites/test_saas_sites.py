# Copyright (c) 2023, OneHash and Contributors
# See license.txt

from frappe.utils import random_string
from frappe.tests.utils import FrappeTestCase
import unittest
from .saas_sites import setupSite
class TestSaaSsites(unittest.TestCase):
	def test_creating_new_site(self):
		setupSite(random_string(4),'admin','Test fname',"test lname","test compay name",'test@email.com')
		return 1
	