# Copyright (c) 2023, OneHash and contributors
# For license information, please see license.txt
import sys
import json
sys.path.append('../saas_stock_sites')
import frappe
import os
import subprocess as sp
from time import sleep
from frappe.model.document import Document
domain = frappe.get_doc('SaaS settings').domain
log = open('log.txt','a')
def executeCommands(commands):
    commands.append("bench --version")
    config = frappe.get_doc("SaaS settings")
    command = " ; ".join(commands)
    print("executing ",command)
    process = sp.Popen(command,shell=True,stdout=log)
    process.wait()
    if(domain != 'localhost'):
        os.system('echo {} | sudo -S sudo service nginx reload'.format(config.root_password))
    print(process.returncode)
    
@frappe.whitelist()   
def test_site(*args, **kwargs):
    print( "test site called")
    print(frappe.publish_realtime("sex"))
    frappe.publish_realtime('site_created',message={"site":"test"})
    return "done"
    
@frappe.whitelist(allow_guest=True)   
def setupSite(*args, **kwargs):
    print(kwargs)
    doc = json.loads(kwargs["doc"])
    print(doc)
    company_name = doc["company_name"]
    subdomain = doc["domain"]
    admin_password = doc["password"]
    fname = doc["first_name"]
    lname = doc["last_name"]
    email = doc['email']
    print(company_name,subdomain,admin_password,fname,lname,email)
    config = frappe.get_doc("SaaS settings")
    print(config)
    stock_sites = frappe.db.get_list("SaaS stock sites",filters={'isused':"no"},ignore_permissions=True)
    print(stock_sites)
    target_site = None
    commands = []
    if(len(stock_sites) == 0):  
        commands.append("bench new-site {} --install-app erpnext --admin-password {} --db-root-password {}".format(subdomain + '.'+domain,admin_password,config.db_password))
        site = frappe.new_doc("SaaS stock sites")
        site.subdomain = subdomain
        site.admin_password = admin_password
        site.insert(ignore_permissions=True)
        target_site = site
    else:
        target_site = frappe.get_doc("SaaS stock sites",stock_sites[0]["name"],ignore_permissions=True)
    print("using ",target_site.subdomain,"to create ",subdomain)
    
    current_site = subdomain + '.' + domain
    print(target_site.subdomain + '.' + domain )
    commands.append('export SITE_{}_STATUS=creating'.format(current_site).replace('.','M'))
    commands.append('bench --site {} set-admin-password {}'.format(target_site.subdomain + '.' + domain ,admin_password))
    commands.append('bench setup add-domain {} --site {}'.format(current_site,target_site.subdomain + '.' + domain))
    target_site.isused = 'yes'
    print("s",target_site)
    target_site.save(ignore_permissions=True)
    commands.append('bench setup nginx --yes')
    executeCommands(commands)
    new_site = frappe.new_doc("SaaS sites")
    new_site.password = admin_password
    new_site.first_name = fname
    new_site.lname = lname
    new_site.company_name = company_name
    new_site.email = email
    new_site.domain = current_site
    new_site.save(ignore_permissions=True)
    return "done"
@frappe.whitelist(allow_guest=True)  
def checkSiteCreated(*args, **kwargs):
    doc = json.loads(kwargs["doc"])
    sitename = doc["domain"]
    print(sitename + domain)
    site = frappe.db.get_list("SaaS sites",filters={'domain':sitename + "."+domain},ignore_permissions=True)
    print(site)
    if(len(site) > 0):
        return "yes"
    else:
        return "no"
    
    
    
class SaaSsites(Document):
	pass
