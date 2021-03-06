# ------------------------------------------------------------------------------------# 
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
from datetime import datetime, timedelta
import pytz

# Googlecalendar Api
import os.path

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import json

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

# ------------------------------------------------------------------------------------# 

appBlueprint = Blueprint("home",__name__)
 
# ------------------------------------------------------------------------------------# 
# Function Check Data

def testcheck(mintimeformDialog,maxtimeformDialog):
    ful = ''
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
        start.append('ไม่มีการแจ้งเตือนแม้แต่นิดเดียวเลยเจ้าค่ะ <break time="200ms"/> ')
    for event in events:
        TextResponse = event['start'].get('dateTime', event['start'].get('date'))
        start.append('<s>'+event['summary']+'  <break time="200ms"/> ตอน '+'<say-as interpret-as="date" format="yyyymmdd" detail="1">'+str(TextResponse.split("T")[0])+'</say-as><break time="200ms"/> เวลา '+str(TextResponse.split("T")[1].split("+")[0])+'<break time="200ms"/> </s>')
    for x in start:
      ful += x 
    return str('<speak><p> การแจ้งเตือนของคุณมี '+ful+'เจ้าค่ะ</p></speak>')

        
def checkJson(data,name):   
    jsonIndex = 0
    if name == "name":
      while jsonIndex < len(data['outputContexts']):
        try:
          NameUser = data['outputContexts'][jsonIndex]["parameters"]["uname"]
          Place = data['outputContexts'][jsonIndex]["parameters"]["place"]
          objname = data['outputContexts'][jsonIndex]["parameters"]["objname"]        
        except: 
          jsonIndex+=1
        else:
          NameUser = data['outputContexts'][jsonIndex]["parameters"]["uname"]
          Place = data['outputContexts'][jsonIndex]["parameters"]["place"]
          objname = data['outputContexts'][jsonIndex]["parameters"]["objname"]
          break
    else:
      while jsonIndex < len(data['outputContexts']):
        try:
         Place = data['outputContexts'][jsonIndex]["parameters"]["place"]
         objname = data['outputContexts'][jsonIndex]["parameters"]["objname"]        
        except:
            jsonIndex+=1
        else:
          Place = data['outputContexts'][jsonIndex]["parameters"]["place"]
          objname = data['outputContexts'][jsonIndex]["parameters"]["objname"]
          break
    return jsonIndex

def checkJsonForCalendar(data):
    jsonIndex = 0
    while jsonIndex < len(data['outputContexts']):
      try:
        aany = data['outputContexts'][jsonIndex]["parameters"]["any"]
        datetime = data['outputContexts'][jsonIndex]["parameters"]["date"]
      except:   
        jsonIndex+=1
      else:
        aany = data['outputContexts'][jsonIndex]["parameters"]["any"]
        dateime = data['outputContexts'][jsonIndex]["parameters"]["date"]
        break
    return jsonIndex

def checkJsonForActivity(data):
    
    jsonIndex = 0
    while jsonIndex < len(data['outputContexts']):
      try:
        aany = data['outputContexts'][jsonIndex]["parameters"]["activityname"]
        datetime = data['outputContexts'][jsonIndex]["parameters"]["activitytime"]
 
      except:
        jsonIndex+=1
      else:
        aany = data['outputContexts'][jsonIndex]["parameters"]["activityname"]
        dateime = data['outputContexts'][jsonIndex]["parameters"]["activitytime"]
        break
    return jsonIndex

def checkJsonForItem(data,informname):
    jsonIndex = 0
    if informname == "informname":
      while jsonIndex < len(data['outputContexts']):
        try:
          informname = data['outputContexts'][jsonIndex]["parameters"]["informname"]
          specifyItemName = data['outputContexts'][jsonIndex]["parameters"]["specifyItemName"]
        except:   
          jsonIndex+=1
        else:
          informname = data['outputContexts'][jsonIndex]["parameters"]["informname"]
          specifyItemName = data['outputContexts'][jsonIndex]["parameters"]["specifyItemName"]
        break
    else:
      while jsonIndex < len(data['outputContexts']):
        try:
            specifyItemName = data['outputContexts'][jsonIndex]["parameters"]["specifyItemName"]
        except:
            jsonIndex+=1
        else:
          specifyItemName = data['outputContexts'][jsonIndex]["parameters"]["specifyItemName"]
          break
    return jsonIndex

def checkJsonToday(data):   
    jsonIndex = 0
    while jsonIndex < len(data['outputContexts']):
      try:
        datet = data['outputContexts'][jsonIndex]["parameters"]["showreminderdate.original"]
      except:
        jsonIndex+=1
      else:
        datet = data['outputContexts'][jsonIndex]["parameters"]["showreminderdate.original"]
        break
    return jsonIndex

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
              './src/credentials.json', scopes=SCOPES)
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

def savehistory(service):
  DBRef = db.reference("/ShowHistory")
  deta = DBRef.get()
  if service in data:
    oldhistory = data
    DBRef.update({service : oldhistory[service]+1})
  else: 
    DBRef.update({service : 1})

# ------------------------------------------------------------------------------------# 
# Webhook Part

@appBlueprint.route('/webhook',methods=['POST'])
def rejectOrder():
    RequestJson = request.get_json(silent=True, force=True)
    fullfillmentText = ''
    CurrentTime = datetime.now(tz)
    query_result = RequestJson.get('queryResult')
    DateMonthYear = CurrentTime.strftime("%d/%m/%Y")
    HourMinuteSecond = CurrentTime.strftime("%H:%M:%S")

# Intent: [Remember] enterUsername - Reject
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
          savehistory("remember")
          return {
            "fulfillmentText": "บันทึกรายการเรียบร้อยเจ้าค่ะ",
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
          savehistory("remember")
          return {
            "fulfillmentText": "บันทึกรายการเรียบร้อยเจ้าค่ะ",
            "displayText": '25',
            "source": "webhookdata"
      }

# Intent: [Remember] enterUsername - confirmed
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
            savehistory("remember")
            return {
              "fulfillmentText": "บันทึกรายการเรียบร้อยเจ้าค่ะ",
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
          savehistory("remember")
          return {
              "fulfillmentText": "บันทึกรายการเรียบร้อยเจ้าค่ะ",
              "displayText": '25',
              "source": "webhookdata"
       } 


# Intent: [Reminder] Reminder - Time
    if query_result.get('action') == 'reminder.Time':
      event = query_result['outputContexts'][checkJsonForCalendar(query_result)]["parameters"]["any"]
      if query_result['outputContexts'][checkJsonForCalendar(query_result)]["parameters"]["date"] == "" :
        datewithtime = query_result['outputContexts'][checkJsonForCalendar(query_result)]["parameters"]["time"]
        date = datewithtime.split("T")[0]
        time = datewithtime.split("T")[1].split("+")[0]
        eventtime = datewithtime
      else :
        dateonly = query_result['outputContexts'][checkJsonForCalendar(query_result)]["parameters"]["date"]
        timeonly = query_result['outputContexts'][checkJsonForCalendar(query_result)]["parameters"]["time"]
        date = dateonly.split("T")[0]
        time = timeonly.split("T")[1].split("+")[0]
        eventtime = dateonly.split("T")[0]+"T"+timeonly.split("T")[1]
      # --- edit ---
      fulfillmentText = "คุณได้บันทึกการเเจ้งเตือนไว้ว่า " + event + " <break time='300ms'/> " + " ที่เวลา "+ time + " <break time='300ms'/> " + " ในวันที่ " + " <say-as interpret-as='date' format='yyyymmdd' detail='1'> " + date + " เจ้าค่ะ</say-as> "
      RefFromDatabase = db.reference("/EventReminder") 
      count = 0
      result = checkService().calendarList().list().execute()
      service = checkService()
      calendar_id = result['items'][2]['id']
      time_zone = 'Asia/Bangkok'
      eventcontent = {
        'summary': event,
        'description': event,
        'start': {
          'dateTime': eventtime,
          'timeZone': time_zone,
        },
        'end': {
          'dateTime': eventtime,
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
        savehistory("reminder")
        # --- edit ---
        return {
          "fulfillmentText": "<speak>" + fulfillmentText + "</speak>",
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
        savehistory("reminder")
      return {
        # --- edit ---
        "fulfillmentText": "<speak>" + fulfillmentText + "</speak>",
        "displayText": '25',
        "source": "webhookdata"
      }

# Intent: [Activity] Activity - Time
    if query_result.get('action') == 'activityTime':
      activityname = query_result['outputContexts'][checkJsonForActivity(query_result)]['parameters']['activityname']
      if query_result['outputContexts'][checkJsonForActivity(query_result)]["parameters"]["date"] == "" :
        datewithtime = query_result['outputContexts'][checkJsonForActivity(query_result)]["parameters"]["activitytime"]
        date = datewithtime.split("T")[0]
        time = datewithtime.split("T")[1].split("+")[0]
        temptime = datewithtime
      else :
        dateonly = query_result['outputContexts'][checkJsonForActivity(query_result)]["parameters"]["date"]
        timeonly = query_result['outputContexts'][checkJsonForActivity(query_result)]["parameters"]["activitytime"]
        date = dateonly.split("T")[0]
        time = timeonly.split("T")[1].split("+")[0]
        temptime = dateonly.split("T")[0]+"T"+timeonly.split("T")[1]
      # --- edit ---
      fulfillmentText = "คุณได้บันทึกกิจกรรมไว้ว่า " + activityname + " <break time='300ms'/> "  + " ที่เวลา " + time + " <break time='300ms'/> "  +" ในวันที่ " + " <say-as interpret-as='date' format='yyyymmdd' detail='1'> " + date + "เจ้าค่ะ </say-as> "
      RefFromDatabase = db.reference("/ActivityReminder") 
      count = 0
      result = checkService().calendarList().list().execute()
      service = checkService()
      calendar_id = result['items'][2]['id']
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
        savehistory("activity")
        return {
          # --- edit ---
          "fulfillmentText": "<speak>" + fulfillmentText + "</speak>",
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
        savehistory("activity")
        return {
          # --- edit ---
          "fulfillmentText": "<speak>" + fulfillmentText + "</speak>",
          "displayText": '25',
          "source": "webhookdata"
        }      

# ------------------------------------------------------------------------------------# 
# show Part

# Intent: [showRemember - All] showRemember - specifyname
    if query_result.get('action') == 'showAll..specifyname':
      try:
        NameUserser = query_result['outputContexts'][checkJsonForItem(query_result,"")]["parameters"]["specifyname"]
        RefFromDatabase = db.reference("/RememberV2")
        get = RefFromDatabase.get()
        textresponse = ''
        for x in get.keys():
          if x == NameUserser:
            for y in get[x].keys():
              textresponse +='<s>'+str(get[x][y]["item"])+ '<break time="300ms"/>  ไว้ที่ <break time="300ms"/> ' + str(get[x][y]["Location"]) + '</s>'+" "   
              fullfillmentText = '<speak><p>สิ่งของที่คุณให้จดจำคือ <break time="300ms"/> '+ textresponse+'</p></speak>'
      except:
        fullfillmentText = '<speak>ขอโทษด้วย <break time="300ms"/> ฉันไม่พบสิ่งของที่คุณต้องการเจ้าค่ะ  <break time="300ms"/></speak>'

# Intent: [showRemember - All] showRemember - No
    if query_result.get('action') == 'showAllrequest-no':
      try:
        RefFromDatabase = db.reference("/RememberV2/Home")
        textresponse = '' 
        get = RefFromDatabase.get()
        for x in get.keys():
           textresponse +='<s>'+str(get[x]["item"])+ '<break time="300ms"/>  ไว้ที่ <break time="300ms"/> ' + str(get[x]["Location"]) + '</s>'+" "   
           fullfillmentText = '<speak><p>สิ่งของที่คุณให้จดจำคือ <break time="300ms"/> '+ textresponse+'</p></speak>'
      except:
          fullfillmentText = '<speak>ขอโทษด้วย <break time="300ms"/> ฉันไม่พบสิ่งของที่คุณต้องการเจ้าค่ะ  <break time="300ms"/></speak>'

# Intent: [showRemember - specifyItemname] specifyItemname - specifyname
    if query_result.get('action') == 'showSpecify.inform':
      try:
        NameUserser = query_result['outputContexts'][checkJsonForItem(query_result,"informname")]["parameters"]["informname"]
        item = query_result['outputContexts'][checkJsonForItem(query_result,"informname")]["parameters"]["specifyItemName"]
        RefFromDatabase = db.reference("/RememberV2") 
        textresponse = '' 
        get = RefFromDatabase.get()
        for name in get.keys():
          if name == NameUserser:
            for itemlist in get[name].keys():
              if get[name][itemlist]["item"] == item:
                textresponse +='<s>คุณจดจำสิ่งของไว้ที่ <break time="300ms"/> '+str(get[name][itemlist]["Location"]) + '<break time="300ms"/> </s>'+" "   
                fullfillmentText = '<speak><p>'+ textresponse+'</p></speak>'
      except:
          fullfillmentText = '<speak>ขอโทษด้วย <break time="300ms"/> ฉันไม่พบสิ่งของที่คุณต้องการเจ้าค่ะ <break time="300ms"/></speak>'

# Intent: [showRemember - specifyItemname] specifyItemname - no
    if query_result.get('action') == 'specifyItemname.no.inform':
      try:
        item = query_result['outputContexts'][checkJsonForItem(query_result,"")]["parameters"]["specifyItemName"]
        RefFromDatabase = db.reference("/RememberV2/Home") 
        textresponse = '' 
        get = RefFromDatabase.get()
        for x in get.keys():
          if get[x]["item"] == item :
             textresponse +='<s>คุณจดจำสิ่งของไว้ที่ <break time="300ms"/> '+str(get[x]["Location"])+ '<break time="300ms"/> </s>'+" "     
             fullfillmentText = '<speak><p>'+ textresponse+'</p></speak>'
      except:
        fullfillmentText = '<speak>ขอโทษด้วย <break time="300ms"/> ฉันไม่พบสิ่งของที่คุณต้องการเจ้าค่ะ  <break time="300ms"/></speak>'

# Intent: [showReminder - All]
    if query_result.get('action') == 'showReminder.All':
      return {
            "fulfillmentText": testcheck("",""),
            "displayText": '50',
            "source": "webhookdata"
      }

# Intent: [showReminder - date]
    if query_result.get('action') == 'showReminder.Date':
      datefromdialog =  query_result['parameters']['showreminderdate'][0]
      resultcheck = query_result['outputContexts'][checkJsonToday(query_result)]['parameters']['showreminderdate.original']
      if resultcheck == "วันนี้":
        todaydate = datetime.now()
        enddaydate = datetime.combine(todaydate, datetime.min.time()) + timedelta(1)
        startdateformat = str(todaydate).split(" ")[0]+"T"+str(todaydate).split(" ")[1].split(".")[0]+"+07:00"
        newcheck = str(enddaydate).split(" ")[0]+"T"+str(enddaydate).split(" ")[1]+"+07:00"
        return {
        "fulfillmentText": testcheck(todaydate,newcheck),
        "displayText": '50',
        "source": "webhookdata"
      }
      else:
        StringToDate = datetime.fromisoformat(datefromdialog)

        datefromdialogStart = datetime.combine(StringToDate, datetime.min.time())
        enddaydate = datetime.combine(datefromdialogStart, datetime.min.time()) + timedelta(1)
        startdateformat = str(datefromdialogStart).split(" ")[0]+"T"+str(datefromdialogStart).split(" ")[1]+"+07:00"
        enddaydateformat = str(enddaydate).split(" ")[0]+"T"+str(enddaydate).split(" ")[1]+"+07:00"
        return {
          "fulfillmentText": testcheck(startdateformat,enddaydateformat),
          "displayText": '50',
          "source": "webhookdata"
        }

# Intent: [ShowActivity] ShowActivity - date
    if query_result.get('action') == 'ShowActivity.date' :
      RefFromDatabase = db.reference("/ActivityReminder") 
      datefromdialog = str(query_result["parameters"]["date-time"])
      datenew = str(datefromdialog).split("T")[0]
      get = RefFromDatabase.get()
      textresponse = '' 
      try:
        get.keys()
      except:
        fullfillmentText = 'ไม่มีกิจกรรมที่คุณบันทึกเจ้าค่ะ'
      else:
        for x in get.keys():
          if get[x]["date"] == datenew :
            textresponse +='<s><break time="200ms"/> '+ str(get[x]["event"])  + '<break time="200ms"/> ตอนเวลา '+str(get[x]["time"])+'<say-as interpret-as="date" format="yyyymmdd" detail="1">'+datenew+ '</say-as> <break time="300ms"/> </s>'+" "     
            fullfillmentText = '<speak><p>กิจกรรมของคุณคือ'+ textresponse+'เจ้าค่ะ</p></speak>'
            
    if query_result.get('action') == 'showHistory':
      try:
        ref1 = db.reference("/ShowHistory").get()
        a='<s>คุณใช้คำสั่งจดจำสิ่งของ  <break time="300ms"/> <say-as interpret-as="cardinal">'+str(ref1["remember"]["remember"])+'<break time="300ms"/></say-as> ครั้ง </s>'
        b='<s>คุณใช้คำสั่งเตือนความจำ <break time="300ms"/><say-as interpret-as="cardinal">'+str(ref1["reminder"]["reminder"])+'<break time="300ms"/></say-as> ครั้ง </s>'
        c='<s>คุณใช้คำสั่งบันทึกกิจกรรม <break time="300ms"/><say-as interpret-as="cardinal">'+str(ref1["activity"]["activity"])+'<break time="300ms"/></say-as> ครั้ง </s>'
        fullfillmentText = '<speak>'+a+b+c+'</speak>'
      except:
        fullfillmentText = 'ยังไม่มีประวัติการใช้งานเลยเจ้าค่ะ'
  
# No Intent  
    if fullfillmentText == "":
      fullfillmentText = 'ขออภัยดิฉันไม่เข้าใจคำสั่งเจ้าค่ะ'  
    return {
            "fulfillmentText": fullfillmentText,
            "displayText": '50',
            "source": "webhookdata"
      }  
# ------------------------------------------------------------------------------------# 

