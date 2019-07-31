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
from .directorate import *
from .constants import *
#================================#
#function for get a studycentre  #
#================================#

def get_a_studycentre(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('id'):
            stud_id=data.get('id')
            queryset=studycentre.objects.filter(studycentre_id=stud_id)
            if queryset.count()==0:
                return JsonResponse({"status":404,"message":"Invalid studycentre id"},safe=False)
            else:
                studycentreDict1=[]
                for i in queryset:
                    studycentreDict = {"id" : i.studycentre_id,"centre_name" : i.name,"centre_address":i.address,"phone_number":i.phone,"glocation":i.location,"managed_by":i.managed_by}
                    studycentreDict1.append(studycentreDict)
                return JsonResponse({"status":200,"message":studycentreDict1},safe=False)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)
    
#================================#
#function for get all studycentre#
#================================#

def get_all_studycentre():
    try:
        queryset=studycentre.objects.all()
        studycentreDict1=[]
        for i in queryset:
            studycentreDict = {"id" : i.studycentre_id,"centre_name" : i.name,"centre_address":i.address,"phone_number":i.phone,"glocation":i.location,"managed_by":i.managed_by}
            studycentreDict1.append(studycentreDict)
        return {"status":200,"message":studycentreDict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer