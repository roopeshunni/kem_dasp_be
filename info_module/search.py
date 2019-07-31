from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import *
from django.http import JsonResponse
import datetime
import json
from .constants import *
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

#======================================================================#
#  function for getting all  programmes related to the search keyword  #
#======================================================================#
def search_programme(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('keyword'):
            if data.get('dtype'):
                keyword1 = data.get('keyword')
                dtype=data.get('dtype').upper()                  
                img_path=imagepath(dtype)
                if img_path==False:
                    return error
                str_path=structurepath(dtype)
                if str_path==False:
                    return error                 
                keyword1=keyword1.replace(" ", "")
                if keyword1=="":
                    return {"status":200,"message":"No results found"}
                    # Remove white space for easy search
                keyword2 = keyword1.lower() # make it lower case when admin creates a programme
                
                programData = Programme.objects.all()
                keyDict1 = [] 
                for i in programData:
                    list1=[]
                    short_dption = i.description
                    short_title = short_dption[0:60]
                    s=short_title.rsplit(' ', 1)[0]
                    short_title1 = s+' ...'
                    batchobj = Batch.objects.filter(program_id=i.program_id).exclude(status="hide")
                    for jb in batchobj:
                        studycentre_id = jb.study_centre_id_id
                        studycentre_details = studycentre.objects.get(studycentre_id=studycentre_id)
                        dict1={"batch_id":jb.batch_id,"study_Centre":studycentre_details.name,'batch_name':jb.batch_name,
                        'application_start_date':str(jb.appli_start_date),'application_end_date':str(jb.appli_end_date),
                        'programme_start_date':str(jb.prgm_start_date),'programme_end_date':str(jb.prgm_end_date),'Fees':jb.program_fee,
                        'status':jb.status,"seats":jb.no_of_seats}
                        list1.append(dict1)
                    metaTag = i.meta_tag.split(',')
                    for j in metaTag:
                        if keyword2 in j.lower():
                            keydict={"id":i.program_id,"program_code":i.program_code,"title":i.title,"description":short_title1,"full_description":i.description,"department_id":i.department_id_id,"Structure":i.programme_Struture,"status":i.status,
                            "thumbnail":i.thumbnail,"eligibility":i.eligibility,"syllabus":i.syllabus,"brochure":i.brochure,"batchdetails":list1,"departmentcode":i.department_id.Department_code}
                            keyDict1.append(keydict)
                if not keyDict1:
                    return {"status":200,"message":"No results found"}
                else:             
                    unique_stuff = { each['id'] : each for each in keyDict1 }.values()
                    return {"status":200,"imagepath":img_path,"structurepath":str_path,"message":list(unique_stuff)}
            else:
                return error  
        else:
                return error          
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer