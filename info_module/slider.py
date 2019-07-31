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


# =======================================#
#  function for get all slider images    #
# =======================================#

def get_slider_all():
    try:
        queryset=Slider.objects.all()
        singlecountryDict1=[]
        for i in queryset:
            singlecountryDict = {"id" : i.slider_id,"title" : i.title,"Description":i.description,"Image":i.image}
            singlecountryDict1.append(singlecountryDict)
        return {"status":200,"message":singlecountryDict1}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer   