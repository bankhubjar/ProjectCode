#Python Flask
from flask import Blueprint
from flask import Flask, render_template
from flask import Flask,request
from flask import Flask, render_template, url_for, json

import urllib
from urllib.parse import unquote

#FirebaseDatabase
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import db
import os

#Time
from datetime import datetime
import pytz

# Googlecalendar Api
import os.path

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

tz = pytz.timezone('Asia/Bangkok')

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

@appBlueprint.route('/calendar')
def calendar():
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './src/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    start = ''
    if not events:
        start ='No upcoming events found.'
    for event in events:
        start = start +event['start'].get('dateTime', event['start'].get('date'))+''+event['summary']+"<br>"
    return start   



@appBlueprint.route('/webhook',methods=['POST'])
def rejectOrder():
    RequestJson = request.get_json(silent=True, force=True)
    fullfillmentText = ''
    CurrentTime = datetime.now(tz)
    query_result = RequestJson.get('queryResult')
    DateMonthYear = CurrentTime.strftime("%d/%m/%Y")
    HourMinuteSecond = CurrentTime.strftime("%H:%M:%S")
    if query_result.get('action') == 'object.confirm.noUsername': 
       Place = query_result['outputContexts'][1]["parameters"]["place"]
       objname = query_result['outputContexts'][1]["parameters"]["objname"] 
       RefFromDatabase = db.reference("/RememberV2/Home") 
       count = 0
       Deta = RefFromDatabase.get()

       try:
          Deta.keys()
       except: 
          ListToDB = RefFromDatabase.child("รายการที่1")
          ListToDB.set({
            "amonut":"1"
            ,"id":count+1
            ,"item":objname
            ,"Location":Place
            ,"Date": DateMonthYear
            ,"time": HourMinuteSecond
         })
          return {
            "fulfillmentText": "บันทึกรายการเรียบร้อย",
            "displayText": '25',
            "source": "webhookdata"
    } 
       else:
         for key in Deta.keys(): count+= 1
         ListToDB = RefFromDatabase.child("รายการที่"+str(count+1))
         ListToDB.set({
            "amonut":"1"
            ,"id":count+1
            ,"item":objname
            ,"Location":Place
            ,"Date": DateMonthYear
            ,"time": HourMinuteSecond
            })
         return {
            "fulfillmentText": "บันทึกรายการเรียบร้อย",
            "displayText": '25',
            "source": "webhookdata"
    }
    if query_result.get('action') == 'object.confirm.withUsername':
      RefNoUser = db.reference("/RememberV2") 
      try:
        NameUser = query_result['outputContexts'][3]["parameters"]["uname"]
        Place = query_result['outputContexts'][3]["parameters"]["place"]
        objname = query_result['outputContexts'][3]["parameters"]["objname"]
        RefFromDatabase = RefNoUser.child(""+NameUser)
        count = 0
        Deta = RefFromDatabase.get()
        try:
            Deta.keys()
        except: 
            ListToDB = RefFromDatabase.child("รายการที่1")
            ListToDB.set({
              "amonut":"1"
              ,"id":count+1
              ,"item":objname
              ,"Location":Place
              ,"Date": DateMonthYear
              ,"time": HourMinuteSecond
          })
            return {
              "fulfillmentText": "บันทึกรายการเรียบร้อย",
              "displayText": '25',
              "source": "webhookdata"
      } 
        else:
          for key in Deta.keys(): count+= 1
          ListToDB = RefFromDatabase.child("รายการที่"+str(count+1))
          ListToDB.set({
              "amonut":"1"
              ,"id":count+1
              ,"item":objname
              ,"Location":Place
              ,"Date": DateMonthYear
              ,"time": HourMinuteSecond
              })
          return {
              "fulfillmentText": "บันทึกรายการเรียบร้อย",
              "displayText": '25',
              "source": "webhookdata"
       }
      except:
        NameUser = query_result['outputContexts'][8]["parameters"]["uname"]
        Place = query_result['outputContexts'][8]["parameters"]["place"]
        objname = query_result['outputContexts'][8]["parameters"]["objname"]
        RefFromDatabase = RefNoUser.child(""+NameUser)
        count = 0
        Deta = RefFromDatabase.get()
        try:
            Deta.keys()
        except: 
            ListToDB = RefFromDatabase.child("รายการที่1")
            ListToDB.set({
              "amonut":"1"
              ,"id":count+1
              ,"item":objname
              ,"Location":Place
              ,"Date": DateMonthYear
              ,"time": HourMinuteSecond
          })
            return {
              "fulfillmentText": "บันทึกรายการเรียบร้อย",
              "displayText": '25',
              "source": "webhookdata"
      } 
        else:
          for key in Deta.keys(): count+= 1
          ListToDB = RefFromDatabase.child("รายการที่"+str(count+1))
          ListToDB.set({
              "amonut":"1"
              ,"id":count+1
              ,"item":objname
              ,"Location":Place
              ,"Date": DateMonthYear
              ,"time": HourMinuteSecond
              })
          return {
              "fulfillmentText": "บันทึกรายการเรียบร้อย",
              "displayText": '25',
              "source": "webhookdata"
       } 

    if query_result.get('action') == 'Reminder-TIme':
      event = query_result['outputContexts'][0]["parameters"]["any"]
      time = query_result['outputContexts'][0]["parameters"]["time"]
      fulfillmentText = "คุณได้บันทึกกิจกรรมไว้ว่า "+event+" ที่เวลา "+time
      RefFromDatabase = db.reference("/EventReminder") 
      count = 0
      Data = RefFromDatabase.get()
      try:
        Data.keys()
      except:
        ListToDb = RefFromDatabase.child("กิจกรรมที่ 1")
        ListToDb.set({"id":count+1,"event":event,"date":time})
        return {
          "fulfillmentText": fulfillmentText,
          "displayText": '25',
          "source": "webhookdata"
        }
      else:
        for key in Data.keys(): count += 1
        ListToDb = RefFromDatabase.child("กิจกรรมที่ "+str(count+1))
        ListToDb.set({"id":count+1,"event":event,"date":time})
        return {
          "fulfillmentText": fulfillmentText,
          "displayText": '25',
          "source": "webhookdata"
        }
             
    if query_result.get('action') == 'showAll..specifyname':
      try:
        NameUserser = query_result['outputContexts'][1]["parameters"]["specifyname"]
        RefFromDatabase = db.reference("/RememberV2")

        RefNo2 = db.reference("/ShowHistory")
        temp = RefNo2.get()
        RefNo2.update({'showAllspecifyname' :temp['showAllspecifyname'] + 1 })

        get = RefFromDatabase.get()
        for x in get.keys():
          if x == NameUserser:
            for y in get[x].keys():
              fullfillmentText +=' คุณบันทึกสิ่งของ : '+str(get[x][y]["item"])+ ' ไว้ตำแหน่ง ' + str(get[x][y]["Location"]) + "  "   
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'

    if query_result.get('action') == 'showAllrequest-no':
      try:
        RefFromDatabase = db.reference("/RememberV2/Home") 
        get = RefFromDatabase.get()
        ##
        RefNo2 = db.reference("/ShowHistory")
        temp = RefNo2.get()
        RefNo2.update({'showAllrequestNo' :temp['showAllrequestNo'] + 1 })

        for x in get.keys():
          fullfillmentText +=' คุณบันทึกสิ่งของ : '+str(get[x]["item"])+ ' ไว้ตำแหน่ง ' + str(get[x]["Location"]) + "  "
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'

    if query_result.get('action') == 'showSpecify.inform':
      try:
        NameUserser = query_result['outputContexts'][1]["parameters"]["informname"]
        if "specifyItemName" in query_result:
          item = query_result['outputContexts'][1]["parameters"]["specifyItemName"]
        else:
          item = query_result['outputContexts'][6]["parameters"]["specifyItemName"]
        RefFromDatabase = db.reference("/RememberV2") 
        ##
        RefNo2 = db.reference("/ShowHistory")
        temp = RefNo2.get()
        RefNo2.update({'showSpecifyInform' :temp['showSpecifyInform'] + 1 })

        get = RefFromDatabase.get()
        for name in get.keys():
          if name == NameUserser:
            for itemlist in get[name].keys():
              if get[name][itemlist]["item"] == item:
                fullfillmentText +=' คุณบันทึกสิ่งของไว้ที่ ' + str(get[name][itemlist]["Location"]) + "  " 
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'

    if query_result.get('action') == 'specifyItemname.no.inform':
      try:
        if "specifyItemName" in query_result:
          item = query_result['outputContexts'][1]["parameters"]["specifyItemName"]
        else:
          item = query_result['outputContexts'][5]["parameters"]["specifyItemName"]
        RefFromDatabase = db.reference("/RememberV2/Home") 
        ##
        RefNo2 = db.reference("/ShowHistory")
        temp = RefNo2.get()
        RefNo2.update({'specifyItemnameNoInform' :temp['specifyItemnameNoInform'] + 1 })

        get = RefFromDatabase.get()
        for x in get.keys():
          if get[x]["item"] == item :
            fullfillmentText +=' คุณบันทึกสิ่งของไว้ที่ ' + str(get[x]["Location"]) + "  "
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'

    if query_result.get('action') == 'showHistory':
      try:
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
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'
    if fullfillmentText == '':
      fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'  

    return {
            "fulfillmentText": fullfillmentText,
            "displayText": '25',
            "source": "webhookdata"
    }  

