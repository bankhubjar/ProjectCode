from flask import Blueprint
from flask import Flask, render_template
from flask import Flask,request
from firebase import firebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
  return ref.get()
  
    
  
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
    
@appBlueprint.route('/webhook', methods=['POST'])
def rejectOrder():
    req = request.get_json(silent=True, force=True)
    fullfillmentText = ''
    query_result = req.get('queryResult')
    if query_result.get('action') == 'order.typeFood':
        orders = query_result.get('parameters')[0][0]
        fullfillmentText = orders
        # fullfillmentText = "Message form python: เข้าใจแล้ว"
        return {
            "fulfillmentText": fullfillmentText,
            "displayText": '25',
            "source": "webhookdata"
        }  
