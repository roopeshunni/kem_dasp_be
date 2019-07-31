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
from django.db.models import Q
# ==================================================#
#  function for get all courses under a programme   #
# ==================================================#

def get_all_prg_courses(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('prg_id'):
            program_id = data.get('prg_id')
            queryset1 =Programme.objects.filter(program_id=program_id)
            if queryset1.count()==0:
                return JsonResponse({"status":404,"message":"Invalid programme id"},safe=False)
            queryset = Course_programme_mapping.objects.filter(prg_id=program_id)
            if queryset.count()==0:
                return JsonResponse({"status":404,"message":"No courses under this programme"},safe=False)
            else:
                data=[]
                for i in queryset:
                    courseobj = Course.objects.filter(course_id=i.course_id_id)
                    for j in courseobj:
                        dict1={"couse_id":j.course_id,"code":j.course_code,"name":j.course_name,
                            "credit":j.credit,"int_mark":j.internal_mark,"ext_mark":j.external_mark,
                            "total_mark":j.total_mark}
                        data.append(dict1)
                return JsonResponse({"status":200,"message":data},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)
        
# ==================================================#
#  function for get all course names under a batch  #
# ==================================================#

def get_all_batch_course_name(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('batch_id'):
            batchid = data.get('batch_id')
            batchobj =Batch.objects.filter(batch_id=batchid)
            if batchobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid batch id"},safe=False)
            else:
                for batch in batchobj:
                    batchdata=[]
                    prgobj =Programme.objects.get(program_id=batch.program_id_id)
                    deptobj =Department.objects.get(Department_id=batch.department_id_id)
                    studobj =studycentre.objects.get(studycentre_id=batch.study_centre_id_id)
                    batchdict={"id":batch.batch_id, "name":batch.batch_name,"prg_name":prgobj.title,
                                "dept_name":deptobj.Department_Name,"study_name":studobj.name,
                                "seats":batch.no_of_seats,"app_start":batch.appli_start_date,
                                "app_end":batch.appli_end_date,"prg_start":batch.prgm_start_date,
                                "prg_end":batch.prgm_end_date,"status":batch.status,"fees":batch.program_fee}
                    batchdata.append(batchdict)
                    queryset = Course_programme_mapping.objects.filter(prg_id=batch.program_id_id)
                    if queryset.count()==0:
                        message={"batchdetails":batchdata,"coursedetails":[]}
                        return JsonResponse({"status":200,"message":message},safe=False)
                    else:                        
                        data=[]
                        for i in queryset:
                            courseobj = Course.objects.filter(course_id=i.course_id_id)
                            for j in courseobj:
                                dict1={"couse_id":j.course_id,"name":j.course_name,"prg_cr_id":i.course_prg_id,
                                "code":j.course_code,"credit":j.credit,"imark":j.internal_mark,
                                "emark":j.external_mark,"tmark":j.total_mark}
                                data.append(dict1)
                        msg={"batchdetails":batchdata,"coursedetails":data}
                        return JsonResponse({"status":200,"message":msg},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)

# ==================================================#
#     function for add programme structure          #
# ==================================================#
def add_all_prg_courses(received_json_data):
    try:
        data1 = json.dumps(received_json_data)
        data = json.loads(data1)
        if data.get('course_code') and data.get('course_name') and data.get('credit') and data.get('internal_mark') and data.get('external_mark') and data.get('total_mark'):
            coursecode= data.get('course_code')
            coursename= data.get('course_name')
            credit= data.get('credit')
            internalmark = data.get('internal_mark')
            externalmark = data.get('external_mark')
            totalmark=data.get('total_mark')
            v1=Course.objects.filter(course_code=coursecode)
            if v1.count()!=0:
                return JsonResponse({"status": 404, "message": "Course already exist"})
            else:
                x = Course(course_code=coursecode, course_name=coursename,
                        credit=credit, internal_mark=internalmark,
                        external_mark=externalmark, total_mark=totalmark)
                x.save()
                return JsonResponse({"status": 200, "message": "Successfully added details"})
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)


# ==================================================#
#     function for edit programme structure         #
# ==================================================#

def edit_prog_course(received_json_data):
    try:
        data1 = json.dumps(received_json_data)
        data = json.loads(data1)
        if data.get('course_id') and data.get('course_name') and data.get('credit') and data.get('internal_mark') and data.get('external_mark') and data.get('total_mark'):
            courseid = data.get('course_id')
            coursename = data.get('course_name')
            credit = data.get('credit')
            internalmark = data.get('internal_mark')
            externalmark = data.get('external_mark')
            totalmark = data.get('total_mark')
            obj =Course.objects.filter(course_id=courseid)
            if obj.count()==0:
                return JsonResponse({"status": 404, "message": "Invalid course id"})
            else:
                for i in obj:
                    i.course_name = coursename
                    i.credit = credit
                    i.internal_mark = internalmark
                    i.external_mark = externalmark
                    i.total_mark = totalmark
                    i.save()
                    return JsonResponse({"status": 200, "message": "Successfully edited course details"}, safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)


# ==================================================#
#     function for get all  programme structure     #
# ==================================================#

def courseget():
    try:
        queryset = Course.objects.all().order_by('course_code')
        aboutusDict1 = []
        for i in queryset:
            aboutusDict = {"course_id": i.course_id,"course_code": i.course_code, "course_name": i.course_name, "credit": i.credit,
                           "internal_mark": i.internal_mark, "external_mark": i.external_mark,
                            "total_mark": i.total_mark}
            aboutusDict1.append(aboutusDict)
        return JsonResponse({"status": 200, "message": aboutusDict1})
    except Exception as e:
        # err = {"status": 400, "message": "Bad Request"}
        return JsonResponse(error)

# ==================================================#
#     function for get single programme structure   #
# ==================================================#

def course_details(received_json_data):
    try:
        data1 = json.dumps(received_json_data)
        data = json.loads(data1)
        if data.get('course_id'):
            course_id = data.get('course_id')
            courseDet= Course_programme_mapping.objects.get(
                        course_prg_id=course_id)
            obj = Course.objects.filter(course_id=courseDet.course_id_id)
            if obj.count() == 0:
                return JsonResponse({"status": 404, "message": "Invalid course id"})
            else:
                aboutusDict1 = []
                for i in obj:
                    aboutusDict = {"course_id": i.course_id, "course_code": i.course_code, "course_name": i.course_name, "credit": i.credit,
                                "internal_mark": i.internal_mark, "external_mark": i.external_mark, "total_mark": i.total_mark}
                    aboutusDict1.append(aboutusDict)
                    return JsonResponse({"status": 200, "message": aboutusDict1})
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)


# ==================================================#
#     function for map programme and course         #
# ==================================================#

def add_all_prg_coursepgmmapping(received_json_data):
    try:
        data1 = json.dumps(received_json_data)
        data = json.loads(data1)
        if data.get('course_id') and data.get('prg_id'):
            course_id = data.get('course_id')
            prgid = data.get('prg_id')
            obj = Course.objects.filter(course_id=course_id)
            if obj.count() == 0:
                return JsonResponse({"status": 404, "message": "Invalid course id"})
            obj1 =Programme.objects.filter(program_id=prgid)
            if obj1.count() == 0:
                return JsonResponse({"status": 404, "message": "Invalid program id"})
            batchobj=Batch.objects.filter(program_id_id=prgid).exclude(status="hide")
            if (batchobj.count()!=0):
                return JsonResponse({"status":404,"message":"Batch already started.Can't assign course"},safe=False)
            v1 = Course_programme_mapping.objects.filter(course_id=course_id,prg_id=prgid)
            if v1.count() != 0:
                return JsonResponse({"status": 404, "message": "Course already mapped"})
            else:
                x = Course_programme_mapping(course_id_id=course_id, prg_id_id=prgid)
                x.save()
                return JsonResponse({"status": 200, "message": "Successfully mapped programme and course"})
        else:
            return JsonResponse(error)

    except Exception as e:  
        return JsonResponse(internalServer)

# ==================================================#
#    function for unlink programme and course       #
# ==================================================#


def del_all_prg_coursepgmmapping(received_json_data):
    try:
        data1 = json.dumps(received_json_data)
        data = json.loads(data1)
        if data.get('course_id') and data.get('program_id'):
            course_id = data.get('course_id')
            prgid = data.get('program_id')
            obj = Course.objects.filter(course_id=course_id)
            if obj.count() == 0:
                return JsonResponse({"status": 404, "message": "Invalid course id"})
            obj = Programme.objects.filter(program_id=prgid)
            if obj.count() == 0:
                return JsonResponse({"status": 404, "message": "Invalid program id"})
            courseMap= Course_programme_mapping.objects.filter(course_id=course_id, prg_id=prgid)
            if courseMap.count() == 0:
                return JsonResponse({"message": "No such course mapping found"})
            batches=Batch.objects.filter(program_id=prgid).exclude(status="hide").exclude(status="Inactive")
            if batches.count()!=0:
                return JsonResponse({"status": 200, "message": "Batch exist,can't unlink course and programme"})
            else:
                courseMap.delete()
                return JsonResponse({"status": 200, "message": "Successfully unlink course and programme"})
    except Exception as e:
        return JsonResponse(internalServer)