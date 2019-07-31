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


#==============================================#
#    function for get an Announcement details #
#==============================================#
def get_single_announcement(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1) 
        if data.get('anid'):
            announce_id = data.get('anid')
            queryset = Announcement.objects.filter(announcements_id=announce_id)
            if queryset.count()==0:
                return JsonResponse({"status":404,"message":"Invalid announcement id"})
            singlecountryDict1=[]
            for i in queryset:
                singlecountryDict = {"id" : i.announcements_id,"title" : i.title,"Description":i.description}
                singlecountryDict1.append(singlecountryDict)
            return JsonResponse({"status":200,"message":singlecountryDict1},safe=False)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer
#==============================================#
#    function for get all Announcements        #
#==============================================#
def get_all_announcement():
    try:
        queryset=Announcement.objects.all()
        singlecountryDict1=[]
        for i in queryset:
            singlecountryDict = {"id" : i.announcements_id,"title" : i.title,"Description":i.description}
            singlecountryDict1.append(singlecountryDict)
        return {"status":200,"message":singlecountryDict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer 