#!/usr/bin/python
# -*- coding: utf8 -*-

from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext

import pymongo
from pymongo import MongoClient

#paginator
from django.core.paginator import Paginator


def base_view(request, database='shoppr_backend_db', collection='Crawler_user', page_number=1):
	args = {}
	client = MongoClient()
	db = client[database]
	col = db[collection]
	name_collections = db.collection_names()
	collections = []
	args['collection'] = collection
	for el in name_collections:
		tmp = {}
		tmp['name'] = el
		tmp['kol'] = db.get_collection(el).count()
		collections.append(tmp)
	args['collections'] = collections
	args['count_documents'] = col.count()
	#args['pagination_elements'] = [x+1 for x in range(int(args['count_documents'])/10+1)]
	args['pagination_first_element'] = 1
	args['page_number'] = page_number
	args['pagination_last_element'] = int(args['count_documents'])/10+1 if int(args['count_documents'])%10>=1 else int(args['count_documents'])/10 #args['pagination_elements'][-1]
	args['pagination_next_element'] = args['pagination_last_element'] if int(page_number)+1 >= args['pagination_last_element'] else int(page_number)+1
	args['pagination_previous_element'] = args['pagination_first_element'] if int(page_number)-1 <= args['pagination_first_element'] else int(page_number)-1
	
	if request.POST:
		search_key = request.POST.get("search_key", "")
		search_value = request.POST.get("search_value", "")
		if search_value.isdigit():
			search_value = int(search_value)
		else:
			args['search_value'] = search_value
		args['search_key'] = search_key
		#args['collection'] = request.POST.get("collection", "")
		#rabotaet i bez etoy stroki
		args['documents'] = db[args['collection']].find({search_key: search_value})
	else:
		args['documents'] = col.find().skip(int(page_number)*10-10).limit(10)
	return render_to_response('main.html', args, context_instance=RequestContext(request))
