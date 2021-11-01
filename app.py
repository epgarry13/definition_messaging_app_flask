from flask import Flask, request, redirect, json, session, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
import datetime
import uuid
import requests


app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection('users')
request_ref = db.collection('request')

# Dictionary API base URL
base_url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


@app.route("/", methods=['GET', 'POST'])
def sms_reply():



    resp = MessagingResponse() 
    
    # Text message from user
    phone_number = request.values.get('From')
    word = request.values.get('Body').lower()

    # Add request to DB
    store_request(phone_number, word)

    # Get word data
    word_dict = get_word_dict(word)

    # Make text response
    response = make_sms_response(word_dict)
    resp.message(response)

    return str(resp)


@app.route('/word/<word>', methods=['GET'])
def word(word):
    word_dict = get_word_dict(word)
    return jsonify(word_dict)


@app.route('/sms-response/<word>', methods=['GET'])
def sms_response(word):
    word_dict = get_word_dict(word)
    response = make_sms_response(word_dict)
    return response


@app.route("/api/dashboard", methods=['GET'])
def dashboard():
    pass


def get_word_dict(word):
    data = requests.get(base_url + word)
    return data.json()[0]


# Will be used make a string of whatever we want to text.


def make_sms_response(word_dict):

    word = word_dict['word']
    word_definition = word_dict['meanings'][0]['definitions'][0]

    definition = word_definition['definition']
    example = word_definition['example']

    response = """
    %s
    Definition: %s
    Example: %s
    """ % (word, definition, example)

    return response


def store_request(phone_number, word):
    request = {}
    doc_id = uuid.uuid1()
    request['id'] = str(doc_id)
    request['phone_number'] = phone_number
    request['word'] = word
    request['timestamp'] = datetime.datetime.now()
    request_ref.document(str(doc_id)).set(request)
