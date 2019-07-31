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

#=======================================#
# function for add about us   details   #
#=======================================#

def about_add(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('desc'):
            desc=data.get('desc')
            description=desc.replace(' ','')
            if len(description)==0:
                return JsonResponse({"status":404,"message":"Invalid data in description"},safe=False) 
            else:
                x=aboutus(description=desc)
                x.save()
                return JsonResponse({"status":200,"message":"Successfully added aboutus details"},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)
#=======================================#
# function for edit  department details #
#=======================================#
def about_edit(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('abt_id') and data.get('desc'):
            aid=data.get('abt_id')
            desc=data.get('desc')
            description=desc.replace(' ','')
            if len(description)==0:
                return JsonResponse({"status":404,"message":"Invalid data in description"},safe=False)
            else:
                abtobj = aboutus.objects.filter(aboutus_id=aid)
                if abtobj.count()==0:
                    return JsonResponse({"status":404,"message":"Invalid aboutus id"},safe=False)
                else:
                    for i in abtobj:
                        i.description=desc
                        i.save()
                        return JsonResponse({"status":200,"message":"successfully edited aboutus details"},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)
# =================================#
#  function for get a department   #
# =================================#

def get_about(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('abt_id'):
            aid = data.get('abt_id')
            abtobj = aboutus.objects.filter(aboutus_id=aid)
            if abtobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid aboutus id"},safe=False)
            else:
                datalist=[]
                for i in abtobj:
                    dict1={"id":i.aboutus_id,"desc":i.description}
                    datalist.append(dict1)
                return JsonResponse({"status":200,"message":datalist},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)

#=================================#
#function for get all achievements#
#=================================#
def get_all_about():
    try:
        queryset=aboutus.objects.all()
        aboutusDict1=[]
        for i in queryset:
            aboutusDict = {"id" : i.aboutus_id,"desc":i.description}
            aboutusDict1.append(aboutusDict)
        return {"status":200,"message":aboutusDict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer 