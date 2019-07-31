from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
import datetime
from django.http import HttpResponse,JsonResponse
import requests 
import json
import re
from .constants import *
#=======================================#
# function for add department details   #
#=======================================#

def department_add(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('dept_name') and data.get('dept_desc') and data.get('dept_code'):
            dept_name=data.get('dept_name')
            name=dept_name.replace(' ','')
            if len(name)==0:
                return JsonResponse({"status":404,"message":"Invalid data in department name"},safe=False) 
            name=dept_name.lower()
            deptname=name.replace(' ','')
            dept_desc=data.get('dept_desc')
            desc=dept_desc.replace(' ','')
            if len(desc)==0:
                return JsonResponse({"status":404,"message":"Invalid data in department description"},safe=False)
            dept_code=data.get('dept_code')
            deptcode=dept_code.replace(' ','')
            depcod=deptcode.upper()
            if len(deptcode)==0:
                return JsonResponse({"status":404,"message":"Invalid data in department code"},safe=False) 

            deptobj = Department.objects.filter(Department_code=depcod)
            if deptobj.count()!=0:
                return JsonResponse({"status":404,"message":"Department already exist"},safe=False)
            else:
                x=Department(Department_Name=dept_name,Department_description=dept_desc,
                meta_tag=deptname,Department_code=depcod)
                x.save()
                return JsonResponse({"status":200,"message":"successfully added department details"},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)
#=======================================#
# function for edit  department details #
#=======================================#
def department_edit(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('dept_id') and data.get('dept_name') and data.get('dept_desc'):
            deptid=data.get('dept_id')
            dept_name=data.get('dept_name')
            name=dept_name.replace(' ','')
            if len(name)==0:
                return JsonResponse({"status":404,"message":"Invalid data in department name"},safe=False)
            name=dept_name.lower()
            deptname=name.replace(' ','')
            dept_desc=data.get('dept_desc')
            desc=dept_desc.replace(' ','')
            if len(desc)==0:
                return JsonResponse({"status":404,"message":"Invalid data in department description"},safe=False)
            deptobj = Department.objects.filter(Department_id=deptid)
            if deptobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid department id"},safe=False)
            else:
                for i in deptobj:
                    i.Department_Name=dept_name
                    i.Department_description=dept_desc
                    i.meta_tag=deptname
                    i.save()
                    return JsonResponse({"status":200,"message":"successfully edited department details"},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)

    # =================================#
    #  function for get a department   #
    # =================================#

def get_a_department(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('did'):
            department_id = data.get('did')
            queryset = Department.objects.filter(Department_id=department_id)
            if queryset.count()==0:
                return JsonResponse({"status":404,"message":"Invalid department id"},safe=False)
            else:
                data=[]
                for i in queryset:
                    dict1={"id":i.Department_id,"Department_Name":i.Department_Name,
                    "Department_description":i.Department_description,
                    "Department_code":i.Department_code
                    }
                    data.append(dict1)
                return JsonResponse({"status":200,"message":data},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)


# ==================================#
#  function for get all Departments #
# ==================================#

def get_all_department():
    try:
        departmentData=Department.objects.all()
        data=[]
        for i in departmentData:
            dict1={"id":i.Department_id,"Department_Name":i.Department_Name,
            "Department_description":i.Department_description,
            "Department_code":i.Department_code
            }
            data.append(dict1)
        return JsonResponse({"status":200,"message":data},safe=False)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)