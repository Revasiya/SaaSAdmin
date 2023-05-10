# Copyright (c) 2023, OneHash and contributors
# For license information, please see license.txt
import sys
sys.path.append('../saas_stock_sites')
import frappe
import os
import subprocess as sp
from time import sleep
from frappe.model.document import Document
domain = 'localhost'
def executeCommands(commands):
    command = " & ".join(commands)
    print("executing ",command)
    process = sp.Popen(command,shell=True,stdout=sp.PIPE)
    print("waiting")
    process.wait()
    print("waiting done")
    print(process.returncode)
def checkifDone(site,time=0):
    print(site)
    if(time > 50):
        exit(1)
    status = sp.getoutput('echo $SITE_{}_STATUS'.format(site).replace('.','M'))
    print(status)
    print(sp.getoutput('echo $madarchod'))
    if status == 'done':
        return 1
    else :
        sleep(10)
        checkifDone(site,time+10)
    
    
def setupSite(subdomain,admin_password,fname,lname,company_name,email):
    config = frappe.get_doc("SaaS settings")
    # find a stock site not used
    stock_sites = frappe.db.get_list("SaaS stock sites",filters={'isused':"no"})
    target_site = frappe.get_doc("SaaS stock sites",stock_sites[0]["name"])
    print("using ",target_site.subdomain,"crating",subdomain)
    commands = []
  #  commands.append('mv sites/{} sites/{}'.format(target_site.subdomain + '.' + domain,subdomain + '.' + domain))
    current_site = subdomain + '.' + domain
    print(target_site.subdomain + '.' + domain )
    commands.append('export SITE_{}_STATUS=creating'.format(current_site).replace('.','M'))
    commands.append('bench --site {} set-admin-password {}'.format(target_site.subdomain + '.' + domain ,admin_password))
    commands.append('bench setup add-domain {} --site {}'.format(current_site,target_site.subdomain + '.' + domain))
    target_site.isused = 'yes'
    print("s",target_site)
    target_site.save()
   # commands.append('echo -y | -S bench setup nginx ')
    #commands.append('echo 861756 | sudo -S service nginx reload')
    commands.append('export SITE_{}_STATUS=done'.format(current_site).replace('.','M'))
    commands.append('export madarchod=1')
    executeCommands(commands)
   # checkifDone(current_site)
    new_site = frappe.new_doc("SaaS sites")
    new_site.password = admin_password
    new_site.first_name = fname
    new_site.lname = lname
    new_site.company_name = company_name
    new_site.email = email
    new_site.domain = current_site
    new_site.save()
    print("created",current_site)
    return True

class SaaSsites(Document):
	pass
