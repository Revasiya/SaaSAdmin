# Copyright (c) 2023, OneHash and contributors
# For license information, please see license.txt
import frappe
domain = frappe.get_doc('SaaS settings').domain
from frappe.model.document import Document
import os
from frappe.utils import random_string
def getSiteConfig():
    siteConfig = frappe.get_doc("SaaS settings")
    return siteConfig
def create_multiple_sites_in_parallel(commands):
    from subprocess import Popen
    processes = [Popen(cmd, shell=True) for cmd in commands]
    for p in processes: 
        p.wait()
    
    
@frappe.whitelist()    
def refreshStockSites(*args, **kwargs):
    # this function runs every day and maintains the stock site
    print("refreshing stock sites")
    config = getSiteConfig()
    commands = []
    currentStock = frappe.db.get_list("SaaS stock sites",filters={"isUsed":"no"})
    print("In stock",len(currentStock))
    db_values = []
    if len(currentStock) < int(config.stock_site_count):
        number_of_sites_to_stock = int(config.stock_site_count) - len(currentStock)
        for _ in range(number_of_sites_to_stock):
            subdomain = random_string(10)
            adminPassword = random_string(5)
            this_command = []
            this_command.append("bench new-site {} --install-app erpnext  --admin-password {} --db-root-password {}".format(subdomain + '.'+domain,adminPassword,config.db_password))
            this_command.append("bench --site {} install-app clientside".format(subdomain + '.'+domain))
            command = " ; ".join(this_command)
            commands.append(command)
            db_values.append([subdomain,adminPassword])
    
    create_multiple_sites_in_parallel(commands)
    for values in db_values:
        site = frappe.new_doc("SaaS stock sites")
        site.subdomain = values[0]
        site.admin_password = values[1]
        site.insert()
class SaaSstocksites(Document):
	pass
        
	
