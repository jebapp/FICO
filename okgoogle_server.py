from flask import Flask, request, jsonify
import json
import requests
import os
import urllib
from flask import make_response

app = Flask(__name__)


def results1():
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
	
    #### future payables
    if (action == "ap_future"):
         supplier = req['queryResult']['parameters']['supplierno']		 
         file = requests.get("https://sapdemo.kpit.com:1447/sap/opu/odata/sap/C_APFUTUREACCOUNTSPAYABLE_CDS/C_APFUTUREACCOUNTSPAYABLE(P_DateFunction='TODAY',P_DisplayCurrency='EUR',P_ExchangeRateType='M',P_NetDueInterval1InDays='30',P_NetDueInterval2InDays='60',P_NetDueInterval3InDays='90')/Results?$filter=(Supplier eq '%s')&$format=json"%supplier, auth=('karunak1', 'Welcome@1234'), verify=False).json()
         size = len(file['d']['results'])
         if(size == 0):
	         output = "Invalid Supplier Number"
         else:         
             sup_name = file["d"]["results"][0]["SupplierName"]
             amount = file["d"]["results"][0]["TotalAmountInDisplayCrcy_F"]
             response = 'The future payables for ' + sup_name + ' is' + amount
         return {'fulfillmentText': response}
		 
	#### cash discount utilization
    if (action == "ap_cash"):
         file = requests.get("https://sapdemo.kpit.com:1447/sap/opu/odata/sap/C_APCSHDISCUTILIZATION_CDS/C_APCSHDISCUTILIZATION(P_StartDate=datetime'2019-04-22T00:00:00',P_DisplayCurrency='EUR')/Results?$format=json", auth=('Karunak1', 'Welcome@1234'), verify=False).json()
         cash = file["d"]["results"][0]["OfferedCshDiscInDspCrcy_E_F"]
         response = 'The cash discount offered is ' + cash    
         return {'fulfillmentText': response} 
		 
    #### days payable outstanding
    if (action == "ap_outstanding"):
         supplier = req['queryResult']['parameters']['supplierno']
         file = requests.get("https://sapdemo.kpit.com:1447/sap/opu/odata/sap/C_APDAYSPAYOUTST_CDS/C_APDAYSPAYOUTST(P_Currency='USD',P_ExchangeRateType='M')/Results?$filter=(Supplier eq '%s')&$format=json"%(supplier), auth=('karunak1', 'Welcome@1234'), verify=False).json()
         size = len(file['d']['results'])
         if(size == 0):
	         output = "Invalid Supplier Number"
         else:
             sup_name = file["d"]["results"][0]["SupplierName"]
             outstanding = file["d"]["results"][0]["DaysPayablesOutstanding_F"]
             response = 'The days payable outstanding for'+ sup_name + ' is' + outstanding    
         return {'fulfillmentText': response}
       
    #### overdue payables       supplier - 17300001
    if (action == "ap_overdue"): 
         supplier = req['queryResult']['parameters']['supplierno']
         file = requests.get("https://sapdemo.kpit.com:1447/sap/opu/odata/sap/C_APOVRD_CDS/C_APOVRD(P_DateFunction='TODAY',P_AgingGridMeasureInDays='30',P_CriticallyOverdueThreshold='70',P_DisplayCurrency='EUR')/Results?$filter=(Supplier eq '%s')&$format=json"%(supplier), auth=('karunak1', 'Welcome@1234'), verify=False).json()
         size = len(file['d']['results'])
         if(size == 0):
	         response = "Invalid Supplier Number"
         else:   
             sup_name = file["d"]["results"][0]["SupplierName"]
             amt = file["d"]["results"][0]["TotalOverdueAmtInDspCrcy_E_F"]
             response = 'The overdues payables for'+ sup_name + ' is' + amt  
         return {'fulfillmentText': response}
 

     #### aging analysis
    if (action == "ap_aging"):
         supplier = req['queryResult']['parameters']['supplierno']
         file = requests.get("https://sapdemo.kpit.com:1447/sap/opu/odata/sap/C_APFLEXIBLEAGING_CDS/C_APFLEXIBLEAGING(P_DateFunction='TODAY',P_AgingGridMeasureInDays='0000000015',P_NumberOfAgingGridColumns='0000000004',P_DisplayCurrency='EUR')/Results?$filter=(Supplier eq '%s')&$format=json"%supplier, auth=('karunak1', 'Welcome@1234'), verify=False).json()
         size = len(file['d']['results'])
         if(size == 0):
             response = 'Invalid Supplier Number' 
         else:		         
             sup_name = file["d"]["results"][0]["SupplierName"]
             amount = file["d"]["results"][0]["AmountInDisplayCurrency_E_F"]
             total = file["d"]["results"][0]["TotalNotOvrdAmtInDspCrcy_F"]
             response = 'The amount of aging analysis for'+ sup_name + ' is' + amount + 'total amount is ' + total 
         return {'fulfillmentText': response}
		
   	####Supplier Payment Analysis 
    if (action == "ap_supplierpayment"):
         supplier = req['queryResult']['parameters']['supplierno']
         file = requests.get("https://sapdemo.kpit.com:1447/sap/opu/odata/sap/C_APMANUALPAYMENTS_CDS/C_APMANUALPAYMENTS(P_NumberOfDays='0',P_Currency='USD',P_ExchangeRateType='M')/Results?$filter=(Supplier eq '%s')&$format=json"%(supplier), auth=('karunak1', 'Welcome@1234'), verify=False).json()
         size = len(file['d']['results'])
         if(size== 0):
             response = 'Invalid Supplier Number'
         else:
             sup_name = file["d"]["results"][0]["SupplierName"]
             amount = file["d"]["results"][0]["PaymentAmountInDisplayCrcy_F"]
             response = 'The amount for Supplier payment analysis of '+ sup_name + ' is' + amount  
         return {'fulfillmentText': response}
	
	####Future Receviables 
    if (action == "ar_future"):
         cnum = req['queryResult']['parameters']['customer_number']
         file = requests.get("https://sapdemo.kpit.com:1447/sap/opu/odata/sap/C_FUTUREACCTRBLS_CDS/C_FUTUREACCTRBLS(P_DateFunction='TODAY',P_DisplayCurrency='USD',P_ExchangeRateType='M',P_NetDueInterval1InDays='30',P_NetDueInterval2InDays='60',P_NetDueInterval3InDays='90',P_NetDueInterval4InDays='120')/Results?$filter=Customer eq '%s'&$format=json" %cnum, auth=('Karunak1', 'Welcome@1234'), verify=False).json()
         size = len(file['d']['results'])
         if(size== 0):
             response = 'Invalid Customer Number'
         else:
             Customer = file["d"]["results"][0]["Customer"]
	     NumberOfOpenItems = file["d"]["results"][0]["NumberOfOpenItems"]
             TotalOverdueAmtInDspCrcy_F = file["d"]["results"][0]["TotalOverdueAmtInDspCrcy_F"]
             response = 'The total overdue amount is '+ TotalOverdueAmtInDspCrcy_F + ' for customer ' + Customer + 'and number of open items is ' + NumberOfOpenItems
         return {'fulfillmentText': response}	
	
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return (jsonify(results1()))

if __name__ == '__main__':
   port = int(os.environ.get('PORT',5000))
   app.run(port=port, host="0.0.0.0")
