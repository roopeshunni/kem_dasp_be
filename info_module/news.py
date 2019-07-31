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

class NewAll(APIView):
    #==========================================#
    #     function for get all News details  #
    #==========================================#
    def get(self, request,format=None):
        try:
            queryset=News.objects.all()
            singlecountryDict1=[]
            for i in queryset:
                singlecountryDict = {"id" : i.news_id,"title" : i.title,"Description":i.description,"Image":i.image}
                singlecountryDict1.append(singlecountryDict)
            return JsonResponse({"status":200,"message":singlecountryDict1},safe=False)
        except Exception as e:
            # err={"status":500,"message":"Internal Server Error"}
            return internalServer

class NewsOne(APIView):
    #==========================================#
    #     function for get a News details  #
    #==========================================#
    def get(self,request,format=None):
        try:
            # news_id=request.data.get('1')
            queryset=News.objects.filter(news_id=1)
            newsDict1=[]
            for i in queryset:    
                newsDict = {"id" : i.news_id,"title":i.title,"description":i.description,"image":i.image}
                newsDict1.append(newsDict)
            return JsonResponse({"status":200,"message":newsDict1},safe=False)
        except Exception as e:
            # err={"status":500,"message":"Internal Server Error"}
            return internalServer    