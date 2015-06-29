# coding: utf-8
import os
from fabric.api import env, run, cd, local

env.forward_agent = True

def dump(host, port, user='', pwd=''):
	if user!='' and pwd!='':
		local("mongodump -h %s:%s -d shoppr_backend_db -u %s -p %s --excludeCollectionsWithPrefix system --out /home/ubuntu/dump" % (host, port, user, pwd))
		local("mongodump -h %s:%s -d shoppr_usercontent_db -u %s -p %s --excludeCollectionsWithPrefix system --out /home/ubuntu/dump" % (host, port, user, pwd))
	else:
		local("mongodump -h %s:%s -d shoppr_backend_db --excludeCollectionsWithPrefix system --out /home/ubuntu/dump" % (host, port))
		local("mongodump -h %s:%s -d shoppr_usercontent_db --excludeCollectionsWithPrefix system --out /home/ubuntu/dump" % (host, port))

def restore(host, port, user='', pwd=''):
	if user!='' and pwd!='':
		local("mongorestore -h %s:%s -d shoppr_backend_db -u %s -p %s /home/ubuntu/dump/shoppr_backend_db/" % (host, port, user, pwd))
		local("mongorestore -h %s:%s -d shoppr_usercontent_db -u %s -p %s /home/ubuntu/dump/shoppr_usercontent_db/" % (host, port, user, pwd))
	else:
		local("mongorestore -h %s:%s -d shoppr_backend_db /home/ubuntu/dump/shoppr_backend_db/" % (host, port))
		local("mongorestore -h %s:%s -d shoppr_usercontent_db /home/ubuntu/dump/shoppr_usercontent_db/" % (host, port))
