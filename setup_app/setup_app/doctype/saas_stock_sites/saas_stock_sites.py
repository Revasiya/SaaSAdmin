# Copyright (c) 2023, OneHash and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

def getSiteConfig():
    siteConfig = frappe.get_doc("SaaS settings")
    return siteConfig
class SaaSstocksites(Document):
	pass
        
	
