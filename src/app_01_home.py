from flask import Blueprint
from flask import Flask, render_template
from flask import Flask,request
from firebase import firebase
import urllib
from urllib.parse import unquote
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from datetime import datetime
from flask import Flask, render_template, url_for, json

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./src/testproject-9cef3-firebase-adminsdk-1hkji-3cdddd3c46.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testproject-9cef3-default-rtdb.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('/users')


firebase = firebase.FirebaseApplication('https://testproject-9cef3-default-rtdb.firebaseio.com/', None)
import json
appBlueprint = Blueprint("home",__name__)


@appBlueprint.route('/webhook',methods=['POST'])
def rejectOrder():
    req = request.get_json(silent=True, force=True)
    fullfillmentText = ''
    now = datetime.now()
    query_result = req.get('queryResult')
    d2 = now.strftime("%d/%m/%Y %H:%M:%S")
    if query_result.get('action') == 'object.confirm.noUsername':
       
       Place = query_result['outputContexts'][1]["parameters"]["place"]
       objname = query_result['outputContexts'][1]["parameters"]["objname"] 
       RefNo1 = db.reference("/RememberV2/Home") 
       count = 0
       Deta = RefNo1.get()
       
       
       try:
          Deta.keys()
       except: 
          GoGo = RefNo1.child("รายการที่1")
          GoGo.set({
            "amonut":"1"
            ,"id":count+1
            ,"item":objname
            ,"Location":Place
            ,"time": d2
         })
          return {
            "fulfillmentText": "บันทึกรายการเรียบร้อย",
            "displayText": '25',
            "source": "webhookdata"
    } 
       else:
         for key in Deta.keys(): count+= 1
         GoGo = RefNo1.child("รายการที่"+str(count+1))
         GoGo.set({
            "amonut":"1"
            ,"id":count+1
            ,"item":objname
            ,"Location":Place
            ,"time": d2
            })
         return {
            "fulfillmentText": "บันทึกรายการเรียบร้อย",
            "displayText": '25',
            "source": "webhookdata"
    }
    if query_result.get('action') == 'object.confirm.withUsername':
       NameUser = query_result['outputContexts'][3]["parameters"]["uname"]
       Place = query_result['outputContexts'][3]["parameters"]["place"]
       objname = query_result['outputContexts'][3]["parameters"]["objname"] 
       RefNoUser = db.reference("/RememberV2") 
       RefNo1 = RefNoUser.child(""+NameUser)
       count = 0
       Deta = RefNo1.get()
       
       
       try:
          Deta.keys()
       except: 
          GoGo = RefNo1.child("รายการที่1")
          GoGo.set({
            "amonut":"1"
            ,"id":count+1
            ,"item":objname
            ,"Location":Place
            ,"time": d2
         })
          return {
            "fulfillmentText": "บันทึกรายการเรียบร้อย",
            "displayText": '25',
            "source": "webhookdata"
    } 
       else:
         for key in Deta.keys(): count+= 1
         GoGo = RefNo1.child("รายการที่"+str(count+1))
         GoGo.set({
            "amonut":"1"
            ,"id":count+1
            ,"item":objname
            ,"Location":Place
            ,"time": d2
            })
         return {
            "fulfillmentText": "บันทึกรายการเรียบร้อย",
            "displayText": '25',
            "source": "webhookdata"
    }
    if query_result.get('action') == 'showAll..specifyname':
      NameUser = query_result['outputContexts'][1]["parameters"]["specifyname"]
      RefNo1 = db.reference("/RememberV2")

      RefNo2 = db.reference("/ShowHistory")
      temp = RefNo2.get()
      RefNo2.update({'showAllspecifyname' :temp['showAllspecifyname'] + 1 })

      get = RefNo1.get()
      for x in get.keys():
        if x == NameUser:
          for y in get[x].keys():
            fullfillmentText +=' คุณบันทึกสิ่งของ : '+str(get[x][y]["item"])+ ' ไว้ตำแหน่ง ' + str(get[x][y]["Location"]) + "  "   
       
    if query_result.get('action') == 'showAllrequest-no':
      RefNo1 = db.reference("/RememberV2/Home") 
      get = RefNo1.get()
      ##
      RefNo2 = db.reference("/ShowHistory")
      temp = RefNo2.get()
      RefNo2.update({'showAllrequestNo' :temp['showAllrequestNo'] + 1 })


      for x in get.keys():
        fullfillmentText +=' คุณบันทึกสิ่งของ : '+str(get[x]["item"])+ ' ไว้ตำแหน่ง ' + str(get[x]["Location"]) + "  "

    if query_result.get('action') == 'showSpecify.inform':
      NameUser = query_result['outputContexts'][1]["parameters"]["informname"]
      item = query_result['outputContexts'][1]["parameters"]["specifyItemName"]
      RefNo1 = db.reference("/RememberV2") 
      ##
      RefNo2 = db.reference("/ShowHistory")
      temp = RefNo2.get()
      RefNo2.update({'showSpecifyInform' :temp['showSpecifyInform'] + 1 })

      get = RefNo1.get()
      for name in get.keys():
        if name == NameUser:
          for itemlist in get[name].keys():
            if get[name][itemlist]["item"] == item:
              fullfillmentText +=' คุณบันทึกสิ่งของไว้ที่ ' + str(get[name][itemlist]["Location"]) + "  " 

    if query_result.get('action') == 'specifyItemname.no.inform':
      item = query_result['outputContexts'][1]["parameters"]["specifyItemName"]
      RefNo1 = db.reference("/RememberV2/Home") 
      ##
      RefNo2 = db.reference("/ShowHistory")
      temp = RefNo2.get()
      RefNo2.update({'specifyItemnameNoInform' :temp['specifyItemnameNoInform'] + 1 })

      get = RefNo1.get()
      for x in get.keys():
        if get[x]["item"] == item :
          fullfillmentText +=' คุณบันทึกสิ่งของไว้ที่ ' + str(get[x]["Location"]) + "  "

    if query_result.get('action') == 'showHistory':
      ref1 = db.reference("/ShowHistory").get()
      ref2 = db.reference("/RememberV2/Home") 
      get2 = ref2.get()
      showallno = 0
      for x in get2.keys():
        showallno += 1
      ref3 = db.reference("/RememberV2")
      get3 = ref3.get()
      showall = 0
      temp = "Home"
      for x in get3.keys():
        if x != temp:
          for y in get3[x].keys():
            showall += 1
      a='คุณได้บันทึกของที่ไม่มีเจ้าของไป '+str(showallno)+' ครั้ง '
      b=',คุณได้บันทึกของที่มีเจ้าของไป '+str(showall) +' ครั้ง'
      c=' และ คุณใช้คำสั่งแสดงของทั้งหมดที่ไม่มีชื่อเจ้าของ '+str(ref1["showAllrequestNo"])+' ครั้ง'
      d=' คุณใช้คำสั่งแสดงของทั้งหมดที่มีชื่อเจ้าของ '+str(ref1["showAllspecifyname"])+' ครั้ง'
      e=' คุณใช้คำสั่งแสดงตำแหน่งของที่ไม่มีชื่อเจ้าของ '+str(ref1["showSpecifyInform"])+' ครั้ง'
      f=' คุณใช้คำสั่งแสดงตำแหน่งของที่มีชื่อเจ้าของ '+str(ref1["specifyItemnameNoInform"])+ ' ครั้ง'
      fullfillmentText = a+b+c+d+e+f 

    return {
            "fulfillmentText": fullfillmentText,
            "displayText": '25',
            "source": "webhookdata"
    }  

