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
#========================================================#
# function for  check selected applicant count 
# according to the admission slot seat capacity, 
# Change status of the selected applicants to "selected" #
#========================================================#
def selected_applicant(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('batch_id') and data.get('userlist'):

            batchobj = Batch.objects.get(batch_id=data.get('batch_id'))
           
            for i in data.get('userlist'):                 
                student_applicantobj = StudentApplicants.objects.get(batch_id_id=data.get('batch_id'),user_id=i)
                student_applicantobj.applicant_status="selected"
                student_applicantobj.save()
            prgmobj=Programme.objects.get(program_id=batchobj.program_id_id)
            data={"p_fee":batchobj.program_fee,"p_code":prgmobj.program_code}
            return JsonResponse({"status":200,"message":"successfully changed applicant status","data":data}) 
        else:
            return JsonResponse(error,safe=False) 
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)


def student_check(received_json_data):
    try:
        received_data=json.dumps(received_json_data)
        data=json.loads(received_data)
        if data.get('user_id'):
            user_id=data.get('user_id')
            student_applicantobj = StudentApplicants.objects.filter(user_id=user_id,applicant_status="student")
            print(student_applicantobj)
            if student_applicantobj.count()>0:
                print(True)
                return True
            else:
                return False

    except Exception as e:
        print(e)
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)



