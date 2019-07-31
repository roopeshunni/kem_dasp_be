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
from .directorate import *
from .studycentre import *
from .events import *
from .about import *
from .achievements import *
from .faq import *
from .gallery import *
from .announcements import *
from .researchPubications import *
from .news import *
from .actsall import *
from .slider import *
from .course import *
from .notify import *
from .department import *
from .course import *
from .programme import *
from .search import *
from .batch import *
from .calender import *
from .highlights import *
from .teachers import *
from .eligibility import *
from .addApplicant import *
from .admissionProgrammes import *
from .applicantExistance import *
from .applicantSelection import *
from .studentApplicantList import *

from .lms import *

from .payment import *
import jwt
from datetime import datetime,timedelta
import datetime
from rest_framework.decorators import api_view
import base64
import re
from .constants import *
#======================================================#
#                 API gateway                          #
#======================================================#
@api_view(['POST','GET','PUT'])
def api_gateway(request):    
    try:      
        uri= request.build_absolute_uri()
        req_type=uri.split('/')[-1] 

        # req_url=uri.split('/')[2]
             

        req_type=req_type.lower()
        
        # request for getting the data from the database
        if request.method=='GET':

            try:
                
                if req_type=='home':                    
                    res=get_home_update()                                                        
                    return JsonResponse(res)
                if req_type=='calendar':
                    res=get_current_calendar()
                    return JsonResponse(res)
                if req_type=='department':
                    res=get_all_department()
                    return res
                if req_type=='allbatch':
                    res=get_all_batch()
                    return res
                if req_type=='allprg':
                    res=allprogramme()
                    return res  
                if req_type=='allcalendar':
                    res=get_cal_events_programmes()
                    return res
                if req_type == 'getcourse':
                    res = courseget()
                    return res 
                if req_type=='adm_pgm':                    
                    res=get_admission_programmes()                                                         
                    return JsonResponse(res)
                if req_type=='get_all_events':                    
                    res=get_all_events()                                                         
                    return JsonResponse(res)
                if req_type=='get_all_faq':                    
                    res=get_all_faq()                                                         
                    return JsonResponse(res)

                else:
                    return JsonResponse(error)
                
            except Exception as e:
                                                             
                return JsonResponse(internalServer)
        
        
        if request.method=='POST':
            try:
                if req_type=='programme':
                    received_json_data=json.loads(request.body)
                    res=fetch_programmes(received_json_data)
                    return JsonResponse(res)
                if req_type=='programme_semester_list':
                    received_json_data=json.loads(request.body)
                    res=program_semester_list(received_json_data)
                    return res
                
                if req_type=='search':
                    received_json_data=json.loads(request.body)
                    res=search_programmes(received_json_data)
                    return JsonResponse(res)
                if req_type=='singledepartment':
                    received_json_data=json.loads(request.body)
                    res=get_a_department(received_json_data)
                    return res
                if req_type=='departmentadd':
                    received_json_data=json.loads(request.body)
                    res=department_add(received_json_data)
                    return res 
                if req_type=='departmentedit':
                    received_json_data=json.loads(request.body)
                    res=department_edit(received_json_data)
                    return res                   
                if req_type=='eventadd':
                    received_json_data=json.loads(request.body)
                    res=event_add(received_json_data)
                    return res 
                if req_type=='eventedit':
                    received_json_data=json.loads(request.body)
                    res=event_edit(received_json_data)
                    return res
                if req_type=='eventdelete':
                    received_json_data=json.loads(request.body)
                    res=event_delete(received_json_data)
                    return res
                if req_type=='eventsingle':
                    received_json_data=json.loads(request.body)
                    res=get_a_event(received_json_data)
                    return res
                if req_type=='aboutadd':
                    received_json_data=json.loads(request.body)
                    res=about_add(received_json_data)
                    return res 
                if req_type=='aboutedit':
                    received_json_data=json.loads(request.body)
                    res=about_edit(received_json_data)
                    return res
                if req_type=='getabout':
                    received_json_data=json.loads(request.body)
                    res=get_about(received_json_data)
                    return res
                
                if req_type=='addfaq':
                    received_json_data=json.loads(request.body)
                    res=add_faq(received_json_data)
                    return JsonResponse(res)

                if req_type=='singlefaq':
                    received_json_data=json.loads(request.body)
                    res=single_faq(received_json_data)
                    return JsonResponse(res)

                if req_type=='editfaq':
                    received_json_data=json.loads(request.body)
                    res=edit_faq(received_json_data)
                    return JsonResponse(res)

                if req_type=='deletefaq':
                    received_json_data=json.loads(request.body)
                    res=delete_faq(received_json_data)
                    return JsonResponse(res)
                
                if req_type=='programmeadd':
                    received_json_data=json.loads(request.body)
                    res=add_programme(received_json_data)
                    return res

                if req_type=='programmeedit':
                    received_json_data=json.loads(request.body)
                    res=edit_programme(received_json_data)
                    return res

                if req_type=='programmedelete':
                    received_json_data=json.loads(request.body)
                    res=delete_programme(received_json_data)
                    return res
                if req_type=='prg_chg_status':
                    received_json_data=json.loads(request.body)
                    res=change_status_prgm(received_json_data)
                    return res

                if req_type=='addbatch':
                    received_json_data=json.loads(request.body)
                    res=add_batch(received_json_data)
                    return JsonResponse(res)
                if req_type=='singlebatch':
                    received_json_data=json.loads(request.body)
                    res=single_batch(received_json_data)
                    return JsonResponse(res)
                if req_type=='editbatch':
                    received_json_data=json.loads(request.body)
                    res=edit_batch(received_json_data)
                    return JsonResponse(res)
                if req_type=='removebatch':
                    received_json_data=json.loads(request.body)
                    res=remove_batch(received_json_data)
                    return JsonResponse(res)
                if req_type=='batch_chg_status':
                    received_json_data=json.loads(request.body)
                    res=change_status_batch(received_json_data)
                    return res
                if req_type=='all_prg_courses':
                    received_json_data=json.loads(request.body)
                    res=get_all_prg_courses(received_json_data)
                    return res
                if req_type=='batch_course_name':
                    received_json_data=json.loads(request.body)
                    res=get_all_batch_course_name(received_json_data)
                    return res 
                if req_type=='teacher_batch':
                    received_json_data=json.loads(request.body)
                    res=teacher_batch_details(received_json_data)
                    return res 
                if req_type=='teacher_course':
                    received_json_data=json.loads(request.body)
                    res=teacher_course_details(received_json_data)
                    return res 
                if req_type=='add_couse':
                    received_json_data=json.loads(request.body)
                    res=add_all_prg_courses(received_json_data)
                    return res 
                if req_type == 'edit_couse':
                    received_json_data = json.loads(request.body)
                    res = edit_prog_course(received_json_data)
                    return (res)
                if req_type == 'retrieve_course':
                    received_json_data = json.loads(request.body)
                    res = course_details(received_json_data)
                    return res
                if req_type == 'course_pgm_mapping':
                    received_json_data = json.loads(request.body)
                    res = add_all_prg_coursepgmmapping(received_json_data)
                    return res
                if req_type == 'prg_course_list':
                    received_json_data = json.loads(request.body)
                    res = all_programme_courses_list(received_json_data)
                    return res
                if req_type == 'coursemap_delete':
                    received_json_data = json.loads(request.body)
                    res = del_all_prg_coursepgmmapping(received_json_data)
                    return res
                
                if req_type=='addeligibility':
                    received_json_data=json.loads(request.body)
                    res=add_eligibility_question(received_json_data)
                    return res

                if req_type=='singleeligibility':
                    received_json_data=json.loads(request.body)
                    res=single_eligibility_question(received_json_data)
                    return res

                if req_type=='editeligibility':
                    received_json_data=json.loads(request.body)
                    res=edit_eligibility_question(received_json_data)
                    return res
                    

                if req_type=='deleteeligibility':
                    received_json_data=json.loads(request.body)
                    res=delete_eligibility_question(received_json_data)
                    return res

                if req_type=='questionnaire':
                    received_json_data=json.loads(request.body)
                    res=fetch_questions(received_json_data)
                    return JsonResponse(res)

                if req_type=='applicantadd':
                    received_json_data=json.loads(request.body)                
                    res=add_applicant(received_json_data)                
                    return res

                if req_type=='change_status_as_student':
                    received_json_data=json.loads(request.body)
                    res=make_student(received_json_data)
                    return res

                if req_type=='checkapplicant':
                    received_json_data=json.loads(request.body)
                    res=check_applicant(received_json_data)
                    return res
                
                if req_type=='selectedlist':
                    received_json_data=json.loads(request.body)
                    res=selected_applicant(received_json_data)
                    return res 
                
                if req_type=='applicantlist':
                    received_json_data=json.loads(request.body)
                    res=get_student_applicantlist(received_json_data)
                    return res
                if req_type=='mycourses':
                    received_json_data=json.loads(request.body)
                    res=my_courses(received_json_data)
                    return res
                if req_type=='adm_pgm_batch':
                    received_json_data=json.loads(request.body)
                    res=get_admission_pgm_batch(received_json_data)
                    return res

                if req_type=='paymentrequest':
                    received_json_data=json.loads(request.body)
                    payment_res=payment_redirection(received_json_data)
                    return payment_res

                if req_type=='paymentresponse':
                    res=payment_response(request)
                    return res

                if req_type=='paymentreceipt':
                    received_json_data=json.loads(request.body)
                    payment_res=payment_receipt(received_json_data)
                    return payment_res
                if req_type=='paymenthistory':
                    received_json_data=json.loads(request.body)
                    res=payment_history(received_json_data)
                    return JsonResponse(res)

                if req_type=='prgm_payment_det':
                    received_json_data=json.loads(request.body)
                    res=get_prgm_paymentdetails(received_json_data)
                    return JsonResponse(res)

                if req_type=='ongoing_prgm':
                    received_json_data=json.loads(request.body)
                    res=get_ongoing_prgms(received_json_data)
                    return JsonResponse(res)

                if req_type=='upcoming_prgmlist':
                    received_json_data=json.loads(request.body)
                    res=upcoming_prgmlist(received_json_data)
                    return JsonResponse(res)
                if req_type=="user_list":
                    received_json_data=json.loads(request.body)
                    res=student_list(received_json_data)
                    return JsonResponse(res)
                if req_type=="student_check":
                    received_json_data=json.loads(request.body)
                    res=student_check(received_json_data)
                    return JsonResponse({"isStud":res})

                if req_type == "lms_teacher_courselist":
                    received_json_data = json.loads(request.body)
                    res = get_all_teacher_prg_courses(received_json_data)
                    return JsonResponse(res)

                if req_type == "get_all_payment_details":
                    received_json_data = json.loads(request.body)
                    res = get_payment_details(received_json_data)
                    return JsonResponse(res)

                if req_type=="payment_status":
                    received_json_data=json.loads(request.body)
                    if received_json_data.get('orderId') and received_json_data.get('status'):
                        res=payment_status(received_json_data.get('orderId'),received_json_data.get('status'))
                    else:
                        return JsonResponse(error)


                



                else:
                    return JsonResponse(error)

            except Exception as e:                                             
                return JsonResponse(internalServer)
                   
    except Exception as e:      
        return JsonResponse({"message":"Bad Gateway"},safe=False)

#======================================================#
#  function for get all information for home page      #
#======================================================#
def get_home_update():

    # getting all the programme list
    prgm_res=get_all_upcoming_programmes()
    prgm_rec_data=json.dumps(prgm_res)
    prgm_parsed_data=json.loads(prgm_rec_data)
    status=prgm_parsed_data.get("status")
    if status==200:
        prgm_resp=prgm_parsed_data.get("message")
    else:
        return internalServer

    # getting all the faq
    # faq_res=get_all_faq()
    # faq_rec_data=json.dumps(faq_res)
    # faq_parsed_data=json.loads(faq_rec_data)
    # status=faq_parsed_data.get("status")
    # if status==200:
    #     faq_resp=faq_parsed_data.get("message")
    # else:
    #     return internalServer 

    result={"status":200,'message':{'programmes':prgm_resp}}
    return result
def get_home():    
    # getting all the directorate info
    dir_res=get_directorate()
    dir_rec_data=json.dumps(dir_res)
    dir_parsed_data=json.loads(dir_rec_data)
    status=dir_parsed_data.get("status")
    if status==200:
        dir_resp=dir_parsed_data.get("message")
    else:
        return internalServer
        
    # getting all the studycentre info 
    ss_res=get_all_studycentre()
    ss_rec_data=json.dumps(ss_res)
    ss_parsed_data=json.loads(ss_rec_data)
    status=ss_parsed_data.get("status")
    if status==200:
        ss_resp=ss_parsed_data.get("message")
    else:
        return internalServer
    
    # getting all the programme list
    prgm_res=get_all_upcoming_programmes()
    prgm_rec_data=json.dumps(prgm_res)
    prgm_parsed_data=json.loads(prgm_rec_data)
    status=prgm_parsed_data.get("status")
    if status==200:
        prgm_resp=prgm_parsed_data.get("message")
    else:
        return internalServer

    # getting all the events list
    evt_res=get_all_events()
    evt_rec_data=json.dumps(evt_res)
    evt_parsed_data=json.loads(evt_rec_data)
    status=evt_parsed_data.get("status")
    if status==200:
        evt_resp=evt_parsed_data.get("message")
    else:
        return internalServer 

    # getting all the achievements list
    ach_res=get_all_achievements()
    ach_rec_data=json.dumps(ach_res)
    ach_parsed_data=json.loads(ach_rec_data)
    status=ach_parsed_data.get("status")
    if status==200:
        ach_resp=ach_parsed_data.get("message")
    else:
        return internalServer

    # getting all the aboutus info
    abt_res=get_all_about()
    abt_rec_data=json.dumps(abt_res)
    abt_parsed_data=json.loads(abt_rec_data)
    status=abt_parsed_data.get("status")
    if status==200:
        abt_resp=abt_parsed_data.get("message")
    else:
        return internalServer 

    # # getting all the gallery photos
    # url_gal=gallery
    # resp_gal = requests.get(url_gal)
    # res_gal=json.loads(resp_gal.text)
    
    # getting all the faq
    faq_res=get_all_faq()
    faq_rec_data=json.dumps(faq_res)
    faq_parsed_data=json.loads(faq_rec_data)
    status=faq_parsed_data.get("status")
    if status==200:
        faq_resp=faq_parsed_data.get("message")
    else:
        return internalServer 
    
    # getting all the announcements
    ann_res=get_all_announcement()
    ann_rec_data=json.dumps(ann_res)
    ann_parsed_data=json.loads(ann_rec_data)
    status=ann_parsed_data.get("status")
    if status==200:
        ann_resp=ann_parsed_data.get("message")
    else:
        return internalServer
          
    # getting all the research
    research_res=get_all_research()
    research_rec_data=json.dumps(research_res)
    research_parsed_data=json.loads(research_rec_data)
    status=research_parsed_data.get("status")
    if status==200:
        research_resp=research_parsed_data.get("message")
    else:
        return internalServer
    
    # getting all the acts and regulations 
    act_res=get_all_act()
    act_rec_data=json.dumps(act_res)
    act_parsed_data=json.loads(act_rec_data)
    status=act_parsed_data.get("status")
    if status==200:
        act_resp=act_parsed_data.get("message")
    else:
        return internalServer 
    # getting all the slider images
    slider_res=get_all_act()
    slider_rec_data=json.dumps(slider_res)
    slider_parsed_data=json.loads(slider_rec_data)
    status=slider_parsed_data.get("status")
    if status==200:
        slider_resp=slider_parsed_data.get("message")
    else:
        return internalServer

    # getting all the notifications
    noti_res= get_all_notification()
    noti_rec_data=json.dumps(noti_res)
    noti_parsed_data=json.loads(noti_rec_data)
    status=noti_parsed_data.get("status")
    if status==200:
        noti_resp=noti_parsed_data.get("message")
    else:
        return internalServer 

    # to get programmes highlights
    high_res=get_all_highlights()
    high_rec_data=json.dumps(high_res)
    high_parsed_data=json.loads(high_rec_data)
    status=high_parsed_data.get("status")
    if status==200:
        high_resp=high_parsed_data.get("message")
    else:
        return internalServer 

    result={"status":200,'message':{"directorate":dir_resp,'studycentre':ss_resp,'programmes':prgm_resp,
    'events':evt_resp,'achievements':ach_resp,'about':abt_resp,'faq':faq_resp,'announcements':ann_resp,
    'research':research_resp,'acts':act_resp,'sliders':slider_resp,'notifications':noti_resp,'highlights':high_resp}}
    return result

#=============================================#
#  function for get all and single programme  #
#=============================================#
def fetch_programmes(received_json_data):    
    re_prgm=get_all_programme(received_json_data)
    re_rec_data=json.dumps(re_prgm)
    re_parsed_data=json.loads(re_rec_data)
    if re_parsed_data.get('status')==200:
        data=re_parsed_data.get('message')
        image_path=re_parsed_data.get('imagepath')
        struct_path=re_parsed_data.get('structurepath')
        result_data={"data":data,'imagepath':image_path,'structurepath':struct_path}
        result={"status":200,'message':result_data}
        return result
    else:
        return re_parsed_data


#=============================================#
#  function for get  any single programme     #
#=============================================#
def get_current_calendar():
    cal_res=get_current_cal_events()
    cal_rec_data=json.dumps(cal_res)
    cal_parsed_data=json.loads(cal_rec_data)
    status=cal_parsed_data.get("status")
    if status==200:
        cal_resp=cal_parsed_data.get("message")
    else:
        return internalServer
    result={'status':200,'message':cal_resp}
    return result 

#=============================================#
#         function for programme search       #
#=============================================#
def search_programmes(received_json_data):
    ser_prgm=search_programme(received_json_data)
    ser_rec_data=json.dumps(ser_prgm)
    ser_parsed_data=json.loads(ser_rec_data)
    if ser_parsed_data.get('status')==200:
        data=ser_parsed_data.get('message')
        image_path=ser_parsed_data.get('imagepath')
        struct_path=ser_parsed_data.get('structurepath')
        ser_result_data={"data":data,'imagepath':image_path,'structurepath':struct_path}
        result={"status":200,'message':ser_result_data}
        return result
    else:
        return ser_parsed_data

#=============================================#
#  function for get  any single programme     #
#=============================================#
def fetch_questions(received_json_data):    
    eligibility_prgm=get_prgm_eligibility_questions(received_json_data)
    eligibility_rec_data=json.dumps(eligibility_prgm)
    eligibility_parsed_data=json.loads(eligibility_rec_data)
    if eligibility_parsed_data.get('status')==200:
        data=eligibility_parsed_data.get('message')
        result={"status":200,'message':data}
        return result
    else:
        return eligibility_parsed_data

            
