from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import *
from django.http import JsonResponse
import datetime
from .constants import *

# ==================================#
#  function for get all highlights  #
# ==================================#
def get_all_highlights():
	try:
		highlightsData = Highlights.objects.all()
		list1=[]
		for i in highlightsData:
			dict1={"highlights_id":i.highlights_id,"decription":i.description}
			list1.append(dict1)
		return {"status":200,"message":list1}
	except Exception as e:
		# err={"status":500,"message":"Internal Server Error"}
		return internalServer
