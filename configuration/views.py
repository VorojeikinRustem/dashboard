from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib import auth

from pymongo import MongoClient
from fabfile import *

def presets(request, preset='local'):
	args={}
	client = MongoClient()
	db = client['dashboard']
	presets_col = db.presets
	presets = list(presets_col.find())
	args['presets_read'] = list(db.presets.find({'$or': [{'role': 'read'}, {'role': 'readWrite'}]}))
	args['presets_readWrite'] = list(db.presets.find({'role': 'readWrite'}))
	args['presets'] = presets
	args['preset'] = preset
	#Current preset
	pres = presets_col.find_one({'name':preset})
	args['cur_username'] = pres['login']
	args['cur_preset'] = pres['name']
	args['cur_host'] = pres['host']
	args['cur_port'] = pres['port']
	args['cur_password'] = pres['password']
	args['cur_role'] = pres['role']
	if request.POST.get("group2", ""):
		#Group1(from)
		group1 = request.POST.get("group1", "")
		host_group1 = presets_col.find_one({'name': group1})['host']
		port_group1 = int(presets_col.find_one({'name': group1})['port'])
		login_group1 = presets_col.find_one({'name': group1})['login']
		password_group1 = presets_col.find_one({'name': group1})['password']
		#Group2(to)
		group2 = request.POST.get("group2", "")
		host_group2 = presets_col.find_one({'name': group2})['host']
		port_group2 = int(presets_col.find_one({'name': group2})['port'])
		login_group2 = presets_col.find_one({'name': group2})['login']
		password_group2 = presets_col.find_one({'name': group2})['password']
		#mongodump
		if login_group1!='' and password_group1!='':
			dump(host_group1, port_group1, login_group1, password_group1)
		else:
			dump(host_group1, port_group1)
		#mongorestore
		if login_group2!='' and password_group2!='':
			restore(host_group2, port_group2, login_group2, password_group2)
		else:
			restore(host_group2, port_group2)
		args['dbs_copy_complete'] = True
	if request.user.is_authenticated():
		return render_to_response('configuration.html', args, context_instance=RequestContext(request))
	else:
		return render_to_response('login.html', args, context_instance=RequestContext(request))

#removed
def change_data(request):
	if request.POST:
		username = request.POST.get("username", "")
		new_password = request.POST.get("password", "")
		u = User.objects.get(username__exact=username)
		u.set_password(new_password)
		u.save()
		auth.logout(request)
	return render_to_response('login.html', {})

def add(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		client = MongoClient()
		db = client['dashboard']
		db.presets.insert({
			'name':request.POST.get("name",""),
			'login':request.POST.get("username",""),
			'password':request.POST.get("password",""),
			'host':request.POST.get("host",""),
			'port':request.POST.get("port",""),
			'role':request.POST.get("role","")
			})
	return redirect('/', context_instance=RequestContext(request))

def delete(request):
	args = {}
	if request.POST.get("del", ""):
		args.update(csrf(request))
		delete = request.POST.get("del", "")
		client = MongoClient()
		db = client['dashboard']
		presets_col = db.presets
		presets_col.delete_one({'name':delete})
	return redirect('/')
