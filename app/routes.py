from app import app
from flask import make_response, request

import json
import requests

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
PAGE_ACCESS_TOKEN = 'EAAeeVSYcYQYBAHng9dsVAiRdvy1kKttTvWFkcmoU2fwUr44vnJXVQJfXzuZCL8FAUM9IqZCqlZBgaWMbRw6JQ09xlF9s130Syzt1trfbZCC1jxbM4IHtPqxVXRg6DB11rsDheteFCtLuXHqJWTXqHkz4gMV7QZBRATgucFmF2ywZDZD'

SEND_API_URL = 'https://graph.facebook.com/v2.12/me/messages?access_token=%s'\
  % PAGE_ACCESS_TOKEN

PASS_THREAD_CONTROL_URL = 'https://graph.facebook.com/v2.12/me/pass_thread_control?access_token=%s'\
  % PAGE_ACCESS_TOKEN

TAKE_THREAD_CONTROL_URL = 'https://graph.facebook.com/v2.12/me/take_thread_control?access_token=%s'\
% PAGE_ACCESS_TOKEN

HEADERS = {'content-type': 'application/json'}

PAGE_INBOX = 263902037430900

ME = '620697518375534'

@app.route('/')
@app.route('/index')
@app.route('/webhook', methods=['GET', 'POST'])

def index():
  return 'Hello, World!'

def send_message(body):
  print('send_message')
  print(body)
  try:
    #send_message_to_recipient(json.dumps(body), sender)
    print('sender')
  except Exception as e:
     print("swapnilc-Exception sending")
     print(e)
     
def send_message_to_recipient(message_text, recipient_id):
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
    print('====ERROR====')
    print(r.json())
    print('==============')

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

