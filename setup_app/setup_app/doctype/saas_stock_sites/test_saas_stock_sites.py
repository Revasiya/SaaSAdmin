# Copyright (c) 2023, OneHash and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
import unittest
from .saas_stock_sites import getSiteConfig

class TestSaaSstocksites(unittest.TestCase):
    def test_getting_site_config(self):
        config = getSiteConfig()
        print(config)
        self.assertEqual(config["stock site count"],15)
        
        
