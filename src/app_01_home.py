from flask import Blueprint
from flask import Flask,request
appBlueprint = Blueprint("home",__name__)

@appBlueprint.route("/")
def index():
    return 'Hello, I am Flask Application ssss.'


@appBlueprint.route('/webhook',methods=['POST'])
 query_result = req.get('queryResult')
  num1 = int(query_result.get('parameters').get('number'))
  num2 = int(query_result.get('parameters').get('number1'))
  sum = str(num1 + num2)
  print('here num1 = {0}'.format(num1))
  print('here num2 = {0}'.format(num2))
  return {
        "fulfillmentText": 'The sum of the two numbers is: '+sum,
        "displayText": '25',
        "source": "webhookdata"
    }
