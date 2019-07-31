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
import time
from .constants import *
#==============================================#
#          CONSTANTS DECLARATION STARTS        #
#==============================================#
faq_id="f_id"
qst='question'
ans='answer'
bad_request={"status":400,"message":"Bad request"}
int_ser_err={"status":500,"message":"Internal Server Error"}
result={"status":200,"message":"Successfully added new faq"}
qst_empty={"status":404,"message":"Question is empty"}
ans_empty={"status":404,"message":"Answer is empty"}
qst_exist={"status":409,"message":"Question already exist"}
faq_invalid={"status":404,"message":"Faq does not exist"}
edit_result={"status":200,"message":"Successfully updated faq"}
delete_result={"status":200,"message":"Successfully deleted faq"}

#==============================================#
#           CONSTANTS DECLARATION ENDS         #
#==============================================#

#==========================================#
#     function for get all FAQ details     #
#==========================================#
def get_all_faq():
    try:
        queryset=Faq.objects.values('faq_id','question','answer')
        singlecountryDict1=[]
        for i in queryset:
            singlecountryDict = {"id" : i['faq_id'],"question" : i['question'],"answer":i['answer']}
            singlecountryDict1.append(singlecountryDict)
        # return 
        s={"status":200,"message":singlecountryDict1}
        return s


    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer 

#==========================================#
#     function for add new  FAQ details    #
#==========================================#
def add_faq(recieved_json):
    try:
        faq_rec_data=json.dumps(recieved_json)
        faq_parsed_data=json.loads(faq_rec_data)
        if faq_parsed_data.get(qst) and faq_parsed_data.get(ans) : #  or len(faq_parsed_data.get(qst))==0 and len(faq_parsed_data.get(ans))==0:
            new_question=faq_parsed_data.get(qst)
            empty_question=new_question.replace(" ","")
            if len(empty_question)==0 :
                return qst_empty
            
            new_answer=faq_parsed_data.get(ans)
            empty_answer=new_answer.replace(" ","")
            if len(empty_answer)==0:
                return ans_empty
            faq_existance=Faq.objects.filter(question=new_question)
            if len(faq_existance)==1:
                return qst_exist                        
            

            new_faq=Faq(question=new_question,answer=new_answer)
            new_faq.save()
            return result
        
        else:
            return bad_request
    except Exception as e:            
            return int_ser_err

#==========================================#
#     function for get single FAQ details  #
#==========================================#
def single_faq(recieved_json):
    try:
        recieved_data=json.dumps(recieved_json)
        parsed_data=json.loads(recieved_data)
        if  parsed_data.get(faq_id):
            f_id=parsed_data.get(faq_id)
            faq=Faq.objects.filter(faq_id=f_id)
            if len(faq)==0:
                return faq_invalid

            faqResultList=[]
            for i in faq:
                faqDict = {"id" : i.faq_id,"question" : i.question,"answer":i.answer}
                faqResultList.append(faqDict)
            return {"status":200,"message":faqResultList}
        else:
            return bad_request

    except Exception as e:            
            return int_ser_err

#==========================================#
#     function for edit FAQ details        #
#==========================================#
def edit_faq(recieved_json):
    try:
        faq_rec_data=json.dumps(recieved_json)
        faq_parsed_data=json.loads(faq_rec_data)

        if faq_parsed_data.get(qst) and faq_parsed_data.get(ans) and faq_parsed_data.get(faq_id): #  or len(faq_parsed_data.get(qst))==0 and len(faq_parsed_data.get(ans))==0:
            f_id=faq_parsed_data.get(faq_id)
            faq_existance=Faq.objects.filter(faq_id=f_id)
            if len(faq_existance)==0:
                return faq_invalid
            edit_question=faq_parsed_data.get(qst)
            empty_question=edit_question.replace(" ","")
            if len(empty_question)==0 :
                return qst_empty
            edit_answer=faq_parsed_data.get(ans)
            empty_answer=edit_answer.replace(" ","")
            if len(empty_answer)==0:
                return ans_empty
            faq_existance=Faq.objects.filter(question=edit_question).exclude(faq_id=f_id)
            if len(faq_existance)>0:
                return qst_exist                        
            #faq_existance=Faq.objects.filter(faq_id=f_id,question=edit_question)
            #print(len(faq_existance))
            #if len(faq_existance)==0:
            #    return faq_invalid

            Faq.objects.filter(faq_id=f_id).update(question=edit_question,answer=edit_answer)
            #new_faq.save()
            return edit_result
        
        else:
            return bad_request
    except Exception as e:
            print(e)            
            return int_ser_err
#==========================================#
#     function for delete FAQ details      #
#==========================================#

def delete_faq(recieved_json):
    try:
        recieved_data=json.dumps(recieved_json)
        parsed_data=json.loads(recieved_data)
        if  parsed_data.get(faq_id):
            f_id=parsed_data.get(faq_id)
            faq=Faq.objects.filter(faq_id=f_id)
            if len(faq)==0:
                return faq_invalid
            del_faq=Faq.objects.filter(faq_id=f_id).delete()
            return delete_result
            

    except Exception as e:            
            return int_ser_err
    
