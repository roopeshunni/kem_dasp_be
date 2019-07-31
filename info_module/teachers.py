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
#===============================================================#
#     function for fetching batch details alloted  for teacher  #
#===============================================================#
def teacher_batch_details(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('batch_id'):
            batch_id = data.get('batch_id')
            data=[]
            for i in batch_id:
                queryset1 =Batch.objects.filter(batch_id=i)
                if queryset1.count()==0:
                    continue
                else:
                    for i in queryset1:
                        dict1={"b_id":i.batch_id,"name":i.batch_name,"status":i.status}
                        data.append(dict1)
            return JsonResponse({"status":200,"message":data},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)

#===============================================================#
#     function for fetching course details alloted  for teacher #
#===============================================================#
def teacher_course_details(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('course_id'):
            course_id = data.get('course_id')
            data=[]
            for i in course_id:
                queryset1 =Course_programme_mapping.objects.filter(course_prg_id=i)
                if queryset1.count()==0:
                    continue
                else:
                    for cour in queryset1:
                        courseobj =Course.objects.filter(course_id=cour.course_id_id)
                        for c in courseobj:
                            dict1={"course_mapping_id":i,"course_id":c.course_id,"code":c.course_code,
                            "name":c.course_name,"credit":c.credit,"imark":c.internal_mark,
                            "emark":c.external_mark,"tmark":c.total_mark}
                            data.append(dict1)
            return JsonResponse({"status":200,"message":data},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)	



