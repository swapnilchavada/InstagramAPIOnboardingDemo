from app import app
from flask import make_response, request

import json
import requests

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
PAGE_ACCESS_TOKEN = 'EAAkHglUjoaIBAN7iJZCGPqjODTGgb3IigegtImZC569IpUdVwhIzfDMZCsIUXzHd7WCXHERbZAtnutgHQWcY9s6tOsNUk1R4ZBtvhDSZAecZCHzrQEH8WTAOeOsYsVkxxEpOSllGZAwu7mQYJOiZARkTxFXK0ARkhcTQi6duaE9x5hAZDZD'
SEND_API_URL = 'https://graph.facebook.com/v5.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN

HEADERS = {'content-type': 'application/json'}
IG_ACC_TO_REPLY = '90010159460687'
      
      
def send_message(body):
  try:
    for entry in body['entry']:
      if(entry['id'] != IG_ACC_TO_REPLY):
        return
      for message in entry['messaging']:
        sender = message['sender']['id']
        recipient_id =  message['recipient']['id']
        if 'message' in message: 
          webhook_type='message'
        elif 'postback' in message: 
          webhook_type='postback'
        else:
          return
        if 'text' in message[webhook_type]:
          msg_text = message[webhook_type]['text']
          if 'echoing_back' in msg_text:
            return
          elif 'qr' in msg_text:
            send_message_with_qr_to_recipient(sender, recipient_id)
            return
        body['echoing_back'] = 'true'
        if 'is_echo' in message[webhook_type]:
          send_message_to_recipient(json.dumps(body), recipient_id, sender)
          print('sent message to', recipient_id)
        else:
          send_message_to_recipient(json.dumps(body), sender, recipient_id)
          print('sent message to', sender)
  except Exception as e:
     print("swapnilc-Exception sending")
     print(e)
      
def send_message_with_qr_to_recipient(recipient_id, page_id):
  message = {
    'recipient': {
      'id': recipient_id,
    },
    'message': {
    "text": "Pick a color echoing_back :",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Red",
        "payload":"red-payload",
      },
      {
        "content_type":"text",
        "title":"Green",
        "payload":"green-payload",
     },
     {
        "content_type":"text",
        "title":"Purple",
        "payload":"purple-payload",
     },
     {
        "content_type":"text",
        "title":"Yellow",
        "payload":"yellow-payload",
     },
      {
        "content_type":"text",
        "title":"Blue",
        "payload":"blue-payload",
     },
     {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"red-payload",
      },
      {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"green-payload",
     },
     {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"green-payload",
     },
      {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"yellow-payload",
     },
      {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"blue-payload",
     },
     {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"red-payload",
      },
      {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"green-payload",
     },
     {
        "content_type":"text",
        "title":"Max 20 chars-Long Long Text for QR Testing",
        "payload":"green-payload",
     }
    ]
  },
    'tag': 'human_agent',
  }
  r = requests.post(SEND_API_URL, data=json.dumps(message), headers=HEADERS)
  if r.status_code != 200:
    print('== ERROR====')
    print(SEND_API_URL)
    print(r.json())
    print('==============')

    
def send_message_to_recipient(message_text, recipient_id, page_id):
  message = {
    'recipient': {
      'id': recipient_id,
    },
    'message': {
      'text': message_text,
    },
    'tag': 'human_agent',
  }
  r = requests.post(SEND_API_URL, data=json.dumps(message), headers=HEADERS)
  if r.status_code != 200:
    print('== ERROR====')
    print(SEND_API_URL)
    print(r.json())
    print('==============')


@app.route('/')
@app.route('/index')
def index():
  print("index")
  return 'Hello, World!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'GET':
    mode = request.args['hub.mode']
    token = request.args['hub.verify_token']
    challenge = request.args['hub.challenge']
    if mode and token:
      if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        return challenge
      else:
        return make_response('wrong token', 403)
    else:
      return make_response('invalid params', 400)
  else: # POST
    body = json.loads(request.data)
    print("swapnilc-Mydata")
    print(body)
    send_message(body)
    return ("", 205)

