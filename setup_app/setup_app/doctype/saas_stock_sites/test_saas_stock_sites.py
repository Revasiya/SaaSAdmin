# Copyright (c) 2023, OneHash and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
import unittest
from .saas_stock_sites import getSiteConfig
from .saas_stock_sites import refreshStockSites
import random
def deleteSomeSites():
    config = getSiteConfig()
    td = random.randint(1,int(config.stock_site_count))
    sites = frappe.db.get_list("SaaS stock sites",filters={"isUsed":"no"})
    if(len(sites) < int(config.stock_site_count)):
        return
    print("deleting ",td,"sites for testing")
    for i in range(td):
        name = sites[i]['name']
        frappe.delete_doc("SaaS stock sites",name)
     
class TestSaaSstocksites(unittest.TestCase):
    def test_getting_site_config(self):
        config = getSiteConfig()
        self.assertIsInstance(config.stock_site_count,str)
    def test_manage_stock_sites(self):
        config = getSiteConfig()
        deleteSomeSites()
        refreshStockSites()
        self.assertEqual(len(frappe.db.get_list("SaaS stock sites",filters={"isUsed":"no"})),int(config.stock_site_count))
        pass
        
