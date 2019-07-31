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
class GalleryAll(APIView):
    #=================================#
    #   function for get all images   #
    #=================================#
    def get(self, request,format=None):
        try:
            queryset=images.objects.all()
            imgDict1=[]
            for i in queryset:    
                title_id=i.title_id_id
                titleobj=gallerytitle.objects.get(title_id=title_id)
                imgDict = {"id" : i.image_id,"desc":i.photo,"date":i.date,"thumb":i.thumbnail,"title":titleobj.title}
                imgDict1.append(imgDict)
            return JsonResponse({"status":200,"message":imgDict1},safe=False)
        except Exception as e:
            # err={"status":500,"message":"Internal Server Error"}
            return internalServer 
    def post(self, request,format=None):
        try:
            if request.data.get('imageid'):
                imgid=request.data.get('imageid')# img_id=request.data.get('1')
                queryset=images.objects.filter(image_id=imgid)
                imgDict1=[]
                for i in queryset:    
                    title_id=i.title_id_id
                    titleobj=gallerytitle.objects.get(title_id=title_id)
                    imgDict = {"id" : i.image_id,"desc":i.photo,"date":i.date,"thumb":i.thumbnail,"title":titleobj.title}
                    imgDict1.append(imgDict)
                return JsonResponse({"status":200,"message":imgDict1},safe=False)
        except Exception as e:
            # err={"status":500,"message":"Internal Server Error"}
            return internalServer 