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
import datetime
from django.db.models import Subquery
from django.db.models import Count
from .constants import *
#=====================================================#
# function for fetching admission started programmes  #
#=====================================================#
def get_admission_programmes():
    try:
        pgmobj=Programme.objects.filter(program_id__in=Subquery(Batch.objects.filter(status="admission").values('program_id'))).values('program_id','program_code','title')
        programmes=[]
        for j in pgmobj:
            programdict={"prgmid":j['program_id'],"programcode":j['program_code'],"programname":j['title']}
            programmes.append(programdict)
        return {"status":200,"message":programmes}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer
#=======================================================================#
# function for fetching admission started batch details of a programme  #
#=======================================================================#
def get_admission_pgm_batch(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('pid'):
            program_id = data.get('pid')
            batchpgmData = Batch.objects.filter(program_id=program_id,status="admission").values('batch_name','batch_id','no_of_seats','appli_start_date','appli_end_date','prgm_start_date','prgm_end_date','program_fee')
            batches=[]
            for i in batchpgmData:
                querysets=StudentApplicants.objects.filter(batch_id_id=i['batch_id'])
                totalapplicants=0
                no_students=querysets.count()
                totalapplicants=totalapplicants+no_students 
                batchdict={"batchid":i['batch_id'],"batchname":i['batch_name'],"no_seats":i['no_of_seats'],
                "appstart":str(i['appli_start_date']),"append":str(i['appli_end_date']),
                "prgstart":str(i['prgm_start_date']),"prgend":str(i['prgm_end_date']),
                "prgfees":i['program_fee'],"applicantcount":totalapplicants}
                batches.append(batchdict)
            msg={"batches":batches}
        return JsonResponse({"status":200,"message":msg})
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer