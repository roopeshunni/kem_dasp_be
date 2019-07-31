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
#======================================================#
#  function for get all Research Publications details  #
#======================================================#
def get_all_research():
    try:
        queryset=ResearchPublication.objects.all()
        singlecountryDict1=[]
        for i in queryset:
            singlecountryDict = {"id" : i.research_id,"title" : i.title,
            "Author":i.author,"Guide":i.guide,"Summary":i.synopsis,
            "Documents":i.research_documents}
            singlecountryDict1.append(singlecountryDict)
        return {"status":200,"message":singlecountryDict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer 
#=========================================================#
#  function for get single Research Publications details  #
#=========================================================#
def single_research(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('rid'):
            research_id = data.get('rid')
            queryset = ResearchPublication.objects.filter(research_id=research_id)
            if abtobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid research id"},safe=False)
            else:
                singlecountryDict1=[]
                for i in queryset:
                    singlecountryDict = {"id" : i.research_id,"title" : i.title,"author":i.author,"guide":i.guide,"synopsis":i.synopsis,"Document":i.research_documents}
                    singlecountryDict1.append(singlecountryDict)
                return JsonResponse({"status":200,"message":singlecountryDict1},safe=False)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer) 
