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
from datetime import datetime as dt
import random
from django.db.models import Subquery
import time
from .constants import *

#==============================================#
#          CONSTANTS DECLARATION STARTS        #
#==============================================#
p_id="pgm_id"
b_id="b_id"
b_name='b_name'
d_id="dpt_id"
s_id="std_id"
p_fee="pgm_fee"
no_seats="no_seats"
apl_st_date='appl_start_date'
apl_en_date='appl_end_date'
pgm_st_date='class_start_date'
pgm_en_date='class_end_date'
batch_dis_name="batch_dis_name"



STATUS='Inactive'
dt_format="%Y-%m-%d"

invalid_pgm={"status":404,"message":"Invalid programme id"}
invalid_course={"status":404,"message":"Please add course for this programme"}
invalid_dpt={"status":404,"message":"Invalid department id"}
invalid_std={"status":404,"message":"Invalid studycentre id"}
invalid_seats={"status":404,"message":"Invalid no.of seats"}
invalid_fee={"status":404,"message":"Invalid fee"}
invalid_apl_date={"status":400,"message":"Application end date never be less than or equal to application start date"}
invalid_cls_date={"status":400,"message":"Class end date is never be less than or equal to class start date"}
invalid_pg_date={"status":400,"message":"You can't start the class before closing the application"}
invalid_st_en_date={"status":400,"message":"Application start date and end date is equal"}
invalid_en_apl_date={"status":400,"message":"Class start date never be equal to application end date"}
invalid_pg_st_en_date={"status":400,"message":"Class start date and end date never be equal"}
bat_exist={"status":409,"message":"Batch already exist"}
bad_request={"status":400,"message":"Bad request"}
int_ser_err={"status":500,"message":"Internal Server Error"}
err_result={"status":304,"message":"Data is not updated.Please try again"}
result={"status":200,"message":"Successfully added a new batch"}
edit_result={"status":200,"message":"Successfully updated the batch"}


invalid_batch={"status":404,"message":"There is no such batch exist"}

#==============================================#
#           CONSTANTS DECLARATION ENDS         #
#==============================================#

#============================================#
#  function for get all upcoming programmes  #
#============================================#
# def get_all_upcoming_programmes():
# 	try:
# 		batchobj = Batch.objects.filter(status="Inactive")
# 		if batchobj.count()==0:
# 			return JsonResponse({"status":404,"message":"No upcoming programmes" })
# 		else:
# 			programmeData= Programme.objects.all()
# 			dict3=[]
# 			for i in programmeData:
# 				pgm_id = i.program_id
# 				batchpgmData = Batch.objects.filter(program_id=pgm_id,status="Inactive")
# 				list1=[]
# 				for j in batchpgmData:
# 					studycentre_id = j.study_centre_id_id
# 					studycentre_details = studycentre.objects.get(studycentre_id=studycentre_id)
# 					dict1={"batch_id":j.batch_id,"study_Centre":studycentre_details.name,
# 					'batch_name':j.batch_name,'application_start_date':str(j.appli_start_date),
# 					'application_end_date':str(j.appli_end_date),'programme_start_date':str(j.prgm_start_date),
# 					'programme_end_date':str(j.prgm_end_date),'Fees':j.program_fee}
# 					list1.append(dict1)
# 					dict2={"programme_id":i.program_id,"code":i.program_code,"title":i.title,"description":i.description,"thumbnail":i.thumbnail,"batches":list1}
# 					dict3.append(dict2)
# 					unique_stuff = { each['programme_id'] : each for each in dict3 }.values()
# 			msg={"mobilepath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/mobile/",
# 			"webpath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/web/",
# 			"upcomingprogramme":list(unique_stuff)}
# 		return {"status":200,"message":msg}
		
# 	except Exception as e:
# 		err={"status":500,"message":"Internal Server Error"}
# 		return err
def get_all_upcoming_programmes():
	try:
		programmeData = Programme.objects.filter(program_id__in=Subquery(Batch.objects.filter(status='Inactive').values('program_id'))).order_by('title')
		# print(programmeData)
		prg_result_list=[]
		if len(programmeData)!=0:		
			
			for i in programmeData:
				prg_result_dict={"programme_id":i.program_id,"code":i.program_code,"title":i.title,"description":i.description,"thumbnail":i.thumbnail}
				prg_result_list.append(prg_result_dict)
				unique_stuff = { each['programme_id'] : each for each in prg_result_list }.values()
			
			msg={"mobilepath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/mobile/",
			"webpath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/web/",
			"upcomingprogramme":list(unique_stuff)}
			return {"status":200,"message":msg}
		else:
			programmeData = Programme.objects.filter(status="active").order_by('title')
			for i in programmeData:
				prg_result_dict={"programme_id":i.program_id,"code":i.program_code,"title":i.title,"description":i.description,"thumbnail":i.thumbnail}
				prg_result_list.append(prg_result_dict)
			
			msg={"mobilepath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/mobile/",
			"webpath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Program/thumbnail/web/",
			"upcomingprogramme":prg_result_list}
			# "upcomingprogramme":list(unique_stuff)}
			return {"status":200,"message":msg}
		
	except Exception as e:
		return internalServer

#=======================================#
#     function for adding a new batch  #
#=======================================#

def add_batch(recieved_json):
	try:
		batch_rec_data=json.dumps(recieved_json)
		batch_parsed_data=json.loads(batch_rec_data)
		batch_dis_name="batch_dis_name"
		if batch_parsed_data.get(p_id) and batch_parsed_data.get(s_id) and batch_parsed_data.get(no_seats) and batch_parsed_data.get(p_fee) and batch_parsed_data.get(apl_st_date) and batch_parsed_data.get(apl_en_date) and batch_parsed_data.get(pgm_st_date) and batch_parsed_data.get(pgm_en_date) and batch_parsed_data.get(batch_dis_name):
			pg_id=batch_parsed_data.get(p_id)
			batch_dis_name=batch_parsed_data.get(batch_dis_name)
			pg_existance=Programme.objects.filter(program_id=pg_id)			
			if len(pg_existance)==0:
				return invalid_pgm
			cprgobj = Course_programme_mapping.objects.filter(prg_id=pg_id)
			if len(cprgobj)==0:
				return invalid_course
			for sing_pg in pg_existance:
				pg_code=sing_pg.program_code
				dp_id=sing_pg.department_id_id

			# dp_id=batch_parsed_data.get(d_id)
			# dp_existance=Department.objects.filter(Department_id=dp_id)			
			# if len(dp_existance)==0:
			# 	return invalid_dpt
			st_id=batch_parsed_data.get(s_id)
			

			# Study centre existance if rquired
			# std_existance=studycentre.objects.filter(studycentre_id=st_id) 			
			# if len(std_existance)==0:
			# 	return invalid_std

			pg_fee=batch_parsed_data.get(p_fee)
			# if pg_fee.isdigit()==False :
			# 	return invalid_fee

			# if int(pg_fee)<0:
			# 	return invalid_fee

			no_of_seats=batch_parsed_data.get(no_seats)
			if no_of_seats.isdigit()==False :
				return invalid_seats

			if int(no_of_seats)<=0:
				return invalid_seats

			appl_st_date=batch_parsed_data.get(apl_st_date)					
			appl_en_date=batch_parsed_data.get(apl_en_date)
			
			a_st=dt.strptime(appl_st_date, dt_format)
			a_en=dt.strptime(appl_en_date, dt_format)
			

			if a_en <= a_st:
				return invalid_apl_date
								

			pg_st_date=batch_parsed_data.get(pgm_st_date)
			pg_en_date=batch_parsed_data.get(pgm_en_date)
			

			p_st=dt.strptime(pg_st_date, dt_format)
			p_en=dt.strptime(pg_en_date, dt_format)
			
			if a_en==p_st:
				return invalid_en_apl_date

			if p_en <= p_st:
				return invalid_cls_date
			
			if p_st < a_en:
				return invalid_pg_date
			
			display_name=batch_dis_name.lower()
			b_d_name=display_name.replace(" ","")
			random_num=batch_name_creation()
			batch_name="Batch-"+pg_code+"-"+str(random_num)
			batch_existance=Batch.objects.filter(no_of_seats=no_of_seats,appli_start_date=appl_st_date, appli_end_date=appl_en_date,prgm_start_date=pg_st_date,prgm_end_date=pg_en_date,status=STATUS,program_fee=pg_fee,department_id_id=dp_id,program_id_id=pg_id, study_centre_id_id=st_id)
			if len(batch_existance)!=0:
				for i in batch_existance:
					dis_name=(i.batch_dis_name).lower()
					batch_dis_name=dis_name.replace(" ", "")
					if batch_dis_name==b_d_name:
						return bat_exist
					else:
						new_batch=Batch(batch_name=batch_name,no_of_seats=no_of_seats,appli_start_date=appl_st_date, appli_end_date=appl_en_date,prgm_start_date=pg_st_date,prgm_end_date=pg_en_date,status=STATUS,program_fee=pg_fee,department_id_id=dp_id,program_id_id=pg_id, study_centre_id_id=st_id,batch_dis_name=batch_dis_name)
						new_batch.save()
			else:		
				new_batch=Batch(batch_name=batch_name,no_of_seats=no_of_seats,appli_start_date=appl_st_date, appli_end_date=appl_en_date,prgm_start_date=pg_st_date,prgm_end_date=pg_en_date,status=STATUS,program_fee=pg_fee,department_id_id=dp_id,program_id_id=pg_id, study_centre_id_id=st_id,batch_dis_name=batch_dis_name)
				new_batch.save()

			# ins_batch=Batch.objects.order_by('-batch_id')[0]			
			# batchResultList=[]		
			# dict1={"program_id":ins_batch.program_id_id,"batch_id":ins_batch.batch_id,'batch_name':ins_batch.batch_name,'application_start_date':ins_batch.appli_start_date,'application_end_date':ins_batch.appli_end_date,'programme_start_date':ins_batch.prgm_start_date,'programme_end_date':ins_batch.prgm_end_date,'fees':ins_batch.program_fee,"study_center_id":ins_batch.study_centre_id_id,"department_id":ins_batch.department_id_id,"status":ins_batch.status,"no_seats":ins_batch.no_of_seats}
			# batchResultList.append(dict1)				
			return result
		
		else:
			return bad_request
	except Exception as e:
		return int_ser_err
# If it requires more loginc for batch name we have to implement the logic here
def batch_name_creation():
	rand=random.randint(0,1000)
	return rand

#============================================#
#     function for fetching a single batch  #
#===========================================#
def single_batch(recieved_json):
	try:
		batch_rec_data=json.dumps(recieved_json)
		batch_parsed_data=json.loads(batch_rec_data)
		if batch_parsed_data.get(p_id) and batch_parsed_data.get(b_id): 
			pg_id=batch_parsed_data.get(p_id)
			bat_id=batch_parsed_data.get(b_id)
			pg_existance=Programme.objects.filter(program_id=pg_id)			
			if len(pg_existance)==0:
				return invalid_pgm
			batch_existance=Batch.objects.filter(batch_id=bat_id,program_id_id=pg_id)
			if len(batch_existance)==0:
				return invalid_batch
						
			batchResultList=[]
			for ins_batch in batch_existance:
				dict1={"pgm_id":ins_batch.program_id_id,"b_id":ins_batch.batch_id,'b_name':ins_batch.batch_name,'application_start_date':ins_batch.appli_start_date,'application_end_date':ins_batch.appli_end_date,'programme_start_date':ins_batch.prgm_start_date,
				'programme_end_date':ins_batch.prgm_end_date,'fees':ins_batch.program_fee,"study_center_id":ins_batch.study_centre_id_id,"department_id":ins_batch.department_id_id,"status":ins_batch.status,"no_seats":ins_batch.no_of_seats,
				"batch_display_name":ins_batch.batch_dis_name}
			batchResultList.append(dict1)				
			return {"status":200,"message":batchResultList}
		
		else:
			return bad_request
	except Exception as e:
		return int_ser_err
	

#=======================================#
#     function for editing a new batch  #
#=======================================#

def edit_batch(recieved_json):
	try:
		batch_rec_data=json.dumps(recieved_json)
		batch_parsed_data=json.loads(batch_rec_data)
		batch_dis_name="batch_dis_name"
		if batch_parsed_data.get(b_id) and batch_parsed_data.get(b_name) and batch_parsed_data.get(p_id) and batch_parsed_data.get(s_id) and batch_parsed_data.get(no_seats) and batch_parsed_data.get(p_fee) and batch_parsed_data.get(apl_st_date) and batch_parsed_data.get(apl_en_date) and batch_parsed_data.get(pgm_st_date) and batch_parsed_data.get(pgm_en_date) and batch_parsed_data.get(batch_dis_name):
			pg_id=batch_parsed_data.get(p_id)
			bat_id=batch_parsed_data.get(b_id)
			batch_name=batch_parsed_data.get(b_name)
			pg_existance=Programme.objects.filter(program_id=pg_id)			
			if len(pg_existance)==0:
				return invalid_pgm
			for sing_pg in pg_existance:
				dp_id=sing_pg.department_id_id
			batch_existance=Batch.objects.filter(batch_id=bat_id,program_id_id=pg_id)
			if len(batch_existance)==0:
				return invalid_batch
			
			# dp_id=batch_parsed_data.get(d_id)
			pg_fee=batch_parsed_data.get(p_fee)
			no_of_seats=batch_parsed_data.get(no_seats)
			appl_st_date=batch_parsed_data.get(apl_st_date)					
			appl_en_date=batch_parsed_data.get(apl_en_date)
			pg_st_date=batch_parsed_data.get(pgm_st_date)
			pg_en_date=batch_parsed_data.get(pgm_en_date)
			batch_dis_name=batch_parsed_data.get(batch_dis_name)
			
			
			# dp_existance=Department.objects.filter(Department_id=dp_id)			
			# if len(dp_existance)==0:
			# 	return invalid_dpt
			st_id=batch_parsed_data.get(s_id)

			# Study centre existance if rquired
			# std_existance=studycentre.objects.filter(studycentre_id=st_id) 			
			# if len(std_existance)==0:
			# 	return invalid_std

			
			# if pg_fee.isdigit()==False :
			# 	return invalid_fee

			# if int(pg_fee)<0:
			# 	return invalid_fee

			
			if no_of_seats.isdigit()==False :
				return invalid_seats

			if int(no_of_seats)<=0:
				return invalid_seats

			
			
			a_st=dt.strptime(appl_st_date, dt_format)
			a_en=dt.strptime(appl_en_date, dt_format)
			
			

			if a_en <= a_st:
				return invalid_apl_date							
		

			p_st=dt.strptime(pg_st_date, dt_format)
			p_en=dt.strptime(pg_en_date, dt_format)

			if p_en <= p_st:
				return invalid_cls_date
			
			if p_st < a_en:
				return invalid_pg_date
			
			
			
			batch_existance=Batch.objects.filter(batch_name=batch_name,no_of_seats=no_of_seats,appli_start_date=appl_st_date, appli_end_date=appl_en_date,prgm_start_date=pg_st_date,prgm_end_date=pg_en_date,program_fee=pg_fee,department_id_id=dp_id,program_id_id=pg_id, study_centre_id_id=st_id).exclude(batch_id=bat_id)
			if len(batch_existance)>0:
				return bat_exist
			
			
			result=Batch.objects.filter(batch_id=bat_id).update(batch_name=batch_name,no_of_seats=no_of_seats,appli_start_date=appl_st_date, appli_end_date=appl_en_date,prgm_start_date=pg_st_date,prgm_end_date=pg_en_date,program_fee=pg_fee,department_id_id=dp_id,program_id_id=pg_id, study_centre_id_id=st_id,batch_dis_name=batch_dis_name)
			
			if result==1:
				return edit_result			
			
			else:
				return err_result
				
		
		else:
			return bad_request
	except Exception as e:
		return int_ser_err


#==================================================================#
#     function for removing the batch for unsuccessfull insertion  #
#==================================================================#
def remove_batch(recieved_json):
	try:
		batch_rec_data=json.dumps(recieved_json)
		batch_parsed_data=json.loads(batch_rec_data)
		if batch_parsed_data.get(p_id) and batch_parsed_data.get(b_id): 
			pg_id=batch_parsed_data.get(p_id)
			bat_id=batch_parsed_data.get(b_id)
			pg_existance=Programme.objects.filter(program_id=pg_id)			
			if len(pg_existance)==0:
				return invalid_pgm
			batch_existance=Batch.objects.filter(batch_id=bat_id,program_id_id=pg_id).delete()				
			return {"status":200,"message":"Successfully removed"}
		else:
			return bad_request
	except Exception as e:
		return int_ser_err
#====================================#
#     function for get all batches   #
#====================================#

def get_all_batch():
	try:
		queryset=Batch.objects.select_related('program_id','study_centre_id','department_id').values('batch_id','program_id','department_id','study_centre_id',
    	'batch_name','no_of_seats','appli_start_date','appli_end_date','prgm_start_date','prgm_end_date','status','program_fee',
		'study_centre_id__name','department_id__Department_Name','department_id__Department_code','program_id__title','batch_dis_name',
		'program_id__program_type')
		batchList=[]
		for b in queryset:
			batchDict = {"batchid":b['batch_id'],"prg_id":b['program_id'], "prg_name":b['program_id__title'],
			"deptname":b['department_id__Department_Name'],"dept_id":b['department_id'],"deptcode":b['department_id__Department_code'],
			"studname":b['study_centre_id__name'],"studycentre_id":b['study_centre_id'], "batchname":b['batch_name'],"seats":b['no_of_seats'],
    		"appli_start_date":b['appli_start_date'],"appli_end_date":b['appli_end_date'],"prg_type":b['program_id__program_type'],
			"prg_start_date":b['prgm_start_date'],"prg_end_date":b['prgm_end_date'],"status":b['status'],"batch_display_name":b['batch_dis_name'],
			"fee":b['program_fee']}
			app_count=applicant_count(b['batch_id'])
			batchDict.update({"appl_count":app_count})

			batchList.append(batchDict)
		allprgobj=Programme.objects.all().order_by('title')
		prgList=[]
		for i in allprgobj:
			prgdict={"prgid":i.program_id,"prgname":i.title,"programtype":i.program_type}
			prgList.append(prgdict)
		allstudobj=studycentre.objects.all()
		studList=[]
		for i in allstudobj:
			studdict={"study_id":i.studycentre_id,"name":i.name}
			studList.append(studdict)
		msg={"batchdetails":batchList,"programlist":prgList,"studycentrelist":studList}
		return JsonResponse({"status":200,"message":msg},safe=False)
	except Exception as e:
		# err={"status":500,"message":"Internal Server Error"}
		return JsonResponse(internalServer)

def applicant_count(batch_id):
        result = StudentApplicants.objects.filter(batch_id_id=batch_id)
        count=len(result)
        return count




#=======================================#
# function  for  change  batch   status #
#=======================================#
def change_status_batch(received_json_data):
	try:
		data1=json.dumps(received_json_data)
		data=json.loads(data1)
		if data.get('bid') and data.get('status') :
			batch_id=data.get('bid')
			batch_status=data.get('status')
			cur_date=dt.today().date()
			batchobj = Batch.objects.filter(batch_id=batch_id)
			if batchobj.count()==0:
				return JsonResponse({"status":404,"message":"Invalid batch id"},safe=False)
			prg_id=batchobj[0].program_id
			i=batchobj[0]
			if (batchobj.count()!=0 and batch_status=="admission"):
				if i.appli_start_date <= cur_date <= i.appli_end_date:
					if i.status=="Inactive":
						queryset=ProgramEligibility.objects.filter(program_id_id=prg_id)
						if queryset.count()==0:
							return JsonResponse({"status":404,"message":"Please add eligibility question for this programme"},safe=False) 
						queryset1 = Course_programme_mapping.objects.filter(prg_id=prg_id)
						if queryset1.count()==0:
							return JsonResponse({"status":404,"message":"Please add  course for this programme"},safe=False)
						old_status=i.status
						i.status=batch_status
						i.save()
						return JsonResponse({"status":200,"message":"Successfully changed batch status"},safe=False)	
					return JsonResponse({"status":404,"message":"Current batch status is not inactive"},safe=False)
				else:
					return JsonResponse({"status":404,"message":"You can change the status only during admission process"},safe=False)
			elif(batchobj.count()!=0 and batch_status=="active") :
				if i.appli_end_date < cur_date <= i.prgm_start_date:
					if i.status=='admission':
						old_status=i.status
						i.status=batch_status
						i.save()
						return JsonResponse({"status":200,"message":"Successfully changed batch status"},safe=False)
					return JsonResponse({"status":404,"message":"Current batch status is not admission"},safe=False)
				return JsonResponse({"status":404,"message":"Can't change the status.Either admission process not completed or class start date for this batch has not been reached"},safe=False)
			elif(batchobj.count()!=0 and batch_status=="hide"):
				if i.status=='Inactive':
					old_status=i.status
					i.status=batch_status
					i.save()
					return JsonResponse({"status":200,"message":"Successfully changed batch status"},safe=False)
				return JsonResponse({"status":404,"message":"Current batch status is not inactive"},safe=False)
			elif(batchobj.count()!=0 and batch_status=="Inactive"):
				if i.status=='hide':
					old_status=i.status
					i.status=batch_status
					i.save()
					return JsonResponse({"status":200,"message":"Successfully changed batch status"},safe=False)
				return JsonResponse({"status":404,"message":"Current batch status is not hide"},safe=False)
		else:
			return JsonResponse(error)
	except Exception as e:
		return JsonResponse(internalServer)

