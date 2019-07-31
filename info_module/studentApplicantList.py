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
from datetime import datetime as dt
from datetime import timedelta 
from .constants import *
from django.db.models import Subquery,F

#=====================================================================================#
# function for listing out all the applicants and their status of a particular batch  #
#=====================================================================================#


def get_student_applicantlist(received_json_data):
	try:
		data1=json.dumps(received_json_data)
		data=json.loads(data1)
		batch_id=int(data.get('batch_id'))
		if data.get('batch_id'):
			batchobj = Batch.objects.filter(batch_id=data.get('batch_id'))
			batchobj_list=list(batchobj)
			if len(batchobj_list)==0:
				return JsonResponse({"status":404,"message":"Invalid batch id"})
			else:
				
				
				student_applicantobj = StudentApplicants.objects.select_related('batch_id_id','program_id_id').values('batch_id','batch_id_id__batch_name','program_id_id__title','program_id_id__program_code','user_id','applied_date','applicant_status','applicant_id','is_paid').filter(user_id__in=Subquery(StudentApplicants.objects.filter(batch_id_id=data.get('batch_id')).values('user_id')))#.exclude(batch_id=data.get('batch_id'))
				list1=list(student_applicantobj)
				
				total_applicant=len(list(filter(lambda x:x.get("batch_id")==batch_id,list1)))
				user_id_list=set(list(map(lambda x: x.get("user_id"),list1)))
				userslist=[]
				
				for j in user_id_list:
					
					list2=list(filter(lambda x:((x.get("user_id")==j) and (x.get("batch_id")!=batch_id)),list1))
					o_list=[]
					
					for k in list2:
						
							olist1={"batch_name":k.get("batch_id_id__batch_name"),"programme_name":k.get("program_id_id__title"),"programme_code":k.get("program_id_id__program_code"),"user_id":k.get("user_id"),"applied_date":dt.strftime(k.get("applied_date"),"%Y-%m-%d"),"applied_time":dt.strftime(k.get("applied_date"),'%H:%M:%S'),
							"status":k.get("applicant_status"),"applicantid":k.get("applicant_id"),"is_paid":k.get("is_paid")}
							o_list.append(olist1)
					
					
					current_user=list(filter(lambda x:((x.get("user_id")==j) and (x.get("batch_id")==batch_id)),list1))[0]
					
					p_code_list=set(list(map(lambda x:x.get("programme_code"),o_list)))
					p_code=", ".join(p_code_list)
					dict4 = {"user_id":current_user.get("user_id"),"applied_date":dt.strftime(current_user.get("applied_date"),"%Y-%m-%d"),"applied_time":dt.strftime(current_user.get("applied_date"),'%H:%M:%S'),
					"status":current_user.get("applicant_status"),"applicantid":current_user.get("applicant_id"),"is_paid":current_user.get("is_paid"),"other_batch":o_list,"other_prg_code":p_code}
					userslist.append(dict4)
				mainlist=[]
				
				for i in batchobj_list:
					dict1={"seat_no":i.no_of_seats,"No_of_Applicants":total_applicant,"application_start_date":i.appli_start_date,
						"application_end_date":i.appli_end_date,"pgm_start_date":i.prgm_start_date,
						"pgm_end_date":i.prgm_end_date,"Fees":i.program_fee,"programme_name":i.program_id.title,
						"programme_code":i.program_id.program_code}
					mainlist.append(dict1)
				dict3={"batch":dict1,"Users":userslist}		
				return JsonResponse({"status":200,"message":dict3})

				
		else:
			return JsonResponse(error)
	except Exception as e:
		print(e)
		# err={"status":500,"message":"Internal Server Error"}
		return JsonResponse(internalServer)




# def get_student_applicantlist(received_json_data):
# 	try:
# 		data1=json.dumps(received_json_data)
# 		data=json.loads(data1)
# 		if data.get('batch_id'):
# 			batchobj = Batch.objects.filter(batch_id=data.get('batch_id'))
# 			if batchobj.count()==0:
# 				return JsonResponse({"status":404,"message":"Invalid batch id"})
# 			else:
# 				for i in batchobj:
# 					student_applicantobj = StudentApplicants.objects.filter(batch_id_id=data.get('batch_id'))
# 					list1=[]
# 					dict2=[]

# 					for j in student_applicantobj:
# 						other_list=StudentApplicants.objects.filter(user_id=j.user_id).exclude(batch_id_id=j.batch_id)
# 						o_list=[]
# 						prg_code=[]
# 						for k in other_list:
# 							olist1={"batch_name":k.batch_id.batch_name,"programme_name":k.program_id.title,"programme_code":k.program_id.program_code,"user_id":k.user_id,"applied_date":k.applied_date.date(),"applied_time":k.applied_date.time(),
# 							"status":k.applicant_status,"applicantid":k.applicant_id,"is_paid":k.is_paid}
# 							o_list.append(olist1)
# 							prg_code.append(k.program_id.program_code)
# 						other_prg_code=list(dict.fromkeys(prg_code))
# 						p_code=(", ".join(other_prg_code))
# 						dict4 = {"user_id":j.user_id,"applied_date":j.applied_date.date(),"applied_time":j.applied_date.time(),
# 						"status":j.applicant_status,"applicantid":j.applicant_id,"is_paid":j.is_paid,"other_batch":o_list,"other_prg_code":p_code}
# 						list1.append(dict4)
# 					dict1={"seat_no":i.no_of_seats,"No_of_Applicants":len(list1),"application_start_date":i.appli_start_date,
# 					"application_end_date":i.appli_end_date,"pgm_start_date":i.prgm_start_date,
# 					"pgm_end_date":i.prgm_end_date,"Fees":i.program_fee,"programme_name":i.program_id.title,
# 					"programme_code":i.program_id.program_code}
# 					dict3={"batch":dict1,"Users":list1}					
# 				return JsonResponse({"status":200,"message":dict3})
# 		else:
# 			return JsonResponse(error)
# 	except Exception as e:
		
# 		# err={"status":500,"message":"Internal Server Error"}
# 		return JsonResponse(internalServer)



# def student_list(received_json_data):
# 	try:
# 		received_date=json.dumps(received_json_data)
# 		r_date=json.loads(received_date)
# 		if r_date.get('purpose') and r_date.get('user_list'):
# 			purpose=r_date.get('purpose')
# 			user_list=r_date.get('user_list')
# 			applResultList=[]
# 			regResultList=[]
# 			resultDic={}
# 			for singleuser in user_list:
				
# 				user_id=singleuser.get("user_id")
# 				studentAppl=StudentApplicants.objects.filter(user_id=user_id)
# 				if studentAppl.count()!=0:
# 					for stud in studentAppl:				
# 						prg=Programme.objects.get(program_id=stud.program_id_id)
# 						batch=Batch.objects.get(batch_id=stud.batch_id_id)
# 						resultDic={"batch_name":batch.batch_name,"prg_name":prg.title,"name":singleuser.get('user_name'),"user_id":singleuser.get('user_id'),
# 						"email":singleuser.get('email'),"phno":singleuser.get('phno'),"nationality":singleuser.get('nationality')}						
# 						applResultList.append(resultDic)
					
# 				else:
# 					resultDic={"name":singleuser.get('user_name'),"user_id":singleuser.get('user_id'),
# 						"email":singleuser.get('email'),"phno":singleuser.get('phno'),"nationality":singleuser.get('nationality')}
						
# 					regResultList.append(resultDic)
# 			if purpose.lower()=="a":
# 				return {"status":200,"message":applResultList,"purpose":purpose.lower()}
# 			else:
				
# 				return {"status":200,"message":regResultList,"purpose":purpose.lower()}

			
# 		else:
# 			return JsonResponse(error)

# 	except Exception as e:
# 		return JsonResponse(internalServer)

def student_list(received_json_data):
	try:
		
		received_data=json.dumps(received_json_data)
		r_data=json.loads(received_data)
		if r_data.get('purpose'):
			
			purpose=r_data.get('purpose')
			start_date=r_data.get('start_date')
			st_date=dt.strptime(start_date, '%Y-%m-%d')
			end_date=r_data.get('end_date')
			en_date=dt.strptime(end_date, '%Y-%m-%d')
			e_date=en_date+timedelta(days=1)
			
			if purpose.lower()=="a":
				applResultList=[]
				resultDic={}
				t=dt.now()
				studentAppl=StudentApplicants.objects.select_related('batch_id', 'program_id').filter(applied_date__range=(st_date, e_date)).exclude(applicant_status="canceled")
				
				
				
				if studentAppl.count()!=0:
					for stud in studentAppl:				
					
						resultDic={"batch_name":stud.batch_id.batch_name,"prg_name":stud.program_id.title,"user_id":stud.user_id}					
						applResultList.append(resultDic)
					
					# applResultList=list(map(lambda x:x.__dict__,studentAppl))
					# print("applResultList")
				
				
				return {"message":applResultList,"purpose":purpose.lower()}
			elif purpose.lower()=="c":
				applResultList=[]
				resultDic={}
				studentAppl=StudentApplicants.objects.filter(applied_date__range=(st_date, en_date),applicant_status="canceled")
				if studentAppl.count()!=0:
					for stud in studentAppl:				
						prg=Programme.objects.get(program_id=stud.program_id_id)
						batch=Batch.objects.get(batch_id=stud.batch_id_id)
						resultDic={"batch_name":batch.batch_name,"prg_name":prg.title,"user_id":stud.user_id}					
						applResultList.append(resultDic)
					
				return {"message":applResultList,"purpose":purpose.lower()}			
		else:
			return JsonResponse(error)

	except Exception as e:
		
		return JsonResponse(internalServer)

