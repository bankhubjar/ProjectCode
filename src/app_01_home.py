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

SCOPES = ['https://www.googleapis.com/auth/calendar']

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

@appBlueprint.route('/test2')
def testcheck2():
    data =''
    with open("./src/message.json", errors='ignore') as read_file:
       data = json.load(read_file)
    # query_result['parameters'][1]['showreminderdate']
    return data["queryResult"]['parameters']['showreminderdate'][0]

def testcheck(mintimeformDialog,maxtimeformDialog):
    ful = ''
    i = 0
    start =[]
    now = ''
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    if not mintimeformDialog:
      now = datetime.utcnow().isoformat() + 'Z'   
    else:
      now = mintimeformDialog
    if not maxtimeformDialog:
      events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    else:    
      events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=maxtimeformDialog,maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        start.append('ไม่มีกิจกรรมแม้แต่นิดเดียวเลยเจ้าค่ะ.')
    for event in events:
        eiei = event['start'].get('dateTime', event['start'].get('date'))
        start.append('การแจ้งเตือนของคุณมี '+event['summary']+' ตอน '+str(eiei.split("T")[0])+' เวลา '+str(eiei.split("T")[1].split("+")[0])+'')
    for x in start:
      ful += x 
    return str(ful)
      # i = 0 
      # fullfillmentText = 'eiei'

      # calendarArray = callCa(checkService())
      # while i > 3:
      #    fullfillmentText += calendarArray[i]
        #  i+=1
        
def checkJson(data,name):
    kiki = 0
    ides = 0
    if not name:
      while ides < len(data['outputContexts']):
        try:
          NameUser = data['outputContexts'][ides]["parameters"]["uname"]
          Place = data['outputContexts'][ides]["parameters"]["place"]
          objname = data['outputContexts'][ides]["parameters"]["objname"]        
        except:
          kiki+= 1
          ides+=1
        else:
          NameUser = data['outputContexts'][ides]["parameters"]["uname"]
          Place = data['outputContexts'][ides]["parameters"]["place"]
          objname = data['outputContexts'][ides]["parameters"]["objname"]
          break
    else:
      while ides < len(data['outputContexts']):
        try:
         Place = data['outputContexts'][ides]["parameters"]["place"]
         objname = data['outputContexts'][ides]["parameters"]["objname"]        
        except:
            kiki+= 1
            ides+=1
        else:
          Place = data['outputContexts'][ides]["parameters"]["place"]
          objname = data['outputContexts'][ides]["parameters"]["objname"]
          break
    return ides

def checkJsonForCalendar(data):
    kiki = 0
    ides = 0
    while ides < len(data['outputContexts']):
      try:
        aany = data['outputContexts'][ides]["parameters"]["any"]
        datetime = data['outputContexts'][ides]["parameters"]["datetime"]
 
      except:
        kiki+= 1
        ides+=1
      else:
        aany = data['outputContexts'][ides]["parameters"]["any"]
        dateime = data['outputContexts'][ides]["parameters"]["datetime"]
        break
    return ides

def checkJsonForActivity(data):
    kiki = 0
    ides = 0
    while ides < len(data['outputContexts']):
      try:
        aany = data['outputContexts'][ides]["parameters"]["activityname"]
        datetime = data['outputContexts'][ides]["parameters"]["activitytime"]
 
      except:
        kiki+= 1
        ides+=1
      else:
        aany = data['outputContexts'][ides]["parameters"]["activityname"]
        dateime = data['outputContexts'][ides]["parameters"]["activitytime"]
        break
    return ides

def checkJsonForItem(data,informname):
    kiki = 0
    ides = 0
    if not informname:
      while ides < len(data['outputContexts']):
        try:
          informname = data['outputContexts'][ides]["parameters"]["informname"]
          specifyItemName = data['outputContexts'][ides]["parameters"]["specifyItemName"]
        except:
          kiki+= 1
          ides+=1
        else:
          informname = data['outputContexts'][ides]["parameters"]["informname"]
          specifyItemName = data['outputContexts'][ides]["parameters"]["specifyItemName"]
        break
    else:
      while ides < len(data['outputContexts']):
        try:
            specifyItemName = data['outputContexts'][ides]["parameters"]["specifyItemName"]
        except:
            kiki+= 1
            ides+=1
        else:
          specifyItemName = data['outputContexts'][ides]["parameters"]["specifyItemName"]
          break
    return ides

def checkService():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service

def callCa(service):
    count = 0
    start = []
    text = ''
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,maxResults=10, singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        start[0]='No upcoming events found.'
    for event in events:
        text = str(event['start'].get('dateTime', event['start'].get('date')))
        start.append(text+''+str(event['summary'])) 
    return start    

@appBlueprint.route('/test1')
def wtf():
       fullfillmentText=''
       RefEvent = db.reference("/EventReminder")
       getEvent = RefEvent.get()
       Event = []
       a=''
       try:
        getEvent.keys()
       except:
         fullfillmentText = 'ไม่มีการบันทึกกิจกรรม'
       else:
         for x in getEvent.keys():
           fullfillmentText+='กิจกรรมของคุณคือ'+getEvent[x]['event']+'ต้องทำตอน'+getEvent[x]['time']+'วันที่'+getEvent[x]['date']+""
       return fullfillmentText

@appBlueprint.route('/calendar')
def calendar():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './src/credentials.json', scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    result = service.calendarList().list().execute()
    calendar_id = result['items'][0]['id']
    # Call the Calendar API
    event = "bruh"
    datetimeq = "2021-02-27T15:00:00+07:00"
    eventcontent = {
        'summary': event,
        'location': '',
        'description': '',
        'start': {
          'dateTime': datetimeq,
          'timeZone': 'Asia/Bangkok',
        },
        'end': {
          'dateTime': datetimeq,
          'timeZone': 'Asia/Bangkok',
        },
        'reminders': {
          'useDefault': False,
          'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
          ],
        },
      }
    service.events().insert(calendarId=calendar_id, body=eventcontent).execute()
    return "sent event to "+calendar_id

@appBlueprint.route('/webhook',methods=['POST'])
def rejectOrder():
    RequestJson = request.get_json(silent=True, force=True)
    fullfillmentText = ''
    CurrentTime = datetime.now(tz)
    query_result = RequestJson.get('queryResult')
    DateMonthYear = CurrentTime.strftime("%d/%m/%Y")
    HourMinuteSecond = CurrentTime.strftime("%H:%M:%S")

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
                './src/credentials.json', scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    result = service.calendarList().list().execute()
    calendar_id = result['items'][0]['id']

    if query_result.get('action') == 'object.confirm.noUsername': 
       Place = query_result['outputContexts'][checkJson(query_result,"")]["parameters"]["place"]
       objname = query_result['outputContexts'][checkJson(query_result,"")]["parameters"]["objname"] 
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
        NameUser = query_result['outputContexts'][checkJson(query_result,"name")]["parameters"]["uname"]
        Place = query_result['outputContexts'][checkJson(query_result,"name")]["parameters"]["place"]
        objname = query_result['outputContexts'][checkJson(query_result,"name")]["parameters"]["objname"]
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

    if query_result.get('action') == 'reminder.Time':
      event = query_result['outputContexts'][checkJsonForCalendar(query_result)]["parameters"]["any"]
      datetimeq = query_result['outputContexts'][checkJsonForCalendar(query_result)]["parameters"]["datetime"]
      date = datetimeq.split("T")[0]
      time = datetimeq.split("T")[1].split("+")[0]
      fulfillmentText = "คุณได้บันทึกกิจกรรมไว้ว่า "+event+" ที่เวลา "+time+" ในวันที่ "+date
      RefFromDatabase = db.reference("/EventReminder") 
      count = 0
      time_zone = 'Asia/Bangkok'
      eventcontent = {
        'summary': event,
        'description': event,
        'start': {
          'dateTime': datetimeq,
          'timeZone': time_zone,
        },
        'end': {
          'dateTime': datetimeq,
          'timeZone': time_zone,
        },
        'reminders': {
          'useDefault': False,
          'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
          ],
        },
      }
      Data = RefFromDatabase.get()
      try:
        Data.keys()
      except:
        ListToDb = RefFromDatabase.child("กิจกรรมที่ 1")
        ListToDb.set({"id":count+1,"event":event,"date":date,"time":time})
        ##      
        service.events().insert(calendarId=calendar_id, body=eventcontent).execute()
        ##
        return {
          "fulfillmentText": fulfillmentText,
          "displayText": '25',
          "source": "webhookdata"
        }
      else:
        for key in Data.keys(): count += 1
        ListToDb = RefFromDatabase.child("กิจกรรมที่ "+str(count+1))
        ListToDb.set({"id":count+1,"event":event,"date":date,"time":time})
        ##
        service.events().insert(calendarId=calendar_id, body=eventcontent).execute()
        ##
        return {
          "fulfillmentText": fulfillmentText,
          "displayText": '25',
          "source": "webhookdata"
        }
             
    if query_result.get('action') == 'showAll..specifyname':
      try:
        NameUserser = query_result['outputContexts'][checkJsonForItem(query_result,"")]["parameters"]["specifyname"]
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
        NameUserser = query_result['outputContexts'][checkJsonForItem(query_result,"informname")]["parameters"]["informname"]
        if "specifyItemName" in query_result:
          item = query_result['outputContexts'][checkJsonForItem(query_result,"informname")]["parameters"]["specifyItemName"]
        else:
          item = query_result['outputContexts'][checkJsonForItem(query_result,"informname")]["parameters"]["specifyItemName"]
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
          item = query_result['outputContexts'][checkJsonForItem(query_result,"")]["parameters"]["specifyItemName"]
        else:
          item = query_result['outputContexts'][checkJsonForItem(query_result,"")]["parameters"]["specifyItemName"]
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
    if query_result.get('action') == 'showReminder.All':
      #  RefEvent = db.reference("/EventReminder")
      #  getEvent = RefEvent.get()
      #  Event = []
      #  a=''
      #  try:
      #   getEvent.keys()
      #  except:
      #    fullfillmentText = 'ไม่มีการบันทึกกิจกรรม'
      #  else:
      #    for x in getEvent.keys():
      #      fullfillmentText='กิจกรรมของคุณคือ'+getEvent[x]['event']+'ต้องทำตอน'+getEvent[x]['time']+'วันที่'+getEvent[x]['date']+""
       return {
            "fulfillmentText": testcheck("",""),
            "displayText": '50',
            "source": "webhookdata"
      }

    if query_result.get('action') == 'showReminder.Date':
      datefromdialog =  query_result['parameters']['showreminderdate'][0]
      return {
        "fulfillmentText": testcheck(datefromdialog,""),
        "displayText": '50',
        "source": "webhookdata"
      }

    if query_result.get('action') == 'activityTime':
      activityname = query_result['outputContexts'][checkJsonForActivity(query_result)]['parameters']['activityname']
      activitytime = query_result['outputContexts'][checkJsonForActivity(query_result)]['parameters']['activitytime']
      datetimea = query_result['outputContexts'][checkJsonForActivity(query_result)]['parameters']['date']
      date = datetimea.split("T")[0]
      time = activitytime.split("T")[1].split("+")[0]
      temptime = datetimea.split("T")[0]+"T"+activitytime.split("T")[1]
      fulfillmentText = "คุณได้บันทึกกิจกรรม "+activityname+" ที่เวลา "+time+" ในวันที่ "+date
      RefFromDatabase = db.reference("/ActivityReminder") 
      count = 0
      time_zone = 'Asia/Bangkok'
      eventcontent = {
        'summary': activityname,
        'description': activityname,
        'start': {
          'dateTime': temptime,
          'timeZone': time_zone,
        },
        'end': {
          'dateTime': temptime,
          'timeZone': time_zone,
        },
        'reminders': {
          'useDefault': False,
          'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
          ],
        },
      }
      Data = RefFromDatabase.get()
      try:
        Data.keys()
      except:
        ListToDb = RefFromDatabase.child("กิจกรรมที่ 1")
        ListToDb.set({"id":count+1,"event":activityname,"date":date,"time":time})
        ##      
        service.events().insert(calendarId=calendar_id, body=eventcontent).execute()
        ##
        return {
          "fulfillmentText": fulfillmentText,
          "displayText": '25',
          "source": "webhookdata"
        }
      else:
        for key in Data.keys(): count += 1
        ListToDb = RefFromDatabase.child("กิจกรรมที่ "+str(count+1))
        ListToDb.set({"id":count+1,"event":activityname,"date":date,"time":time})
        ##
        service.events().insert(calendarId=calendar_id, body=eventcontent).execute()
        ##
        return {
          "fulfillmentText": fulfillmentText,
          "displayText": '25',
          "source": "webhookdata"
        } 


    return {
            "fulfillmentText": fullfillmentText,
            "displayText": '50',
            "source": "webhookdata"
      }  
    

