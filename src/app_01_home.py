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
    ref2 = db.reference("/Remember")
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

    
#     name = "Newworld"
#     address = "NewworldEiEi"
#     new_data = {"name": name, "address": address}
#     firebase.post("/restaurants", new_data)
#     return "Thank you!"





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
    query_result = req.get('queryResult')
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
    elif query_result.get('action') == 'object.remember':
        NameU = query_result['outputContexts'][3]["parameters"]['name']
        Item = query_result['outputContexts'][3]["parameters"]['objname']
        Place = query_result['outputContexts'][3]["parameters"]['place']
        Item2 = FDB[NameU]
        fullfillmentText = 'From Python คุณ'+ str(Item2.keys()[0]) + 'บันทึกสิ่งของ : '+str(Item2.keys()[0])+ ' ไว้ตำแหน่ง ' + str(FDB[NameU][Item]) 
        # fullfillmentText = "Message form python: เข้าใจแล้ว"
    return {
            "fulfillmentText": fullfillmentText,
            "displayText": '25',
            "source": "webhookdata"
    }  



