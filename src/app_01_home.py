from flask import Blueprint
from flask import Flask,request
import json
appBlueprint = Blueprint("home",__name__)

@appBlueprint.route("/")
def index():
    return 'Hello, I am Flask Application ssss.'


@appBlueprint.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  fulfillmentText = ''
  sum = 0
  query_result = req.get('queryResult')
  if query_result.get('action') == 'add.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    sum = str(num1 + num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The sum of the two numbers is '+sum
  elif query_result.get('action') == 'multiply.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    product = str(num1 * num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The product of the two numbers is '+product
    elif query_result.get('action') == 'Listmenu':
       with open('food.json') as json_file:
        data = json.load(json_file)
        s = ""
        for p in data['eng_name']:
            s += ","+p
        fulfillmentText = 'list menu have  '+s
       return {
        "fulfillmentText": fulfillmentText,
        "displayText": '25',
        "source": "webhookdata"
    }




        
