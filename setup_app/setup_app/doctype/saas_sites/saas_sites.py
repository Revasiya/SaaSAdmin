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

    command = " ; ".join(commands)
    print("executing ",command)
    process = sp.Popen(command,shell=True,stdout=log)
    process.wait()
    os.system('sudo service nginx reload')
    print(process.returncode)
    
@frappe.whitelist()    
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
    stock_sites = frappe.db.get_list("SaaS stock sites",filters={'isused':"no"})
    target_site = frappe.get_doc("SaaS stock sites",stock_sites[0]["name"])
    print("using ",target_site.subdomain,"to create ",subdomain)
    commands = []
    current_site = subdomain + '.' + domain
    print(target_site.subdomain + '.' + domain )
    commands.append('export SITE_{}_STATUS=creating'.format(current_site).replace('.','M'))
    commands.append('bench --site {} set-admin-password {}'.format(target_site.subdomain + '.' + domain ,admin_password))
    commands.append('bench setup add-domain {} --site {}'.format(current_site,target_site.subdomain + '.' + domain))
    target_site.isused = 'yes'
    print("s",target_site)
    target_site.save()
    commands.append('bench setup nginx --yes')
    commands.append('echo {} | sudo service nginx reload'.format(config.root_password))
    commands.append('export SITE_{}_STATUS=done'.format(current_site).replace('.','M'))
    commands.append('export madarchod=1')
    executeCommands(commands)
    new_site = frappe.new_doc("SaaS sites")
    new_site.password = admin_password
    new_site.first_name = fname
    new_site.lname = lname
    new_site.company_name = company_name
    new_site.email = email
    new_site.domain = current_site
    new_site.save()
    frappe.msgprint(msg='Site {} has been created'.format(current_site))
    return True

class SaaSsites(Document):
	pass
