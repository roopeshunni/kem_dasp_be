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
from random import randint
from .constants import *
from dateutil import tz
from datetime import datetime as dt
to_zone=tz.gettz('Asia/Calcutta')
#===============================================================#
# function for creating 5 digit random number for applicant id  #
#===============================================================#
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
#======================================================#
# function for checking applicant already exist or not #
#======================================================#

def add_applicant(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('batchid') and data.get('userid') and data.get('prgid') and data.get('deptcode'):
            batchid=data.get('batchid')
            userid=data.get('userid')
            prgid=data.get('prgid')
            dept_code=data.get('deptcode')
            # applieddate=datetime.datetime.now()
            # print(type(applieddate))
            applieddate=current_datetime()
            year_of_applicant=str((applieddate.year%100))
            appstatus='applicant'
            is_paid=False
            v6=Batch.objects.filter(batch_id=batchid)       
            if(len(v6)==0):
                return JsonResponse({"status": 200,'message':'Invalid Batchid'},safe=False)

            v7=Programme.objects.filter(program_id=prgid)
            if(len(v7)==0):
                return JsonResponse({"status": 200,'message':'Invalid Programmeid '},safe=False)
            for j in v7:
                prg_type=j.program_type
                batches=Batch.objects.filter(program_id_id=prgid,status="admission")
                if batches.count()==0:
                    return JsonResponse({"status": 200,'message':'Admission process not started'},safe=False)
                batchobj = StudentApplicants.objects.filter(program_id_id=prgid,user_id=userid,batch_id_id=batchid)
                if batchobj.count()!=0:
                    return JsonResponse({"status":200,"message":"Already Exists"},safe=False)
                else:
                    app_no_rand=random_with_N_digits(5)
                    app_id=prg_type+dept_code+year_of_applicant+str(app_no_rand)
                    appobj=StudentApplicants.objects.filter(applicant_id=app_id)
                    if appobj.count()!=0:
                        app_no_rand=random_with_N_digits(5)
                        app_id=prg_type+dept_code+year_of_applicant+str(app_no_rand)
                        x=StudentApplicants(batch_id_id=batchid,user_id=userid,program_id_id=prgid,applied_date=applieddate,applicant_status=appstatus,course_fee=-1,
                        transaction_id=-1,applicant_id=app_id,is_paid=is_paid)
                        x.save()
                        return JsonResponse({"status":200,"message":"successfully added student details"},safe=False)
                    else:
                        x=StudentApplicants(batch_id_id=batchid,user_id=userid,program_id_id=prgid,applied_date=applieddate,applicant_status=appstatus,course_fee=-1,
                        transaction_id=-1,applicant_id=app_id,is_paid=is_paid)
                        x.save()
                        return JsonResponse({"status":200,"message":"successfully added student details"},safe=False)
        elif data.get('user_id') and data.get('prgm_id') and data.get('txn_id') and data.get('batch_id'):
                userid=data.get('user_id')
                prgid=data.get('prgm_id')
                batid=data.get('batch_id')
                transid=data.get('txn_id')
                prgmobj=Programme.objects.filter(program_id=prgid)
                if len(prgmobj)==0:
                    return JsonResponse({"status": 200,'message':'Invalid Programmeid'},safe=False)
                else:
                    for i in prgmobj:
                        appobj=StudentApplicants.objects.get(user_id=userid,program_id_id=prgid,batch_id_id=batid)
                        tid=appobj.transaction_id
                        if tid=="-1":
                            appobj.transaction_id=transid
                            appobj.is_paid=True
                            appobj.save()                   
                            return JsonResponse({"status":200,"message":"successfully added transaction id"},safe=False)
                        else:
                             return JsonResponse({"status":404,"message":"Already added transaction id"},safe=False)

        else:
            return JsonResponse(error,safe=False) 
    except Exception as e:
        print(e)
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)


def current_datetime():
    c_date=datetime.datetime.now().astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")
    cur_date=dt.strptime(c_date, '%Y-%m-%d %H:%M:%S')
    return cur_date
#======================================================#
#        function for changing status to  student      #
#======================================================#

def make_student(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('batchid') and data.get('userid') and data.get('prgid'):
            batchid=data.get('batchid')
            userid=data.get('userid')
            prgid=data.get('prgid')
            prgmobj=Programme.objects.filter(program_id=prgid)
            if len(prgmobj)==0:
                return JsonResponse({"status": 200,'message':'Invalid Programmeid'},safe=False)
            v6=Batch.objects.filter(batch_id=batchid)       
            if(len(v6)==0):
                return JsonResponse({"status": 200,'message':'Invalid Batchid'},safe=False)
            appobj2=StudentApplicants.objects.filter(user_id=userid,applicant_status="student")

            if(len(appobj2)>0):
                return JsonResponse({"status":400,'message':'Selected student is already assigned to a batch'},safe=False)

            seat=v6[0].no_of_seats
            appobj1=StudentApplicants.objects.filter(program_id_id=prgid,batch_id_id=batchid,applicant_status="student")
            if len(appobj1)<seat:
                appobj=StudentApplicants.objects.get(user_id=userid,program_id_id=prgid,batch_id_id=batchid)
                if appobj.is_paid==True:
                    appobj.applicant_status="student"
                    appobj.save()                   
                    return JsonResponse({"status":200,"message":"successfully changed to student"},safe=False)
                else:
                     return JsonResponse({"status":200,"message":"can't change to student"},safe=False)
            else:
                return JsonResponse({"status":404,"message":"All seats are filled.Can't admit Student"},safe=False)
                
        else:
            return JsonResponse(error,safe=False) 
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)
#====================================================================#
#     function for get programmes applied by an user - Mycourses     #
#====================================================================#
def my_courses(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('userid'):
            userid=data.get('userid')
            appobj=StudentApplicants.objects.filter(user_id=userid)
            userlist=[]
            for i in appobj:
                studid=i.student_id
                batchid=i.batch_id_id
                
                prg_id=i.program_id_id
                applieddate=i.applied_date.date()
                status=i.applicant_status
                appliacantid=i.applicant_id
                is_paid=i.is_paid
                list2=[]
                paylist=[]
                paymentdetails=PaymentHistory.objects.filter(applicant_no=appliacantid,user_id=userid)
                for p in paymentdetails:
                    t_date=p.trans_date
                    dt=t_date.strftime("%Y-%m-%d %H:%M:%S")
                    trans_date=str(dt).replace('Z', '').replace('T', '')
                    payDet={"order_id":p.order_id,"trans_id":p.trans_id,"trans_amount":p.trans_amount,"trans_date":trans_date,
                    "res_code":p.res_code,"status":p.status,"res_msg":p.res_msg,"total_fee":p.total_fee}
                    paylist.append(payDet)

                cprgobj = Course_programme_mapping.objects.filter(prg_id=prg_id)
                for cp in cprgobj:
                    courobj = Course.objects.filter(course_id=cp.course_id_id)
                    for course in courobj:
                        dict2={
                            "id":course.course_id, "code":course.course_code,"name":course.course_name,
                            "credit":course.credit,"imark":course.internal_mark,
                            "emark":course.external_mark,"tmark":course.total_mark}
                        list2.append(dict2)
                result={"applicant_id":appliacantid,"programid":prg_id,"programcode":i.program_id.program_code,
                "programname":i.program_id.title,"description":i.program_id.description,
                "thumbnail":i.program_id.thumbnail,"prg_fee":i.batch_id.program_fee,
                "applieddate":str(applieddate),"studentid":studid,"is_paid":is_paid,
                "batchid":batchid,"batchname":i.batch_id.batch_name,"status":status,
                "courses":list2,"paymentDic":paylist}
                userlist.append(result)
            return JsonResponse({"status":200, "imgpath": "https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/web/","message":userlist},safe=False) 
        else:
            return JsonResponse(error,safe=False) 
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)