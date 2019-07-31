from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import *
from .constants import *
from django.http import JsonResponse
import datetime
import json
import requests
import string
from django.db.models import Q
from django.db.models import Subquery
#=====================================#
# function for add programme details  #
#=====================================#

def add_programme(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        # print(data)
        if data.get('prg_code') and data.get('title') and data.get('desc') and data.get('dept_id') and data.get('structure') and data.get('syllabus') and data.get('brochure') and data.get('thumbnail') and data.get('eligibility') and data.get('prgtype') and data.get('no_of_semester'):
            no_of_semester=data.get('no_of_semester')
            code=data.get('prg_code').upper()
            pgm_code=code.replace(' ','')
            prgobj = Programme.objects.filter(program_code=pgm_code)
            if prgobj.count()>0:
                return JsonResponse({"status":404,"message":"Programme code already exist"},safe=False)
            if len(pgm_code)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme code"},safe=False)
            title=data.get('title')
            title_lower=title.lower()
            pgm_title=title_lower.replace(' ','')
            if len(pgm_title)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme title"},safe=False)
            desc=data.get('desc')
            pgm_desc=desc.replace(' ','')
            if len(pgm_desc)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme description"},safe=False)
            deptid=data.get('dept_id') 
            structure=data.get('structure')
            pgm_struct=structure.replace(' ','')
            if len(pgm_struct)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme structure"},safe=False)
            syllabus=data.get('syllabus')
            pgm_syllabus=syllabus.replace(' ','')
            if len(pgm_syllabus)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme syllabus"},safe=False)
            thumbnail=data.get('thumbnail')
            pgm_thumb=thumbnail.replace(' ','')
            if len(pgm_thumb)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme thumbnail"},safe=False)
            eligibility=data.get('eligibility')
            pgm_eli=eligibility.replace(' ','')
            if len(pgm_eli)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme eligibility"},safe=False)
            brochure=data.get('brochure') 
            pgm_bro=brochure.replace(' ','')
            if len(pgm_bro)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme brochure"},safe=False)
            status="active" 
            prg_type=data.get('prgtype').upper()  
            prgm_title=title.replace(' ',',')
            if ' ' in title_lower:
                metatag=pgm_title+','+prgm_title.lower()+','+pgm_code.lower()                
            else:
                metatag=pgm_title+','+pgm_code.lower()            
            
            prgobj = Programme.objects.filter(program_code=code)
            if prgobj.count()!=0:
                return JsonResponse({"status":404,"message":"Programme already exist"},safe=False)
            deptobj = Department.objects.filter(Department_id=deptid)
            if deptobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid department id"},safe=False)
            else:
                x=Programme(program_code=pgm_code,title=title,description=desc,department_id_id=deptid,
                programme_Struture=structure,syllabus=syllabus,brochure=brochure,status=status,
                thumbnail =thumbnail,meta_tag=metatag,eligibility =eligibility,program_type=prg_type,no_of_semester=no_of_semester)
                x.save()
                prgmobj = Programme.objects.filter(program_code=pgm_code)
                for i in prgmobj:
                    pid=i.program_id
                return JsonResponse({"status":200,"message":"Successfully added programme details"},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)

#=======================================#
# function for edit  programme  details #
#=======================================#
def edit_programme(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('pid') and data.get('prg_code') and data.get('title') and data.get('desc') and data.get('dept_id') and data.get('structure') and data.get('syllabus') and data.get('brochure') and data.get('thumbnail') and data.get('eligibility'):
            prg_id=data.get('pid')
            prgmobj = Programme.objects.filter(program_id=prg_id)
            if prgmobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid programme id"},safe=False)
            deptid=data.get('dept_id')
            deptobj = Department.objects.filter(Department_id=deptid)
            if deptobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid department id"},safe=False)
            code=data.get('prg_code').upper()
            pgm_code=code.replace(' ','')
            prgobj = Programme.objects.filter(program_code=pgm_code).exclude(program_id=prg_id)
            if prgobj.count()>0:
                return JsonResponse({"status":404,"message":"Programme code already exist"},safe=False)
            if len(pgm_code)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme code"},safe=False)
            title=data.get('title')
            title_lower=data.get('title')
            pgm_title=title_lower.replace(' ','')
            if len(pgm_title)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme title"},safe=False)
            desc=data.get('desc')
            pgm_desc=desc.replace(' ','')
            if len(pgm_desc)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme description"},safe=False)  
            structure=data.get('structure')
            pgm_struct=structure.replace(' ','')
            if len(pgm_struct)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme structure"},safe=False)
            syllabus=data.get('syllabus')
            pgm_syllabus=syllabus.replace(' ','')
            if len(pgm_syllabus)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme syllabus"},safe=False)
            thumbnail=data.get('thumbnail')
            pgm_thumb=thumbnail.replace(' ','')
            if len(pgm_thumb)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme thumbnail"},safe=False)
            eligibility=data.get('eligibility')
            pgm_eli=eligibility.replace(' ','')
            if len(pgm_eli)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme eligibility"},safe=False)
            brochure=data.get('brochure') 
            pgm_bro=brochure.replace(' ','')
            if len(pgm_bro)==0:
                return JsonResponse({"status":404,"message":"Invalid data in programme brochure"},safe=False)   
            prgm_title=title.replace(' ',',')
            if ' ' in title_lower:
                metatag=pgm_title.lower()+','+prgm_title.lower()+','+pgm_code.lower()
            else:
                metatag=pgm_title+','+pgm_code.lower()
            # no_of_semester=data.get('no_of_semester')
   
            for i in prgmobj:
                i.program_code=pgm_code
                i.title=title
                i.description=desc
                i.department_id_id=deptid
                i.programme_Struture=structure
                i.syllabus=syllabus
                i.brochure=brochure
                i.thumbnail =thumbnail
                i.meta_tag=metatag
                i.eligibility =eligibility
                # i.no_of_semester=no_of_semester
                i.save()
            return JsonResponse({"status":200,"message":"Successfully edited programme details"},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)
#========================================#
# function for delete programme  details #
#========================================#
def delete_programme(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('pid'):
            prg_id=data.get('pid')
            prgobj = Programme.objects.filter(program_id=prg_id)
            if prgobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid programme id"},safe=False)
            else:
                prgobj.delete()
                return JsonResponse({"status":200,"message":"successfully deleted programme"},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)
#=======================================#
# function for change programme status  #
#=======================================#
def change_status_prgm(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('pid') and data.get('status') :
            prg_id=data.get('pid')
            prg_status=data.get('status')
            prgobj = Programme.objects.filter(program_id=prg_id)
            if prgobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid programme id"},safe=False)
            batchobj=Batch.objects.filter(program_id_id=prg_id).exclude(status="hide")
            if (batchobj.count()!=0 and prg_status=="inactive"):
                return JsonResponse({"status":404,"message":"Please change the batch status first then change programme status"},safe=False)
            else:
                for i in prgobj:
                    old_status=i.status
                    i.status=prg_status
                    i.save()
                    return JsonResponse({"status":200,"message":"Successfully changed programme status"},safe=False)                
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)


# ==================================#
#  function for finding image path  #
# ==================================#
def imagepath(dtype):
    imgpath="https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/"
    if dtype=="M":
        imgpath=imgpath+"mobile/"
        return imgpath
    elif dtype=="W":
        imgpath=imgpath+"web/"
        return imgpath
    else:
        return False
# =====================================#
#  function for finding structure path #
# =====================================#
def structurepath(dtype):
    structpath="https://s3-ap-southeast-1.amazonaws.com/dastp/Program/structure_image/"
    if dtype=="M":
        structpath=structpath+"mobile/"
        return structpath
    elif dtype=="W":
        structpath=structpath+"web/"
        return structpath
    else:
        return False


# =================================#
#  function for get all programme  #
# =================================#
def get_all_programme(received_json_data):
    try:

        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('pid'):
            if data.get('dtype'):
                program_id = data.get('pid')
                dtype=data.get('dtype').upper()
                img_path=imagepath(dtype)
                if img_path==False:
                    return error
                str_path=structurepath(dtype)
                if str_path==False:
                    return error
                programData=Programme.objects.filter(program_id=program_id,status='active')
                if programData.count()==0:
                    return {"status":200,"message":[]}
                else:
                    for i in programData:
                        departobj = i.department_id_id
                        departmentobj = Department.objects.get(Department_id=departobj)
                        list1=[]
                        batchobj = Batch.objects.filter(program_id=i.program_id).exclude(status="hide")
                        for j in batchobj:
                            studycentre_id = j.study_centre_id_id
                            studycentre_details = studycentre.objects.get(studycentre_id=studycentre_id)
                            dict1={"batch_id":j.batch_id,"study_Centre":studycentre_details.name,'batch_name':j.batch_name,
                            'application_start_date':str(j.appli_start_date),'application_end_date':str(j.appli_end_date),
                            'programme_start_date':str(j.prgm_start_date),'programme_end_date':str(j.prgm_end_date),'Fees':j.program_fee,
                            'status':j.status,"seats":j.no_of_seats,"batch_display_name":j.batch_dis_name}
                            list1.append(dict1)
                        list2=[]
                        cprgobj = Course_programme_mapping.objects.filter(prg_id=i.program_id)
                        for cp in cprgobj:
                            courobj = Course.objects.filter(course_id=cp.course_id_id)
                            for course in courobj:
                                dict2={
                                    "id":course.course_id, "code":course.course_code,"name":course.course_name,
                                    "credit":course.credit,"imark":course.internal_mark,
                                    "emark":course.external_mark,"tmark":course.total_mark}
                                list2.append(dict2)
                        data=[]
                        dict1={"id":i.program_id,"code":i.program_code,
                        "title":i.title,"description":i.description,
                        "department_id":departmentobj.Department_Name,
                        "dept_id":departmentobj.Department_id,
                        "deptcode":departmentobj.Department_code,
                        "structure":i.programme_Struture,
                        "status":i.status,"thumbnail":i.thumbnail,
                        "meta_tag":i.meta_tag,"eligibility":i.eligibility,"prgtype":i.program_type,
                        "syllabus":i.syllabus,"brochure":i.brochure,"no_of_semester":i.no_of_semester,
                        "batches":list1,"courses":list2}
                        # print(dict1)
                        data.append(dict1)
                return {"status":200,"imagepath":img_path,"structurepath":str_path,"message":data}

        elif data.get('pdid'):
            if data.get('dtype'):
                department_id=data.get('pdid')
                dtype=data.get('dtype').upper()
                img_path=imagepath(dtype)
                if img_path==False:
                    return error
                str_path=structurepath(dtype)
                if str_path==False:
                    return error
                programDepartment = Programme.objects.filter(department_id=department_id)
                programDict1 = []
                for i in programDepartment:
                    depart_id = i.department_id_id
                    departmentobj = Department.objects.get(Department_id=depart_id)
                    queryDict = {"id":i.program_id,"PCode":i.program_code,"title":i.title,"description":i.description,
                    "structure":i.programme_Struture,"syllabus":i.syllabus,"brochure":i.brochure,
                    "department_id":departmentobj.Department_Name,"Photo":i.thumbnail,"status":i.status,
                    "Tags":i.meta_tag,"eligibility":i.eligibility,"prgtype":i.program_type,"no_of_semester":i.no_of_semester}
                    programDict1.append(queryDict)
                return {"status":200,"imagepath":img_path,"structurepath":str_path,"message":programDict1}
        elif data.get('dtype'):
            dtype=data.get('dtype').upper()
            img_path=imagepath(dtype)
            if img_path==False:
                return error
            str_path=structurepath(dtype)
            if str_path==False:
                return error
            programData=Programme.objects.filter(status="active").order_by('title')
            data=[]
            flag=0
            for i in programData:
                list1=[]
                # batchobj = Batch.objects.filter(program_id=i.program_id).exclude(status="hide")
                batchobj = Batch.objects.filter(~Q(status="hide"),program_id=i.program_id).select_related('study_centre_id','department_id  ').values('batch_name','batch_id','appli_start_date','appli_end_date','prgm_start_date','prgm_end_date','program_fee','status','study_centre_id__name','department_id__Department_code','department_id__Department_Name','department_id','batch_dis_name')
                # print(len(batchobj))
                if len(batchobj) == 0:
                    dict1={"batch_id":"NA","study_Centre":"NA",
                    'batch_name':"NA",'application_start_date':"NA",
                    'application_end_date':"NA",'programme_start_date':"NA",
                    'programme_end_date':"NA",'Fees':"NA",'status':"NA","batch_dis_name":"NA"}
                    list1.append(dict1)
                    flag=1
                for j in batchobj:
                    flag=0
                    # studycentre_id = j.study_centre_id_id
                    department_code=j['department_id__Department_code']
                    # deptobj=Department.objects.get(Department_id=department_id_id)
                    # studycentre_details = studycentre.objects.get(studycentre_id=studycentre_id)
                    dict1={"batch_id":j['batch_id'],"study_Centre":j['study_centre_id__name'],
                    'batch_name':j['batch_name'],'batch_dis_name':j['batch_dis_name'],'application_start_date':str(j['appli_start_date']),
                    'application_end_date':str(j['appli_end_date']),'programme_start_date':str(j['prgm_start_date']),
                    'programme_end_date':str(j['prgm_end_date']),'Fees':j['program_fee'],'status':j['status']}
                    list1.append(dict1)
                short_dption = i.description
                short_title = short_dption[0:60]
                s=short_title.rsplit(' ', 1)[0]
                short_title1 = s+' ...'
                dict1={"id":i.program_id,"program_code":i.program_code,"title":i.title,
                "description":short_title1,"no_of_semester":i.no_of_semester,
                "structure":i.programme_Struture,"status":i.status,"thumbnail":i.thumbnail,
                "meta_tag":i.meta_tag,"eligibility":i.eligibility,"syllabus":i.syllabus,"brochure":i.brochure,
                "prgtype":i.program_type,"batches":list1,"full_description":short_dption}
                
                if flag==0:
                    dict1.update({"department_id":j['department_id'],"departmentcode":j['department_id__Department_code']})
                else:
                    dict1.update({"department_id":"NA","departmentcode":"NA"})
                data.append(dict1)
            return {"status":200,"imagepath":img_path,"structurepath":str_path,"message":data}
        else:
                return error
    except Exception as e:
        print(e)
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer
# =================================#
#  function for get a programme    #
# =================================#       
def allprogramme():
    try:
        programDepartment = Programme.objects.select_related('department_id').values('program_id','program_code','title','description',
    	'program_type','department_id','department_id__Department_Name','programme_Struture','syllabus','no_of_semester',
		'brochure','status','thumbnail','meta_tag','eligibility')
        list1=[]
        for i in programDepartment:
            dict1={"program_id":i['program_id'],"program_code":i['program_code'],"title":i['title'],
            "description":i['description'],"prgtype":i['program_type'],
            "dept_id":i['department_id'],"department_name":i['department_id__Department_Name'],"programme_Struture":i['programme_Struture'],
            "syllabus":i['syllabus'],"brochure":i['brochure'],"no_of_semester":i['no_of_semester'],
            "status":i['status'],"thumbnail":i['thumbnail'],"meta_tag":i['meta_tag'],"eligibility":i['eligibility']
            }
            list1.append(dict1)
        departmentobj1 = Department.objects.values('Department_id','Department_Name','Department_code')
        list2=[]
        for i in departmentobj1:
            dict1={"Department_id":i['Department_id'],"Department_Name":i['Department_Name'],"Department_code":i['Department_code']}
            list2.append(dict1)
        msg={"programme":list1,"department":list2}
        return JsonResponse({"status":200,"message":msg},safe=False)
    except Exception as e:
        # # print(e)
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)

# ====================================================#
#  function for get list programme and their courses  #
# ====================================================#

def all_programme_courses_list(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('pid') and data.get('dtype'):
                program_id = data.get('pid')
                dtype=data.get('dtype').upper()
                prg_list=[]
                for i in program_id:
                    queryset1 =Programme.objects.filter(program_id=i)
                    if queryset1.count()==0:
                        continue
                    else:
                        received_json_data={"pid":i,"dtype":dtype}
                        prgDataResponse=get_all_programme(received_json_data)
                        dir_rec_data=json.dumps(prgDataResponse)
                        dir_parsed_data=json.loads(dir_rec_data)
                        imgpath=dir_parsed_data.get("imagepath")
                        msg=dir_parsed_data.get("message")[0]
                        del msg["batches"]
                        prg_list.append(msg) 
                return JsonResponse({"status":200,"message":prg_list,"imgpath":imgpath})
        else:
            return JsonResponse(error)
    except Exception as e:
        # print(e)
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)

def program_semester_list(received_json_data):
    try:
        receiveddata=json.dumps(received_json_data)
        data=json.loads(receiveddata)
        if data.get('pid'):
            program_id = data.get('pid')
            queryset=Programme.objects.filter(program_id=program_id)
            resultlist=[]
            if len(queryset) == 0:
                return JsonResponse({"status":404,"message":"Invalid programme id"})
            else:
                for i in queryset:
                    resultData={"no_of_semester":i.no_of_semester}
                resultlist.append(resultData)
                return JsonResponse({"status":200,"message":resultlist},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)

# ====================================================#
#  function for get list programme and payment details#
# ====================================================#

def get_prgm_paymentdetails(received_json_data):
    try:
        received_data=json.dumps(received_json_data)
        data=json.loads(received_data)
        if data.get('pid') and data.get('student_id') and data.get('batch_id') :
            program_id=data.get('pid')
            user_id=data.get('student_id')
            batch_id=data.get('batch_id')
            
            prgobj=Programme.objects.filter(program_id=program_id)
            if prgobj.count()==0:
                return {"status":404,"message":"Invalid programme id"}
            else:
                for i in prgobj:
                    prg_id=i.program_id
                    prg_code=i.program_code
                    prg_name=i.title
                programdict={"prgcode":prg_code,"prgname":prg_name}
                batchlist={}
                batchdetails=Batch.objects.filter(program_id_id=prg_id)
                for i in batchdetails:
                    batchid=i.batch_id
                    batchname=i.batch_name
                    batchdict={"batchid":batchid,"batchname":batchname}
                    batchlist.update({batchid:batchdict})
                    paymentList=[]
                studaplobj= StudentApplicants.objects.filter(batch_id_id=data.get('batch_id'),user_id=user_id,program_id_id=program_id)
                if len(studaplobj)!=0:
                    for i in  studaplobj: 
                        paymentdetails=PaymentHistory.objects.filter(applicant_no=i.applicant_id,status="TXN_SUCCESS")
                        if len(paymentdetails)==0:
                            paymentList=[]
                        else:
                            for j in paymentdetails:
                                t_date=j.trans_date
                                dt=t_date.strftime("%Y-%m-%d %H:%M:%S")
                                trans_date=str(dt).replace('Z', '').replace('T', '')
                                paymentDic={"trans_id":j.trans_id,"applicant_no":j.applicant_no,
                                "trans_amount":j.trans_amount,"trans_date":trans_date,"res_code":j.res_code,
                                "total_fee":j.total_fee}
                                paymentList.append(paymentDic)
                result={"prgid":program_id,"ProgramDetails":programdict,"BatchDetails":batchlist,"paymentDetails":paymentList}
                return {"status":200,"message":result}
        else:
            return error
    except Exception as e:
        print(e)
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer

    
# ====================================================#
#  function for getting ongoing programmes            #
# ====================================================#

def get_ongoing_prgms(received_json_data):
    try:
        received_data=json.dumps(received_json_data)
        data=json.loads(received_data)
        if data.get('dtype'):
            dtype=data.get('dtype').upper()
            img_path=imagepath(dtype)
            if img_path==False:
                return error
            str_path=structurepath(dtype)
            if str_path==False:
                return error
            prgmlist=[]
            prgrsltlist=[]
            batches=Batch.objects.filter(~Q(status="active"))
            programidlist=[batch.program_id_id for batch in batches]
            bath_det=Batch.objects.all().exclude(program_id_id__in=programidlist)
            for i in bath_det:
                prgmlist.append(i.program_id_id)
            prgm_list=list(dict.fromkeys(prgmlist))
            for i in prgm_list:
                prgm_obj=Programme.objects.get(program_id=i)
                dept_obj=Department.objects.get(Department_id=prgm_obj.department_id_id)
                short_dption = prgm_obj.description
                short_title = short_dption[0:60]
                s=short_title.rsplit(' ', 1)[0]
                short_title1 = s+' ...'
                prgmDict={"program_id":prgm_obj.program_id,"program_code":prgm_obj.program_code,"title":prgm_obj.title,
                "description":prgm_obj.description,"prgtype":prgm_obj.program_type,"department_code":dept_obj.Department_code,
                "programme_Struture":prgm_obj.programme_Struture,"full_description":short_dption,"description":short_title1,
                "syllabus":prgm_obj.syllabus,"brochure":prgm_obj.brochure,"no_of_semester":prgm_obj.no_of_semester,
                "status":prgm_obj.status,"thumbnail":prgm_obj.thumbnail,"meta_tag":prgm_obj.meta_tag,"eligibility":prgm_obj.eligibility}
                prgrsltlist.append(prgmDict)
            return {"status":200,"imagepath":img_path,"structurepath":str_path,"message":prgrsltlist}
            
            

    except Exception as e:
        
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer

def upcoming_prgmlist(received_json_data):
    try:
        received_data=json.dumps(received_json_data)
        data=json.loads(received_data)
        if data.get('dtype'):
            dtype=data.get('dtype').upper()
            img_path=imagepath(dtype)
            if img_path==False:
                return error
            str_path=structurepath(dtype)
            if str_path==False:
                return error
            prgmlist=[]
            prgmslist=[]
            batch_obj=Batch.objects.filter(status="admission")
            if len(batch_obj)!=0:
                for i in batch_obj:
                    prgmslist.append(i.program_id_id)
                prgm_list=list(dict.fromkeys(prgmslist))
                for i in prgm_list:
                    prgm_obj=Programme.objects.get(program_id=i)
                    dept_obj=Department.objects.get(Department_id=prgm_obj.department_id_id)
                    short_dption = prgm_obj.description
                    short_title = short_dption[0:60]
                    s=short_title.rsplit(' ', 1)[0]
                    short_title1 = s+' ...'
                    prgmDict={"program_id":prgm_obj.program_id,"program_code":prgm_obj.program_code,"title":prgm_obj.title,
                    "description":prgm_obj.description,"prgtype":prgm_obj.program_type,"department_code":dept_obj.Department_code,
                    "programme_Struture":prgm_obj.programme_Struture,"full_description":short_dption,"description":short_title1,
                    "syllabus":prgm_obj.syllabus,"brochure":prgm_obj.brochure,"no_of_semester":prgm_obj.no_of_semester,
                    "status":prgm_obj.status,"thumbnail":prgm_obj.thumbnail,"meta_tag":prgm_obj.meta_tag,"eligibility":prgm_obj.eligibility}
                    prgmlist.append(prgmDict)
                return {"status":200,"imagepath":img_path,"structurepath":str_path,"message":prgmlist}
            else:
                return {"status":200,"message":prgmlist}


    except Exception as e:
        return internalServer
