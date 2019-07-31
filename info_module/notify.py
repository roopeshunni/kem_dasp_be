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
#====================================#
# function for get all notifications #
#====================================#
def get_all_notification():
    try:
        queryset=Notify.objects.filter(notify_status="active")
        notifydict1=[]
        for i in queryset:
            notifyDict = {"id" : i.notify_id,"title" : i.notify_title,"status":i.notify_status}
            notifydict1.append(notifyDict)
            # print(type(i.notify_status))
        return {"status":200,"message":notifydict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer    