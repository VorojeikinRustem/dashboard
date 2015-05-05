#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django import template
import urlparse

register = template.Library()

@register.filter
def dict_field(value):
	rez=""
	if isinstance(value, dict):
		for k in value.keys():
			key = value.get(k)
			if isinstance(key, list):
				rez += "<div class='dict_list'>LIST:<span class='dict_list_key'>" + k + "</span>: <div class='next_dict'>"
				for k_dict in key:
					rez += k_dict + "; "
				rez += "</div></div>"
			elif isinstance(key, dict):
				rez += "<div class='dict_dict'>DICT: <span class='dict_dict_list_key'>" + k + "</span>: <div>"
				for k_dict in key.keys():
					v_dict = key.get(k_dict)
					rez += "<span class='dict_dict_list_dict_key'>" + k_dict + ": </span> " + str(v_dict) + "; "
				rez += "</div></div>"
			else:
				#FIX BUG LATTER (Crawler_productdescription on Last page, UnicodeEncodeError)
				rez += "<div>STR:<span class='dict_str_key'>"+ u'%s' % str(k) + "</span>: " + u'%s' % str(key) + "</div>"
				#repr(i).decode('unicode_escape')
		return rez
	else:
		return value
	

#  margin-left:15px;