#!/usr/bin/python
# -*- coding: utf8 -*-

from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from django.template import RequestContext
from django.contrib import auth

import pymongo
from pymongo import MongoClient

def logout(request):
	auth.logout(request)
	return redirect("/login/")

def base_view(request, database='shoppr_usercontent_db', collection='shoppr_backend_db', page_number=1, preset='local'):
	args = {}
	current_preset = None
	if request.user.is_authenticated():
		client1 = MongoClient()
		db = client1['dashboard']
		presets = db.presets
		pres = presets.find_one({'name':preset})
		preset_host = pres['host']
		preset_port = int(pres['port'])
		preset_name = pres['name']
		args['preset'] = preset
		args['username'] = request.POST.get("username", "")
		args['page_number'] = page_number
		args['database'] = database
		preset_username = pres['login']
		preset_password = pres['password']
		client = MongoClient(preset_host, preset_port)
		args['db_user'] = preset_username
		args['databases'] = ['shoppr_backend_db', 'shoppr_usercontent_db']
		#[i for i in client.database_names() if i not in ['test', 'dashboard', 'local', 'admin']]
		args['login'] = preset_username
		db = client[database]
		if preset_username!='' and preset_password!='':
			try:
				db.authenticate(preset_username, preset_password)
			except Exception as e:
				return redirect('/')
		collections_count=0
		col = db[collection]
		collections = []
		try:
			name_collections = db.collection_names(include_system_collections=False)
			args['collection'] = collection
			for el in name_collections:
				tmp = {}
				tmp['name'] = el
				tmp['kol'] = db.get_collection(el).count()
				collections.append(tmp)
			args['collections'] = collections
		except Exception as e:
			return redirect('/')
		if collections_count>0:
			args['count_documents'] = int(col.count())
			args['pagination_first_element'] = 1
			args['pagination_last_element'] = int(args['count_documents'])/10+1 if int(args['count_documents'])%10>=1 else int(args['count_documents'])/10
			args['pagination_next_element'] = args['pagination_last_element'] if int(page_number)+1 >= args['pagination_last_element'] else int(page_number)+1
			args['pagination_previous_element'] = args['pagination_first_element'] if int(page_number)-1 <= args['pagination_first_element'] else int(page_number)-1
		if request.POST.get("search_key", ""):
			search_key = request.POST.get("search_key", "")
			search_value = request.POST.get("search_value", "")
			if search_value.isdigit():
				search_value = int(search_value)
			else:
				args['search_value'] = search_value
			args['search_key'] = search_key
			args['documents'] = db[args['collection']].find({search_key: search_value})
			args['documents2'] = db[args['collection']].find_one({search_key: search_value})
		else:
			args['documents'] = col.find().skip(int(page_number)*10-10).limit(10)
			args['documents2'] = col.find_one()
		return render_to_response('list_documents.html', args, context_instance=RequestContext(request))
	else:
		args={}
		args.update(csrf(request))
		username = request.POST.get("username", "")
		if username:
			password = request.POST.get("password", "")
			user = auth.authenticate(username=username, password=password)
			if user is not None:
				auth.login(request, user)
				args['username'] = username
				args['password'] = password
				return redirect('/configuration/')
			else:
				args['login_error'] = "User not found"
				return render_to_response('login.html', args)
		else:
			return render_to_response('login.html', args)