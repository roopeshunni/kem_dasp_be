from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import *
from django.http import JsonResponse
import datetime
import json
import requests
from .checksum import *
from .addApplicant import *
import string
# import Checksum
from datetime import datetime as dt
from datetime import timedelta
from django.conf import settings
import ast
from .constants import *
from dateutil import tz
to_zone=tz.gettz('Asia/Calcutta')

def payment_redirection(recieved_json):
    try:

        payment_data=json.dumps(recieved_json)
        payment_data=json.loads(payment_data)
        if payment_data['user_id'] and payment_data['pid'] and payment_data['batch_id'] and payment_data['amount'] and payment_data['user_name']:

            u_id=payment_data['user_id']
            p_id=payment_data['pid']
            b_id=payment_data['batch_id']
            bill_amount=payment_data['amount']
            user_name=payment_data['user_name']
            prgmobj=Batch.objects.get(batch_id=b_id)
            prgm_fee=prgmobj.program_fee
            # if(prgm_fee.contains("|")):
            if "|" in prgm_fee:
                pay_fee=prgm_fee.split("|")
                p_fee=(map(int, pay_fee))
                total_fee=sum(p_fee)
            else:
                total_fee=prgm_fee
            student=StudentApplicants.objects.filter(user_id=u_id,batch_id=b_id)
            if student.count()==0:
                return JsonResponse({"status":404,"message":"Invalid details"})
            # studentPayment=PaymentHistory.objects.filter(user_id=u_id,status="TXN_SUCCESS")
            # if studentPayment.count()!=0:
            #     return JsonResponse({"status":404,"message":"You  can't pay the fee, You have already paid for a programme"})
            for singleStudent in student:
                appl_num= singleStudent.applicant_id
        

            MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
            MERCHANT_ID = settings.PAYTM_MERCHANT_ID
            # get_lang = "/" + get_language() if get_language() else ''
            # CALLBACK_URL = settings.HOST_URL + get_lang + settings.PAYTM_CALLBACK_URL
            # Generating unique temporary ids
            order_id = id_generator()       

            # bill_amount="1.00"
            if bill_amount:
                data_dict = {
                            'MID':MERCHANT_ID,
                            'ORDER_ID':order_id,
                            'TXN_AMOUNT': bill_amount,
                            'CUST_ID':str(u_id),#'cust123',
                            'INDUSTRY_TYPE_ID':'Retail',
                            'WEBSITE': settings.PAYTM_WEBSITE,
                            'CHANNEL_ID':'WEB',
                            'CALLBACK_URL':settings.CALLBACK_URL,
                            # 'user_name':user_name
                        }
                param_dict = data_dict
                param_dict['CHECKSUMHASH'] = generate_checksum(data_dict, MERCHANT_KEY).decode('utf-8')
                # cur_date = datetime.datetime.now()
                # c_date = cur_date.strftime("%Y-%m-%d %H:%M:%S")
                c_date=current_datetime()
                
                payData = PaymentHistory(user_id=u_id, prgm_id=p_id, applicant_no=appl_num,
                                         order_id=order_id, total_fee=total_fee, trans_date=c_date)
                payData.save()
                return JsonResponse({"status":200,"message":param_dict})
            
        else:
            return JsonResponse(error)

    except Exception as e:
        return JsonResponse(internalServer)

def current_datetime():
    c_date=datetime.datetime.now().astimezone(to_zone).strftime("%Y-%m-%d %H:%M:%S")
    cur_date=dt.strptime(c_date, '%Y-%m-%d %H:%M:%S')
    return cur_date

def payment_response(request):   
    try:
        if request.method == "POST":
            MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
            data_dict = {}
            for key in request.POST:
                data_dict[key] = request.POST[key]
            
            verify = verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
            # student=StudentApplicants.objects.filter(user_id=u_id,batch_id=b_id)
            # verify=True
            paymentobj=PaymentHistory.objects.filter(order_id=data_dict.get("ORDERID"))
            appl_num=''
            for i in paymentobj:
                i.trans_id=data_dict.get("TXNID")
                i.trans_amount=data_dict.get("TXNAMOUNT")
                # If the transaction is cancelled no date will be there in the response #retured by the paytm. So we need to add the current date
                i.trans_date=data_dict.get("TXNDATE") if data_dict.get("TXNDATE") else datetime.datetime.now()
                ##########################  
                i.res_code=data_dict.get("RESPCODE")
                i.status=data_dict.get("STATUS")
                i.res_msg=data_dict.get("RESPMSG")
                i.trans_res=str(data_dict)
                appl_num=i.applicant_no
                i.save()
            if verify:
                student=StudentApplicants.objects.filter(applicant_id=appl_num)
                for singleStudent in student:
                   
                    if(data_dict.get("STATUS")=="TXN_SUCCESS"):
                        singleStudent.transaction_id=data_dict.get("TXNID")
                        singleStudent.is_paid=True
                    elif(data_dict.get("STATUS")=="PENDING"):
                        pay_status=payment_status(data_dict.get("ORDERID"),True)
                        if (pay_status.get('STATUS')=="TXN_SUCCESS"):
                            for data in paymentobj:
                                data.trans_id=pay_status.get("TXNID")
                                data.trans_amount=pay_status.get("TXNAMOUNT")
                                # If the transaction is cancelled no date will be there in the response #retured by the paytm. So we need to add the current date
                                data.trans_date=pay_status.get("TXNDATE") if pay_status.get("TXNDATE") else datetime.datetime.now()
                                ##########################  
                                data.res_code=pay_status.get("RESPCODE")
                                data.status=pay_status.get("STATUS")
                                data.res_msg=pay_status.get("RESPMSG")
                                data.trans_res=str(pay_status)
                                data.save()

                                
                            singleStudent.transaction_id=data_dict.get("TXNID")
                            singleStudent.is_paid=True  


                    else:
                       singleStudent.is_paid=False
                    singleStudent.save()

                
            # PaytmHistory.objects.create(user=request.user, **data_dict)
                url=settings.REDIRECT_URL+"%s" %(data_dict['TXNID'])
                # url="http://54.66.133.32:8000/#/paymentresponse/%s" %(data_dict['TXNID'])
                return redirect(url)
                # return render(request,"response.html",{"paytm":data_dict})
            else:
                url=settings.REDIRECT_URL+"%s" %(data_dict['TXNID'])
                return redirect(url)
                # return HttpResponse("checksum verify failed")
        return HttpResponse(status=200)
    except Exception as e:
        return JsonResponse(internalServer)


def payment_receipt(recieved_json):    
    try:
        payment_data=json.dumps(recieved_json)
        payment_data=json.loads(payment_data)
        if payment_data['txn_id']:
            paymentobj=PaymentHistory.objects.filter(trans_id=payment_data.get("txn_id"))
            paymentlist=[]
            
            if paymentobj.count()==0:
                return JsonResponse({"status":309,"message":paymentlist})
            for i in paymentobj:
                prgmobj=Programme.objects.get(program_id=i.prgm_id)
                t_date=i.trans_date
                dt=t_date.strftime("%Y-%m-%d %H:%M:%S")
                trans_date=str(dt).replace('Z', '').replace('T', '')
                paymnetDic={"user_id":i.user_id,"user_name":payment_data.get("name"),"prgm_id":i.prgm_id,"appl_no":i.applicant_no,"order_id":i.order_id,
                "trans_id":i.trans_id,"trans_amount":i.trans_amount,"trans_date":trans_date,"res_msg":i.res_msg,"prgm_name":prgmobj.title,
                "res_code":i.res_code,"status":i.status}
                paymentlist.append(paymnetDic)
                return JsonResponse({"status":200,"message":paymentlist})
                # if i.res_code=="01":
                #     # response=add_applicant(recieved_json)
                #     return JsonResponse({"status":200,"message":paymentlist})
                # else:

                #     return JsonResponse({"status":202,"message":paymentlist})
        else:
            return JsonResponse(error)
    except Exception as e:
        return JsonResponse(internalServer)


def payment_history(recieved_json):
    try:
        received_data=json.dumps(recieved_json)
        data=json.loads(received_data)
        if data.get('pid') and data.get('student_id') and data.get('batch_id'):
            program_id=data.get('pid')
            user_id=data.get('student_id')
            batch_id=data.get('batch_id')
            
            result=payment_result_data(program_id,batch_id,user_id)            
            return {"status":200,"message":result}
        else:
            return error
    except Exception as e:
        return internalServer

def payment_result_data(program_id,batch_id,opt):
    prgobj=Programme.objects.filter(program_id=program_id)
    if prgobj.count()==0:
        result={"prgid":program_id,"ProgramDetails":[],"BatchDetails":[],"paymentDetails":[]}
        return result
    else:
        for i in prgobj:
            prg_id=i.program_id
            prg_code=i.program_code
            prg_name=i.title
        programdict={"prgcode":prg_code,"prgname":prg_name}
        batchlist={}
        paymentDic={}
        paymentList=[]
        batchdetails=Batch.objects.filter(program_id_id=program_id,batch_id=batch_id)
        for i in batchdetails:
            batchid=i.batch_id
            batchname=i.batch_name
            batchdict={"batchid":batchid,"batchname":batchname}
            batchlist.update({batchid:batchdict})
        if opt=="-1":
            studaplobj= StudentApplicants.objects.filter(batch_id_id=batch_id,program_id_id=program_id)
            
        else:
            studaplobj= StudentApplicants.objects.filter(batch_id_id=batch_id,user_id=opt,program_id_id=program_id)
            
         
        if len(studaplobj)!=0:
            paymentList=[]  
            for i in  studaplobj:
                paymentdetails=PaymentHistory.objects.filter(applicant_no=i.applicant_id,status="TXN_SUCCESS")
               
                if len(paymentdetails)!=0:  
                    for j in paymentdetails:
                        t_date=j.trans_date
                        dt=t_date.strftime("%Y-%m-%d %H:%M:%S")
                        trans_date=str(dt).replace('Z', '').replace('T', '')
                        trans_res=ast.literal_eval(j.trans_res)
                        paymentDic={"trans_id":j.trans_id,"applicant_no":j.applicant_no,
                        "trans_amount":j.trans_amount,"trans_date":trans_date,"res_code":j.res_code,
                        "total_fee":j.total_fee,"user_id":j.user_id,"trans_paymentmode":
                        trans_res.get('PAYMENTMODE'),"trans_gatewayname":trans_res.get('GATEWAYNAME'),
                        "trans_bankname":trans_res.get('BANKNAME')
                        }
                        paymentList.append(paymentDic)
                        
        result={"prgid":program_id,"ProgramDetails":programdict,"BatchDetails":batchlist,"paymentDetails":paymentList}
        return result


def get_payment_details(received_json_data):
    try:
        received_data = json.dumps(received_json_data)
        r_data = json.loads(received_data)
        if r_data.get('date'):  
            s_date = r_data.get('date') 
            st_date = dt.strptime(s_date,'%Y-%m-%d')
            en_date = dt.strptime(s_date,'%Y-%m-%d')
            e_date = en_date+timedelta(days=1)
            paymentdet = PaymentHistory.objects.filter(trans_date__range=(st_date, e_date))
            paymentList=[]
            if len(paymentdet) != 0:
                for i in paymentdet:
                    paymentdet = Programme.objects.get(
                        program_id=i.prgm_id)
                    t_date = i.trans_date
                    date = t_date.strftime("%Y-%m-%d %H:%M:%S")
                    trans_date = str(date).replace('Z', '').replace('T', '')
                    if i.trans_res=="":
                        # trans_res = ast.literal_eval(i.trans_res)
                        paymentDic = {"transId": i.trans_id, "applicantNo": i.applicant_no,
                                    "transAmount": i.trans_amount, "transDate": trans_date, "resCode": i.res_code,
                                    "totalFee": i.total_fee, "userId": i.user_id,"programmeName": paymentdet.title,"responseMessage":i.res_msg,
                                    "orderId":i.order_id,
                                    "status":i.status
                                    # trans_res.get('PAYMENTMODE'), "transGatewayName": trans_res.get('GATEWAYNAME'), 
                                    # "transBankName": trans_res.get('BANKNAME'), "status": trans_res.get('STATUS')
                                    
                                    }
                    else:
                        trans_res = ast.literal_eval(i.trans_res)
                        paymentDic = {"transId": i.trans_id, "applicantNo": i.applicant_no,
                                    "transAmount": i.trans_amount, "transDate": trans_date, "resCode": i.res_code,
                                    "totalFee": i.total_fee, "userId": i.user_id,"programmeName": paymentdet.title,"responseMessage":i.res_msg,
                                    "orderId":i.order_id,
                                    "status":i.status,"transPaymentMode":trans_res.get('PAYMENTMODE'), "transGatewayName": trans_res.get('GATEWAYNAME'), 
                                    "transBankName": trans_res.get('BANKNAME'), "status": trans_res.get('STATUS')
                                    
                                    }
                    paymentList.append(paymentDic)
                return {"status":True, "message":"Successfully fetched","data":paymentList}
            else:
                return {"status":False, "message":"No transaction found in this date","data":{}}
    except Exception as e:
        return JsonResponse(error)




def payment_status(order_id,type):
# initialize a dictionary
    paytmParams = dict()
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY

    
    paytmParams["MID"] = settings.PAYTM_MERCHANT_ID

    # Enter your order id which needs to be check status for
    paytmParams["ORDERID"] = order_id
    # paytmParams["ORDERID"]="lAGBWC"

    # Generate checksum by parameters we have in body
    checksum = generate_checksum(paytmParams, MERCHANT_KEY).decode('utf-8')

    # put generated checksum value here
    paytmParams["CHECKSUMHASH"] = checksum

    # prepare JSON string for request
    post_data = json.dumps(paytmParams)
    
    
    # for Production
    url = "https://securegw.paytm.in/order/status"

    data_dict = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    
    if type:
        return data_dict
    

    if data_dict.get('STATUS')=="TXN_SUCCESS": 
        paymentobj=PaymentHistory.objects.filter(order_id=data_dict.get("ORDERID"))
        if paymentobj.count()==0:
            return {"status":False,"message":"Please check the order id you have tried"}

        student=StudentApplicants.objects.filter(applicant_id=paymentobj[0].applicant_no)

        # If the transaction is cancelled no date will be there in the response #retured by the paytm. So we need to add the current date
        trans_date=data_dict.get("TXNDATE") if data_dict.get("TXNDATE") else datetime.datetime.now()
        

        payData=PaymentHistory(user_id=paymentobj[0].user_id,prgm_id=paymentobj[0].prgm_id,
        applicant_no=paymentobj[0].applicant_no,trans_id=data_dict.get("TXNID"),
        trans_amount=data_dict.get("TXNAMOUNT"),trans_date=trans_date,res_code=data_dict.get("RESPCODE"),
        status=data_dict.get("STATUS"),res_msg=data_dict.get("RESPMSG"),trans_res=str(data_dict),
        order_id=paymentobj[0].order_id,total_fee=paymentobj[0].total_fee)

        for singlestudent in student:
            singlestudent.transaction_id=data_dict.get("TXNID")
            singlestudent.is_paid=True
            singlestudent.save()
        payment_data_existance=PaymentHistory.objects.filter(order_id=data_dict.get("ORDERID"),user_id=paymentobj[0].user_id,
        prgm_id=paymentobj[0].prgm_id,applicant_no=paymentobj[0].applicant_no,trans_id=data_dict.get("TXNID"),
        status=data_dict.get("STATUS"))

        if payment_data_existance.count()!=0:
            return {"status":True,"message":"Payment details already updated"}

        payData.save()
        
        return {"status":True,"message":"Payment status updated successfully"}
    else:
        return {"status":False,"message":"Something went wrong please try again"}

        
        

    #     for i in paymentobj:
    #         student=StudentApplicants.objects.filter(applicant_id=i.applicant_no)
    #         i.trans_id=data_dict.get("TXNID")
    #         i.trans_amount=data_dict.get("TXNAMOUNT")
    #         # If the transaction is cancelled no date will be there in the response #retured by the paytm. So we need to add the current date
    #         i.trans_date=data_dict.get("TXNDATE") if data_dict.get("TXNDATE") else datetime.datetime.now()
    #         ##########################  
    #         i.res_code=data_dict.get("RESPCODE")
    #         i.status=data_dict.get("STATUS")
    #         i.res_msg=data_dict.get("RESPMSG")
    #         i.trans_res=str(data_dict)

    #         appl_num=i.applicant_no
    #         i.save()

    #     payData=PaymentHistory(user_id=u_id,prgm_id=p_id,applicant_no=appl_num,order_id=order_id,total_fee=total_fee)
    #     payData.save()

    # elif data_dict.get('STATUS')=="TXN_FAILURE":
    #     return JsonResponse({"status":404,"message":"Please check the order id you have tried"},safe=False)
    # else:
    #     return JsonResponse({"status":404,"message":"Please check the order id you have tried"},safe=False)


    
    # return response


   
			
            
            
            
            





           


