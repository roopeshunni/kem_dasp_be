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
import datetime
from .constants import *
#======================================================#
# function for checking applicant already exist or not #
#======================================================#

def check_applicant(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('batchid') and data.get('userid') and data.get('prgid'):
            v8 = Batch.objects.filter(batch_id=data.get('batchid'))
            if(len(v8)==0):
                return JsonResponse({"status":200,"message":"Invalid batch id"})
            v7=Programme.objects.filter(program_id=data.get('prgid'))
            if(len(v7)==0):
                return JsonResponse({"status": 200,'message':'Invalid Programmeid '},safe=False)

            batchobj = StudentApplicants.objects.filter(program_id_id=data.get('prgid'),user_id=data.get('userid'),batch_id_id=data.get('batchid')).exclude(applicant_status="canceled")
            # otherbatchobj = StudentApplicants.objects.filter(user_id=data.get('userid')).exclude(applicant_status="canceled")
            # print(otherbatchobj)
            if batchobj.count()!=0:
                return JsonResponse({"status":200,"message":"Already Applied"},safe=False)
            # elif otherbatchobj.count()!=0:
            #     return JsonResponse({"status":200,"message":"You are already applied for a programme if you want to apply for another one please cancel your previous application"},safe=False)
            else:
                return JsonResponse({"status":200,"message":"Not Applied"},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
       
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)

