from django.shortcuts import render
from .models import *
# Create your views here.
from django.http import HttpResponse,JsonResponse
import requests 
import json
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from urllib.parse import parse_qs
from .constants import *
#================================#
#function for get all directorate#
#================================#

def get_directorate():
    try:
        queryset=directorate.objects.all()
        directorateDict1=[]
        for i in queryset:
            directorateDict = {"id" : i.directorate_id,"directorate_name" : i.name,"directorate_address":i.address,"phone_number":i.phone,"email_id":i.email,"fax_number":i.fax,"title":i.title,"description":i.description,"caption":i.caption,"image":i.logo}
            directorateDict1.append(directorateDict)
            msg={"status":200,"message":directorateDict1}
        return msg
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer