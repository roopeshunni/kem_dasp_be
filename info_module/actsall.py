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

#====================================================#
# function for get all acts and regulations details  #
#====================================================#
def get_all_act():
    try:
        queryset=ActsAndRegulation.objects.all()
        singlecountryDict1=[]
        for i in queryset:
            singlecountryDict = {"id" : i.news_id,"title" : i.title,"Description":i.description,"Image":i.image}
            singlecountryDict1.append(singlecountryDict)
        return {"status":200,"message":singlecountryDict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer
#=======================================================#
# function for get single acts and regulations details  #
#=======================================================#
def get_single_act(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('actid'):
            act_id = data.get('actid')
            queryset = ActsAndRegulation.objects.filter(act_id=act_id)
            if queryset.count()==0:
                return JsonResponse({"status":404,"message":"Invalid act id"},safe=False)
            else:
                singlecountryDict1=[]
                for i in queryset:
                    singlecountryDict = {"id" : i.act_id,"title" : i.title,"description":i.description,"Document":i.document}
                    singlecountryDict1.append(singlecountryDict)
                return JsonResponse({"status":200,"message":singlecountryDict1},safe=False)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)    