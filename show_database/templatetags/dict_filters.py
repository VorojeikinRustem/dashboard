#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
from django import template
reload(sys)
sys.setdefaultencoding('utf8')

register = template.Library()

@register.filter
def dict_field(value):
	rez="<i class='icon-circle-arrow-down'></i></p></div><div class='show-dict-item'>"
	if isinstance(value, dict):
		for k in value.keys():
			key = value.get(k)
			if isinstance(key, list):
				rez += "<p class='str-list'><span class='text-error'>" + k + "</span>: </p>"
				i=0
				for k_dict in key:
					rez += "<p class='str-list-item'><span class='text-error'>[" + str(i) + "]</span>: <span  class='text-success'>" + k_dict + "</span></p>"
					i+=1
			elif isinstance(key, dict):
				rez += "<p class='str-list'><span class='text-error'>" + k + "</span>: </p>"
				for k_dict in key.keys():
					v_dict = key.get(k_dict)
					rez += "<p class='str-list-item'><span class='text-error'>" + k_dict + "</span> :<span class='text-success'>" + str(v_dict) + "</span></p>"
			else:
				rez += "<p class='str-list'><span class='text-error'>"+ u'%s' % str(k) + "</span>: <span class='text-success'>" + u'%s' % str(key) + "</span></p>"
		return rez+"</div>"
	else:
		return "<span class='text-success'>" + unicode(value) + "</span></p></div>"
