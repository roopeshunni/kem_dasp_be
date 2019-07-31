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


#==============================================#
#          CONSTANTS DECLARATION STARTS        #
#==============================================#
p_id="pid"
qst='question'
ans='answer'
elg_id='elg_id'
is_mand='is_mandatory'
bad_request={"status":400,"message":"Bad request"}
int_ser_err={"status":500,"message":"Internal Server Error"}
qst_empty={"status":404,"message":"Question is empty"}
qst_exist={"status":409,"message":"Question already exist"}
pgm_invalid={"status":404,"message":"Invalid programme id"}
ans_invalid={"status":422,"message":"Invalid answer"}
mand_invalid={"status":422,"message":"Mandatory field is invalid"}
result={"status":200,"message":"Successfully added new eligibility question"}
elg_invalid={"status":409,"message":"Eligibility question does not exist"}
elg_result={"status":200,"message":"Successfully updated eligibility question"}
delete_result={"status":200,"message":"Successfully deleted eligibility question"}
#==============================================#
#           CONSTANTS DECLARATION ENDS         #
#==============================================#


# #========================================================#
# # function for get eligibility question for a programme  #
# #========================================================#
def get_prgm_eligibility_questions(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('pid'):
            program_id=data.get('pid')
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
                queryset=ProgramEligibility.objects.filter(program_id_id=prg_id)
                eligibilityDict={}
                elians={}
                for i in queryset:
                    eligibilityDict[i.eligibility_id]=i.eligibility_question
                    elians[i.eligibility_id]=i.default_answer 
                result={"prgid":program_id,"questions":eligibilityDict,"answer":elians,"ProgramDetails":programdict,"BatchDetails":batchlist}
                return {"status":200,"message":result}
        else:
            return error
    except Exception as e:
       
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer

#========================================================#
#      Adding a new eligibility question into table      #
#========================================================#

def add_eligibility_question(recieved_json):
    try:
        eligibility_rec_data=json.dumps(recieved_json)
        eligibility_parsed_data=json.loads(eligibility_rec_data)
        if eligibility_parsed_data.get(qst) and  eligibility_parsed_data.get(p_id) and ans in eligibility_parsed_data  and is_mand in eligibility_parsed_data:
            pgm_id=eligibility_parsed_data.get(p_id)
            program_existance=Programme.objects.filter(program_id=pgm_id)                       
            if len(program_existance)==0:
                return JsonResponse(pgm_invalid)                                  
            eligibility_question=eligibility_parsed_data.get(qst)
            empty_question=eligibility_question.replace(" ","")
            if len(empty_question)==0 :
                return JsonResponse(qst_empty)
            eligibility_answer=eligibility_parsed_data.get(ans)   
            if eligibility_answer != True and eligibility_answer != False: 
                return JsonResponse(ans_invalid)
            eligibility_mandatory=eligibility_parsed_data.get(is_mand)
            if eligibility_mandatory!=True and eligibility_mandatory!=False:
                return JsonResponse(mand_invalid)
            
            prgm_existance=ProgramEligibility.objects.filter(program_id_id=pgm_id,eligibility_question=eligibility_question)            
            if len(prgm_existance)==1:
                return JsonResponse(qst_exist)            
                                  
            new_eligibility_question=ProgramEligibility(eligibility_question=eligibility_question,default_answer=eligibility_answer,is_mandatory=eligibility_mandatory,program_id_id=pgm_id)
            new_eligibility_question.save()
            return JsonResponse(result)
        
        else:
            return JsonResponse(bad_request)
    except Exception as e: 
        print(e)
        return JsonResponse(int_ser_err)

# Single fetching of eligibility question under a particular programme
def single_eligibility_question(recieved_json):
    try:
        recieved_data=json.dumps(recieved_json)
        eligibility_parsed_data=json.loads(recieved_data)
        if  eligibility_parsed_data.get(elg_id) and eligibility_parsed_data.get(p_id):
            pgm_id=eligibility_parsed_data.get(p_id)
            program_existance=Programme.objects.filter(program_id=pgm_id)                        
            if len(program_existance)==0:
                return JsonRespose(pgm_invalid)            
            el_id=eligibility_parsed_data.get(elg_id)            
            
            programme=ProgramEligibility.objects.filter(program_id_id=pgm_id,eligibility_id=el_id) 
            if len(programme)==0:
                return JsonResponse(elg_invalid)
            programmeResultList=[]
            for pgm in programme:
                pgmDict = {"id" : pgm.eligibility_id,"question" : pgm.eligibility_question,"answer":pgm.default_answer,"is_mandatory":pgm.is_mandatory}
                programmeResultList.append(pgmDict)
            return JsonResponse({"status":200,"message":programmeResultList})
        elif eligibility_parsed_data.get(p_id):
            pgm_id=eligibility_parsed_data.get(p_id)
            program_existance=Programme.objects.filter(program_id=pgm_id)                        
            if len(program_existance)==0:
                return JsonRespose(pgm_invalid)
            programmeEligibilityList=[] 
            programme=ProgramEligibility.objects.filter(program_id_id=pgm_id)           
            for elobj in programme:
                eli_id=elobj.eligibility_id
                ques=elobj.eligibility_question
                ans=elobj.default_answer
                mandatory=elobj.is_mandatory
                elidict={"pgmid":pgm_id,"id":eli_id,"question":ques,"answer":ans,"is_mandatory":mandatory}
                programmeEligibilityList.append(elidict)
            return JsonResponse({"status":200,"message":programmeEligibilityList})
        else:
            return JsonResponse(bad_request)

    except Exception as e:          
        return JsonResponse(int_ser_err)

 # Editing an exisiting eligibility question 
def edit_eligibility_question(recieved_json):
    try:
        eligibility_rec_data=json.dumps(recieved_json)
        eligibility_parsed_data=json.loads(eligibility_rec_data)
        if eligibility_parsed_data.get(qst) and  eligibility_parsed_data.get(p_id) and eligibility_parsed_data.get(elg_id) and ans in eligibility_parsed_data  and is_mand in eligibility_parsed_data:
            pgm_id=eligibility_parsed_data.get(p_id)
            program_existance=Programme.objects.filter(program_id=pgm_id)                        
            if len(program_existance)==0:
                return JsonRespose(pgm_invalid)            
            el_id=eligibility_parsed_data.get(elg_id)                    
            eligibility_question=eligibility_parsed_data.get(qst)
            empty_question=eligibility_question.replace(" ","")
            if len(empty_question)==0 :
                return JsonResponse(qst_empty)
            eligibility_answer=eligibility_parsed_data.get(ans)
            
            if eligibility_answer != True and eligibility_answer != False: # or eligibility_answer != False: #or not eligibility_answer:# or eligibility_answer!=0:
                return JsonResponse(ans_invalid)
            eligibility_mandatory=eligibility_parsed_data.get(is_mand)
            
            if eligibility_mandatory!=True and eligibility_mandatory!=False:
                return JsonResponse(mand_invalid)

            elg_exsistance=ProgramEligibility.objects.filter(eligibility_question=eligibility_question,program_id_id=pgm_id).exclude(eligibility_id=el_id)
            if len(elg_exsistance)>0:
                return JsonResponse(qst_exist)        
            
            ProgramEligibility.objects.filter(eligibility_id=el_id).update(eligibility_question=eligibility_question,default_answer=eligibility_answer,is_mandatory=eligibility_mandatory)            
            return JsonResponse(elg_result)
        
        else:
            return JsonRespone(bad_request)
    except Exception as e:
        # print(e)            
        return JsonResponse(int_ser_err)

 # deleting an exisiting eligibility question 
def delete_eligibility_question(recieved_json):
    try:
        recieved_data=json.dumps(recieved_json)
        eligibility_parsed_data=json.loads(recieved_data)
       
        if  eligibility_parsed_data.get(elg_id) and eligibility_parsed_data.get(p_id):
            pgm_id=eligibility_parsed_data.get(p_id)
            program_existance=Programme.objects.filter(program_id=pgm_id)                        
            if len(program_existance)==0:
                return JsonResponse(pgm_invalid)
            batches=Batch.objects.filter(program_id_id=pgm_id).exclude(status="hide")
            if batches.count()!=0:
                return JsonResponse({"status": 200, "message": "Batch exist,can't delete eligibility questions"})            
            el_id=eligibility_parsed_data.get(elg_id)            
            
            programme=ProgramEligibility.objects.filter(program_id_id=pgm_id,eligibility_id=el_id) 
            if len(programme)==0:
                return JsonResponse(elg_invalid)
            del_elg=ProgramEligibility.objects.filter(eligibility_id=el_id).delete()
            return JsonResponse(delete_result)
    except Exception as e:       
        return JsonResponse(int_ser_err)