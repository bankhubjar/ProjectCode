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

appBlueprint = Blueprint("home",__name__)
    # data =''
    # with open("./src/message.json", errors='ignore') as read_file:
    #    data = json.load(read_file)
    # # query_result['parameters'][1]['showreminderdate']
    # return data["queryResult"]['parameters']['showreminderdate'][0]
@appBlueprint.route('/test2')
def testcheck2():
   todaydate = datetime.now()
   startdateformat = str(todaydate).split(" ")[0]+"T"+str(todaydate).split(" ")[1].split(".")[0]+"+07:00"
   return startdateformat

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
        datetime = data['outputContexts'][ides]["parameters"]["date"]
      except:
        kiki+=1
        ides+=1
      else:
        aany = data['outputContexts'][ides]["parameters"]["any"]
        dateime = data['outputContexts'][ides]["parameters"]["date"]
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
        kiki+=1
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

def checkJsonToday(data):
    kiki = 0
    ides = 0
    while ides < len(data['outputContexts']):
      try:
        datet = data['outputContexts'][ides]["parameters"]["showreminderdate.original"]
      except:
        kiki+= 1
        ides+=1
      else:
        datet = data['outputContexts'][ides]["parameters"]["showreminderdate.original"]
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
  newhistory = DBRef.child(service)
  try:
    data[service]
  except:
    newhistory.set({service : 1})
  else: 
    oldhistory = data
    newhistory.set({service : oldhistory[service]+1})

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
    service = checkService()
    result = service.calendarList().list().execute()
    calendar_id = result['items'][2]['id']
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
          savehistory("remember")
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
            savehistory("remember")
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
          savehistory("remember")
          return {
              "fulfillmentText": "บันทึกรายการเรียบร้อย",
              "displayText": '25',
              "source": "webhookdata"
       } 

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
      fulfillmentText = "คุณได้บันทึกกิจกรรมไว้ว่า "+event+" ที่เวลา "+time+" ในวันที่ "+date
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
        savehistory("reminder")
      return {
        "fulfillmentText": fulfillmentText,
        "displayText": '25',
        "source": "webhookdata"
      }
             
    if query_result.get('action') == 'showAll..specifyname':
      try:
        NameUserser = query_result['outputContexts'][checkJsonForItem(query_result,"")]["parameters"]["specifyname"]
        RefFromDatabase = db.reference("/RememberV2")
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
        for x in get.keys():
          fullfillmentText +=' คุณบันทึกสิ่งของ : '+str(get[x]["item"])+ ' ไว้ตำแหน่ง ' + str(get[x]["Location"]) + "  "
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'

    if query_result.get('action') == 'showSpecify.inform':
      try:
        NameUserser = query_result['outputContexts'][checkJsonForItem(query_result,"informname")]["parameters"]["informname"]
        item = query_result['outputContexts'][checkJsonForItem(query_result,"informname")]["parameters"]["specifyItemName"]
        RefFromDatabase = db.reference("/RememberV2") 
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
        item = query_result['outputContexts'][checkJsonForItem(query_result,"")]["parameters"]["specifyItemName"]
        RefFromDatabase = db.reference("/RememberV2/Home") 
        get = RefFromDatabase.get()
        for x in get.keys():
          if get[x]["item"] == item :
            fullfillmentText +=' คุณบันทึกสิ่งของไว้ที่ ' + str(get[x]["Location"]) + "  "
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'
  
    if query_result.get('action') == 'showReminder.All':
      return {
            "fulfillmentText": testcheck("",""),
            "displayText": '50',
            "source": "webhookdata"
      }

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
      fulfillmentText = "คุณได้บันทึกกิจกรรมไว้ว่า "+activityname+" ที่เวลา "+time+" ในวันที่ "+date
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
        savehistory("activity")
        return {
          "fulfillmentText": fulfillmentText,
          "displayText": '25',
          "source": "webhookdata"
        } 

    if query_result.get('action') == 'ShowActivity.date' :
      datefromdialog = query_result['outputContexts']["parameters"]["date-time"]

    if query_result.get('action') == 'showHistory':
      try:
        ref1 = db.reference("/ShowHistory").get()
        a='คุณใช้คำสั่งบันทึกของ '+str(ref1["Remember"])+' ครั้ง '
        b='คุณใช้คำสั่งเตือนความจำ '+str(ref1["reminder"])+' ครั้ง '
        c='คุณใช้คำสั่งบันทึกกิจกรรม '+str(ref1["activity"])+' ครั้ง'
        fullfillmentText = a+b+c
      except:
        fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'
  
    if fullfillmentText == "":
      fullfillmentText = 'ไม่พบสิ่งของที่คุณต้องการ'  
    return {
            "fulfillmentText": fullfillmentText,
            "displayText": '50',
            "source": "webhookdata"
      }  
    

