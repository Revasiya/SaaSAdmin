# Copyright (c) 2023, OneHash and contributors
# For license information, please see license.txt
domain = "localhost"
import frappe
from frappe.model.document import Document
import os
from frappe.utils import random_string
def getSiteConfig():
    siteConfig = frappe.get_doc("SaaS settings")
    return siteConfig
def executeCommands(commands):
    command = " & ".join(commands)
    os.system(command)
def refreshStockSites():
    # this function runs every day and maintains the stock site
    config = getSiteConfig()
    commands = []
    currentStock = frappe.db.get_list("SaaS stock sites",filters={"isUsed":"no"})
    print("In stock",len(currentStock))
    if len(currentStock) < int(config.stock_site_count):
        number_of_sites_to_stock = int(config.stock_site_count) - len(currentStock)
        for _ in range(number_of_sites_to_stock):
            subdomain = random_string(10)
            adminPassword = random_string(5)
            print("creating",subdomain)
            commands.append("bench new-site {} --install-app erpnext --admin-password {} --db-root-password {}".format(subdomain + '.'+domain,adminPassword,config.db_password))
            site = frappe.new_doc("SaaS stock sites")
            site.subdomain = subdomain
            site.admin_password = adminPassword
            site.insert()
    executeCommands(commands)
class SaaSstocksites(Document):
	pass
        
	
