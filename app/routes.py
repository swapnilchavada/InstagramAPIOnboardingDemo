from app import app
from flask import make_response, request

import json
import requests

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
PAGE_ACCESS_TOKEN = 'EAAkHglUjoaIBAH2wmaM8BRwdJjXmJmtyuLOI9OEpByxGQWSLXXq8ZCmSmtjheoQZAPEXktZCzRFiYNEdUpwViPZChnamTjhguYZB48ktQkJ2jgUcMNIWOnQZCIfNiLL6BQN4r6WKeVt3x8U48pmaKQvZCiZC9zQmUFVbZBBkO3dyeLgZCBN1ZCaDoKWxy8e0Fc0LowZD'
SEND_API_URL = 'https://graph.facebook.com/v4.0/me/messages?access_token=%s'\
  %PAGE_ACCESS_TOKEN

HEADERS = {'content-type': 'application/json'}
IG_ACC_TO_REPLY = 90010159460687

def send_message(body):
  try:
    #send_message_to_recipient(json.dumps(body), sender, recipient_id)
    print('sender')
    #print(sender)
  except Exception as e:
     print("swapnilc-Exception sending")
     print(e)
      
      
def send_message(body):
  print('send_message')
  print(body)
  try:
    for entry in body['entry']:
      if(entry['id'] !== IG_ACC_TO_REPLY):
        return
      for message in entry['messaging']:
          sender = message['sender']['id']
          recipient_id =  message['recipient']['id']
          if 'message' in message: 
            webhook_type='message'
          else:
            return
          if 'text' in message[webhook_type]:
            msg_text = message[webhook_type]['text']
            if 'echoing_back' in msg_text:
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
      
      
def send_message_to_recipient(message_text, recipient_id, page_id):
  message = {
    'recipient': {
      'id': recipient_id,
    },
    'message': {
      'text': message_text,
    },
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

