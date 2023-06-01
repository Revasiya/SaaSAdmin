# Copyright (c) 2023, OneHash and contributors
# For license information, please see license.txt
import sys
import json
sys.path.append('../saas_stock_sites')
import frappe
import os
import time
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
        commands.append("bench new-site {} --install-app erpnext  --admin-password {} --db-root-password {}".format(subdomain + '.'+domain,admin_password,config.db_password))
        commands.append("bench --site {} install-app clientside".format(subdomain + '.'+domain))
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
    print("creating the first user")
    sub = subdomain 
    if domain == 'localhost':
        sub = target_site.subdomain
    print(sub)
    resp = create_first_user_on_site(email,admin_password,sub,fname,lname)
    if resp :
        print("first user created")
    else:
        print("first user not created")
        
    return target_site.subdomain
@frappe.whitelist(allow_guest=True)  
def create_first_user_on_site(email,password,subdomain,firstname,lastname):
    retry_count = 1
    conn=""
    user=None
    url = ""
    if domain == 'localhost':
        url = "http://"+subdomain+"."+domain+":8000"
    else :
        url = "https://"+subdomain+"."+domain
    from setup_app.setup_app.doctype.saas_sites.frappeclient import FrappeClient
    print(url)
    while(conn==""):
        try:
            conn = FrappeClient(url)
            conn.login("Administrator",password)
            
        except Exception as e:
            print("Exception in connection to site:")
            print(e)
            print("Connection Object")
            print(conn)
            print(str(retry_count)+" Retry to Connect:")
            retry_count = retry_count+1
            time.sleep(2)
        if(retry_count>3):
            break			
    
    if(retry_count>3):
        return False
    try:
        user = conn.get_list("User",filters={"email":email})
        if(len(user)==0):
            user = False
    except Exception as e:
        print(e)	
        pass
    if(not user):
            conn.insert({
        "doctype": "User",
        "first_name": firstname,
        "last_name":lastname,
        "email": email,
        "send_welcome_email":0,	
        "new_password":password,
        "enabled":1
        })
    user = conn.get_doc("User",email)
    role_list = conn.get_list("Role",['name'],limit_page_length=1000,filters = [['Role','name','not in',["Administrator", "Guest", "All", "Customer", "Supplier", "Partner", "Employee"]]])
    for role in role_list:
        user['roles'].append({"role":role['name']})
    conn.update(user)
    return user
    
    
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
    
@frappe.whitelist(allow_guest=True)
def checkConnection():
    #q4frq3
    from better_saas.better_saas.doctype.saas_user.frappeclient import FrappeClient
    url = "http://q4frq3.localhost:8000"
    conn = FrappeClient(url)
    conn.login("Administrator","12345678")
    print(conn)
    
class SaaSsites(Document):
    pass
