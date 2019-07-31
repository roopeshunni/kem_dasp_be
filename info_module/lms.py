from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import *
from django.http import JsonResponse
import datetime
from .constants import *
import requests
import json
import re


# =========================================================================#
#  function for get all course details and batch details nunder a program  #
# =========================================================================#


def get_all_teacher_prg_courses(received_json_data):
    try:
        data1 =json.dumps(received_json_data)
        data = json.loads(data1)
        datas = []
        for i in data:
            if i.get('batch_id') and i.get('course_id') and i.get('teacher_id'):
                queryset = Batch.objects.select_related('program_id').values(
                    'batch_id', 'batch_name', 'program_id', 'program_id__title').filter(batch_id=i.get('batch_id'))
                if queryset.count() == 0:
                    return JsonResponse({"success":False, "message": "There is no batch exist","data":{}}, safe=False)
                else:
                    for x in queryset:
                        courseDet= Course_programme_mapping.objects.get(
                        course_prg_id=i.get('course_id'))
                        
                        resultDic = {"batchId": x.get('batch_id'), "batchName": x.get('batch_name'),"programId": x.get('program_id'), "prgrammeName": x.get('program_id__title')}
                        
                        queryset2 = Course.objects.get(
                            course_id=courseDet.course_id_id)
                        
                        if queryset2 == None:
                            return JsonResponse({"success":False, "message": "No courses under this program", "data": {}}, safe=False)
                        else:
                            resultDic["courseId"] = queryset2.course_id
                            resultDic["courseCode"] = queryset2.course_code
                            resultDic["courseName"] = queryset2.course_name
                            datas.append(resultDic)
            else:
                return JsonResponse(error)
       
        return {"success":True, "data": {"teacherCourseList": datas}, "message": "Succesfully fetched"}
    except Exception as e:
        return JsonResponse(error)





  
