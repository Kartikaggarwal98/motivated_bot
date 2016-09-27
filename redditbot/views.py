#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import re
from bs4 import BeautifulSoup as BS
import random
# Create your views here.
def index(request):
	print "@@@@"
	output_text="HELLO"
	quote_list,image_list=motivate()
	print quote_list[0],"\n",image_list[0]
	random.shuffle(quote_list)
	random.shuffle(image_list)
	output_text=quote_list[0]+"\n" +image_list[0]
	#output_text="quote"+str(len(quote_list))+"image"+str(len(image_list))

	return HttpResponse(output_text,content_type='application/json')

def motivate(): 
	url="https://www.reddit.com/r/GetMotivated/new/"
	f=requests.get(url)
	soup=BS(f.text)

	print "hello"

	image_list=[]
	quote_list=[]

	div_table=soup.find_all('div',{'class':"sitetable linklisting"})

	if len(div_table)==0:
		return motivate()
	else:
		div=div_table[0].find_all('div',{'data-subreddit':"GetMotivated"})

		for ix in div:
			try:
				thumbnail=ix.get('data-url')
			except Exception:
				pass

			quote=ix.find_all('div',class_="entry unvoted")[0].find_all('a')[0].text

			if '[Image]' in quote:
				image_list.append(thumbnail)
			elif '[Text]' in quote:
				quote_list.append(quote[7:])
			else:
				pass
		print quote_list[0]," ",image_list[0]
		print "________"
		return (quote_list,image_list)


def post_facebook_message(sender_id,message):
	post_message_url= 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN

def logg(message,symbol='-'):
	print '%s\n %s \n%s'%(symbol*10,message,symbol*10)

class RedditBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('OOPS INVALID TOKEN')
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		incoming_message=json.loads(self.request.body.decode('utf-8'))

		logg(incoming_message)

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				try:
					sender_id=message['sender']['id']
					message_text=message['message']['text']
					post_facebook_message(sender_id,message_text)
				except Exception as e:
					logg(e,symbol='-199-')

		return HttpResponse