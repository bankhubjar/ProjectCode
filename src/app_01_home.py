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

@appBlueprint.route("/")
def home():
     d = '<form action="next">'
     f =  '<p>Field1 <input type = "text" name = "name" /></p>'
     o = '<p><input type = "submit" value = "submit" /></p> </form>'
     z = d+f+o
     return z

  
    
@appBlueprint.route("/next")
def next():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "test.json")
    data = json.load(open(json_url, encoding="utf8"))
    ref2 = db.reference("/Remember2")
    eiei = data['queryResult']
    NameU = eiei['outputContexts'][2]["parameters"]['name']
    Item = eiei['outputContexts'][2]["parameters"]['objname']
    Place = eiei['outputContexts'][2]["parameters"]['place']
    users_r29 = ref2.child(NameU)
    users_r29.set({
        Item: Place
        
     })  
    # nameF = "/"+request.form['name']
    # ref1 = db.reference("/Remember")
    # data = ref1.get()
  #sdasdasdasdsa
    return "kuy"
  # def getDB():
  #   return ref.get()
#   users_ref = ref.child('something')
# users_ref.set({
#     'alanisawesome': {
#         'date_of_birth': 'June 23, 1912',
#         'full_name': 'Alan Turing'
#     },
#     'gracehop': {
#         'date_of_birth': 'December 9, 1906',
#         'full_name': 'Grace Hopper'
#     }
#})
  # result = firebase.get('/restaurants', None)
  # s = ""
  # for x  in result:
  #   s += x["name"]
  #   s += x["address"]
  #   s += ", <br>"

  # return str(s)


@appBlueprint.route("/getDB")
def getDBE():
  RefG = db.reference('/RememberV2/Home')
  count = 0
  Deta = RefG.get()
  eiei = ""
  for key in Deta.keys(): eiei += key
  # while 
  # Data = Deta["Home"]["รายการที่"+ str(count)]
  

  return eiei


@appBlueprint.route("/test")
def submit():
    
  users_r = ref.child('something')
  users_r.set({
        'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
    })
  return "helloeiei"

@appBlueprint.route("/test1")
def submiteiei():
  ref2 = db.reference("/Remember")  
  users_r = ref2.child('EiEi')
  users_r.set({
        'หนังสือ': {
        'สถานที่': 'หลังบ้าน'
    }})
  return "helloeiei"
# @appBlueprint.route('/submit', methods=['GET', 'POST'])
# def submit():

@appBlueprint.route("/HomeUser")    
def HomeUser():
       SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
       json_url = os.path.join(SITE_ROOT, "", "new.json")
       data2 = json.load(open(json_url, encoding="utf8"))
       data = data2['queryResult']
       Place = data['outputContexts'][1]["parameters"]["place"]
       objname = data['outputContexts'][1]["parameters"]["objname"] 
       RefNo1 = db.reference("/RememberV2/Home") 
       count = 0
       Deta = RefNo1.get()
       
       d2 = "EiEi"
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
          return "ควย"
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
         return "ควย" 
#     name = "Newworld"
#     address = "NewworldEiEi"
#     new_data = {"name": name, "address": address}
#     firebase.post("/restaurants", new_data)
#     return "Thank you!"

@appBlueprint.route("/nospecifyname")
def intentshowAllrequestno():
  ref2 = db.reference("/RememberV2/Home")  
  test = ref2.get()
  fulfillmentText = ''
  for x in test.keys():
    fulfillmentText +=' คุณบันทึกสิ่งของ : '+str(test[x]["item"])+ ' ไว้ตำแหน่ง ' + str(test[x]["Location"]) + "  " 
  return fulfillmentText

@appBlueprint.route("/specifyitem")
def intentshowAllrequestyesspecifyname():
  ref2 = db.reference("/RememberV2/Home")  
  test = ref2.get()
  fulfillmentText = ''
  for x in test.keys():
    if(test[x]["item"] == "ควย"):
      fulfillmentText +=' คุณได้บันทึก : '+str(test[x]["item"])+ " ไว้" 
  return fulfillmentText

@appBlueprint.route("/specifyLocation")
def intentshowAllrequestyesspecifyLocation():
  ref2 = db.reference("/RememberV2/Home")  
  test = ref2.get()
  fulfillmentText = ''
  for x in test.keys():

    if(test[x]["Location"] == "ในใจ"):
      fulfillmentText +=' คุณบันทึกสิ่งของไว้พี่ ' + str(test[x]["Location"]) + "  " 
  return fulfillmentText

# @appBlueprint.route('/webhook', methods=['POST'])
# def webhook():
#   req = request.get_json(silent=True, force=True)
#   fulfillmentText = ''
#   sum = 0
#   query_result = req.get('queryResult')
#   if query_result.get('action') == 'add.numbers':
#     num1 = int(query_result.get('parameters').get('number'))
#     num2 = int(query_result.get('parameters').get('number1'))
#     sum = str(num1 + num2)
#     print('here num1 = {0}'.format(num1))
#     print('here num2 = {0}'.format(num2))
#     fulfillmentText = 'The sum of the two numbers is '+sum
#   elif query_result.get('action') == 'multiply.numbers':
#     num1 = int(query_result.get('parameters').get('number'))
#     num2 = int(query_result.get('parameters').get('number1'))
#     product = str(num1 * num2)
#     print('here num1 = {0}'.format(num1))
#     print('here num2 = {0}'.format(num2))
#     fulfillmentText = 'The product of the two numbers is '+product
#   return {
#         "fulfillmentText": fulfillmentText,
#         "displayText": '25',
#         "source": "webhookdata"
#     }
    
@appBlueprint.route('/webhook',methods=['POST'])
def rejectOrder():
    ref2 = db.reference("/Remember")  
    FDB = ref2.get()
    req = request.get_json(silent=True, force=True)
    fullfillmentText = ''
    now = datetime.now()
    query_result = req.get('queryResult')
    d2 = now.strftime("%d/%m/%Y %H:%M:%S")
    if query_result.get('action') == 'object.confirm':
        NameU = query_result['outputContexts'][4]["parameters"]['name']
        Item = query_result['outputContexts'][4]["parameters"]['objname']
        Place = query_result['outputContexts'][4]["parameters"]['place']        
        users_r29 = ref2.child(NameU)
        users_r29.set({
          "ชื่อ":NameU,
          Item: Place
        })  
        fullfillmentText = 'From Python คุณ'+ NameU+ 'บันทึกสิ่งของ : '+Item+ ' ไว้ตำแหน่ง ' + Place
    if query_result.get('action') == 'object.remember':
        NameU = query_result['outputContexts'][3]["parameters"]['name']
        Item = query_result['outputContexts'][3]["parameters"]['objname']
        Place = query_result['outputContexts'][3]["parameters"]['place']
        Item2 = FDB[NameU]
        fullfillmentText = 'From Python คุณ'+ str(Item2.keys()[0]) + 'บันทึกสิ่งของ : '+str(Item2.keys()[0])+ ' ไว้ตำแหน่ง ' + str(FDB[NameU][Item]) 
        # fullfillmentText = "Message form python: เข้าใจแล้ว"
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
            "fulfillmentText": "NoHave",
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
            "fulfillmentText": "Have1",
            "displayText": '25',
            "source": "webhookdata"
    }
    if query_result.get('action') == 'object.confirm.withUsername':
       NameUser = query_result['outputContexts'][4]["parameters"]["uname"]
       Place = query_result['outputContexts'][4]["parameters"]["place"]
       objname = query_result['outputContexts'][4]["parameters"]["objname"] 
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
            "fulfillmentText": "NoHave",
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
            "fulfillmentText": "Have1",
            "displayText": '25',
            "source": "webhookdata"
    }
    if query_result.get('action') == 'showAll..specifyname':
      for x in FDB.keys():
        fulfillmentText +=' คุณบันทึกสิ่งของ : '+str(test[x]["item"])+ ' ไว้ตำแหน่ง ' + str(test[x]["Location"]) + "  "      
    return {
            "fulfillmentText": fullfillmentText,
            "displayText": '25',
            "source": "webhookdata"
    }  



