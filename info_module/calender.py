from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import *
from django.http import JsonResponse
import datetime
from .constants import *

# Create your views here.
    #======================================================#
    #  function for get current month calendar details     #
    #======================================================#

def get_current_cal_events():
    try:
        current_date=datetime.date.today()
        month=current_date.month
        programData=Batch.objects.select_related('program_id').values('prgm_start_date','program_id__title').exclude(status="hide")            
        datefield=[]
        programdate=[]
        for i in programData:
            datefield.append(i['prgm_start_date']) 
            if i['prgm_start_date']!=None:
                psd=i['prgm_start_date']
                if psd.month == month:
                    prgmdict={"name":i['program_id__title'],"startdate":str(i['prgm_start_date'])}
                    programdate.append(prgmdict)
        datefield1=[]
        EventData=events.objects.values('event_id','title','start_date') 
        eventdate=[]
        for i in EventData:
            datefield1.append(i['start_date']) 
            st=i['start_date']
            if st.month == month:
                evntdict={"id":i['event_id'],"name":i['title'],"startdate":str(i['start_date'])}
                eventdate.append(evntdict)
        return {"status":200,"message":{"programme":programdate,"event":eventdate}}
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return internalServer

#======================================================#
#     function for get all month  calendar details     #
#======================================================#

def get_cal_events_programmes():
    try:
    
        programData=Batch.objects.select_related('program_id').values('prgm_start_date','program_id__title').exclude(status="hide")
        programdate=[]            
        for i in programData:
            prgmdict={"name":i['program_id__title'],"startdate":i['prgm_start_date']}
            programdate.append(prgmdict)
        EventData=events.objects.values('event_id','title','start_date')  
        eventdate=[] 
        for i in EventData:
            evntdict={"id":i['event_id'],"name":i['title'],"startdate":i['start_date']}
            eventdate.append(evntdict)
        return JsonResponse({"status":200,"message":{"programme":programdate,"event":eventdate}},safe=False)
    except Exception as e:
        # err={"status":500,"message":"Internal Server Error"}
        return JsonResponse(internalServer)
 