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
from datetime import datetime as dt
from .constants import *
#==================================#
# function for add event details   #
#==================================#

def event_add(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('title') and data.get('desc') and data.get('start_date') and data.get('end_date') and data.get('pic'):
            title=data.get('title')
            ev_title=title.replace(' ','')
            if len(ev_title)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event title"},safe=False)
            desc=data.get('desc')
            ev_desc=desc.replace(' ','')
            if len(ev_desc)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event description"},safe=False)
            start=data.get('start_date')
            ev_start=start.replace(' ','')
            if len(ev_start)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event start date"},safe=False)
            end=data.get('end_date')
            ev_end=end.replace(' ','')
            if len(ev_end)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event end date"},safe=False)
            tdate=dt.today().date()
            tdate=str(tdate)
            t_date=dt.strptime(tdate, '%Y-%m-%d')
            e_st=dt.strptime(start, '%Y-%m-%d')
            e_en=dt.strptime(end, '%Y-%m-%d')
            if e_st < t_date:
                return JsonResponse({"status":404,"message":"Event startdate never be lessthan the current date"},safe=False)
            if e_en < e_st:
                return JsonResponse({"status":404,"message":"Event enddate never be lessthan event startdate"},safe=False)
            pic=data.get('pic')
            ev_pic=pic.replace(' ','')
            if len(ev_pic)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event picture"},safe=False)
            queryset=events.objects.filter(title=title,start_date=start,end_date=end)
            qset=events.objects.filter(title=title,start_date=start)
            if((queryset.count()==0) and (qset.count()==0)):
                add=events(title=title,description=desc,start_date=start,
                end_date=end,picture=pic)
                add.save()
                return JsonResponse({"status":200,"message":"Successfully added event details"},safe=False) 
            return JsonResponse({"status":404,"message":"Event already exist"},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)

#=======================================#
# function  for  edit  event    details #
#=======================================#
def event_edit(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('id') and data.get('title') and data.get('desc') and data.get('start_date') and data.get('end_date') and data.get('pic'):
            event_id=data.get('id')
            event_title=data.get('title')
            ev_title=event_title.replace(' ','')
            if len(ev_title)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event title"},safe=False)
            event_desc=data.get('desc')
            ev_desc=event_desc.replace(' ','')
            if len(ev_desc)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event description"},safe=False)
            start_date=data.get('start_date')
            ev_start=start_date.replace(' ','')
            if len(ev_start)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event start date"},safe=False)
            end_date=data.get('end_date')
            ev_end=end_date.replace(' ','')
            if len(ev_end)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event end date"},safe=False)
            tdate=dt.today().date()
            tdate=str(tdate)
            t_date=dt.strptime(tdate, '%Y-%m-%d')
            e_st=dt.strptime(start_date, '%Y-%m-%d')
            e_en=dt.strptime(end_date, '%Y-%m-%d')
            # if e_st < t_date:
            #     return JsonResponse({"status":404,"message":"Event startdate never be lessthan the current date"},safe=False)
            if e_en < e_st:
                return JsonResponse({"status":404,"message":"Event enddate never be lessthan event startdate"},safe=False)
            picture=data.get('pic')
            ev_pic=picture.replace(' ','')
            if len(ev_pic)==0:
                return JsonResponse({"status":404,"message":"Invalid data in event picture"},safe=False)
            eventobj = events.objects.filter(event_id=event_id)
            if eventobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid event id"},safe=False)
            queryset=events.objects.filter(title=event_title,start_date=start_date,end_date=end_date).exclude(event_id=event_id)
            qset=events.objects.filter(title=event_title,start_date=start_date).exclude(event_id=event_id)
            if((queryset.count()==0) and (qset.count()==0)):
                for event in eventobj:
                    event.title=event_title
                    event.description=event_desc
                    event.start_date=start_date
                    event.end_date=end_date
                    event.picture=picture
                    event.save()
                    return JsonResponse({"status":200,"message":"Successfully edited event details"},safe=False) 
            return JsonResponse({"status":404,"message":"Event already exist"},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
       
        return JsonResponse(internalServer)
#========================================#
# function for delete   event    details #
#========================================#
def event_delete(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('id'):
            event_id=data.get('id')
            eventobj = events.objects.filter(event_id=event_id)
            if eventobj.count()==0:
                return JsonResponse({"status":404,"message":"Invalid event id"},safe=False)
            else:
                eventobj.delete()
                return JsonResponse({"status":200,"message":"Successfully deleted event details"},safe=False)
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)

#=====================================#
# function for get an  event  details #
#=====================================#

def get_a_event(received_json_data):
    try:
        data1=json.dumps(received_json_data)
        data=json.loads(data1)
        if data.get('dtype') and data.get('eventid'):
            dtype=data.get('dtype').upper()
            img_path=imagepath(dtype)
            evnt_id=data.get('eventid')
            if img_path==False:
                return JsonResponse({"status":400,"message":"Bad request"},safe=False)
            queryset=events.objects.filter(event_id=evnt_id)
            if queryset.count()==0:
                return JsonResponse({"status":404,"message":"Invalid event id"},safe=False) 
            else:
                eventDict1=[]
                for i in queryset:
                    eventDict = {"id" : i.event_id,"event_title" : i.title,"desc":i.description,"startdate":i.start_date,"enddate":i.end_date,"image":i.picture}
                    eventDict1.append(eventDict)
                return JsonResponse({"status":200,"imagepath":img_path,"message":eventDict1},safe=False) 
        else:
            return JsonResponse(error)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)
# ==================================#
#  function for finding image path  #
# ==================================#
def imagepath(dtype):
    imgpath="https://s3-ap-southeast-1.amazonaws.com/dastp/Events/"
    if dtype=="M":
        imgpath=imgpath+"mobile/"
        return imgpath
    elif dtype=="W":
        imgpath=imgpath+"web/"
        return imgpath
    else:
        return False

#==================================#
#     function for get all events  #
#==================================#
def get_all_events():
    try:
        queryset=events.objects.values('event_id','title','description','start_date','end_date','picture')
        eventDict1=[]
        for i in queryset:
            eventDict = {"id" : i['event_id'],"event_title" : i['title'],"desc":i['description'],
            "startdate":str(i['start_date']),"enddate":str(i['end_date']),"image":i['picture']}
            eventDict1.append(eventDict)
        
        msg={"mobilepath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Events/mobile/",
            "webpath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Events/web/",
            "thumbnailpath":"https://s3-ap-southeast-1.amazonaws.com/dastp/Events/thumb/",
            "events":eventDict1}
        return {"status":200,"message":msg}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer