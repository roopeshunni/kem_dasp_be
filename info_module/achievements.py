from django.shortcuts import render
from .models import *
# Create your views here.
from django.http import HttpResponse,JsonResponse
import requests 
import json
from .constants import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from urllib.parse import parse_qs


#============================================#
# function for get all Achievements details  #
#============================================#
def get_all_achievements():
    try:
        queryset=achievements.objects.all()
        achievementsDict1=[]
        for i in queryset:
            achievementsDict = {"id" : i.achievement_id,"title" : i.title,"desc":i.description,"image":i.picture}
            achievementsDict1.append(achievementsDict)
        return {"status":200,"message":achievementsDict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer
#============================================#
# function for get an Achievements details  #
#============================================#
def get_single_achievement(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('aid'):
            a_id=data.get('aid')
            queryset=achievements.objects.filter(achievement_id=a_id)
            if queryset.count()==0:
                return JsonResponse({"status":404,"message":"Invalid achievement id"})
            achievementsDict1=[]
            for i in queryset:
                achievementsDict = {"id" : i.achievement_id,"title" : i.title,"desc":i.description,"image":i.picture}
                achievementsDict1.append(achievementsDict)
            return JsonResponse({"status":200,"message":achievementsDict1})
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)
