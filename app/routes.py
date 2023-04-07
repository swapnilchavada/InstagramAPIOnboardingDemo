from app import app
from flask import make_response, request, render_template, url_for

import json
import requests
import os

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
HEADERS = {'content-type': 'application/json'}
IG_ACC_TO_REPLY = '17841453418980195'

@app.route('/')
@app.route('/index')
def index():
  print("index")
  return "<h1>Welcome to Geeks for Geeks</h1>"

  # app_id = app.config.get('APP_ID')
  # redirect_uri = app.config.get('REDIRECT_URL')

  # url = 'https://www.facebook.com/dialog/oauth?client_id={}&response_type=code&display=page&redirect_uri={}&scope=instagram_manage_messages%2Cinstagram_basic%2Cpages_manage_metadata&extras=%7B%22setup%22%3A%7B%22channel%22%3A%22IG_API_ONBOARDING%22%7D%7D"'.format(app_id, redirect_uri)
  # print('print', url)
  # return render_template('fb-login.html', fb_login_link =url )

@app.route('/login_success')
def login_success():
  code = request.args.get('code')
  app_id = app.config.get('APP_ID')
  app_secret = app.config.get('APP_SECRET')
  redirect_uri = app.config.get('REDIRECT_URL')
  base_graph_api_url = app.config.get('BASE_GRAPH_API_URL')

  print('print', base_graph_api_url)

  # get user access token from code
  access_token_url = '{}oauth/access_token?client_id={}&redirect_uri={}&client_secret={}&code={}'.format(base_graph_api_url, app_id, redirect_uri, app_secret, code)
  access_token_response = requests.get(access_token_url)
  access_token_response = access_token_response.json()
  print("access_token_response", access_token_response)
  access_token =  access_token_response['access_token']

  print("access_token", access_token)

  # Get page access token
  accounts_url = '{}me/accounts?access_token={}&fields=connected_instagram_account,access_token'.format(base_graph_api_url, access_token)
  print("11", accounts_url)
  accounts_url_response = requests.get(accounts_url)
  accounts_url_response = accounts_url_response.json()
  # Assuming the first account here. In practise if there are many accounts here, you might want to show
  # a drop down to the user to get input on which account they are interested to connect with
  page_access_token = accounts_url_response['data'][0]['access_token']
  print("page_access_token", page_access_token)

  #convert to long live access token
  long_live_access_token_url = '{}oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'.format(base_graph_api_url, app_id, app_secret, page_access_token)
  long_live_access_token_response = requests.get(long_live_access_token_url)
  long_live_access_token_response = long_live_access_token_response.json()
  print("long_live_access_token_response", long_live_access_token_response)
  page_access_token = long_live_access_token_response['access_token']
  # Might want to save this access tokn at this point in Database

  # call conversations api, just to demo this works
  conversations_api_url = '{}me/conversations?fields=participants&platform=instagram&access_token={}'.format(base_graph_api_url, page_access_token)
  print("conversations_api_url", conversations_api_url)
  conversations_api_url_response = requests.get(conversations_api_url)
  conversations_api_url_response = conversations_api_url_response.json()
  data = conversations_api_url_response['data']
  print('conversations_api_url_response', data)
  return render_template('conversations_api.html', tableData =data )

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
    print("body", body)
    send_message(body)
    return ("", 205)


def send_message(body):
  try:
    for entry in body['entry']:
      if(entry['id'] != IG_ACC_TO_REPLY):
        return
      if 'standby' in entry:
        channel='standby'
      else:
        channel='messaging'
      for message in entry[channel]:
        sender = message['sender']['id']
        recipient_id =  message['recipient']['id']
        if 'message' in message:
          webhook_type='message'
        elif 'postback' in message:
          webhook_type='postback'
        else:
          return
        if 'is_echo' in message[webhook_type]:
          return
        if 'text' in message[webhook_type]:
          msg_text = message[webhook_type]['text']
          if 'BOT SAYS: ' in msg_text:
            return
          if 'echo_back' not in msg_text:
            #ignore if no_reply in message
            return
          msg_text = 'BOT SAYS: ' + msg_text
        body['echoing_back'] = 'true'
        send_message_to_recipient(json.dumps(body), sender, recipient_id)
        print('sent message to', sender)
  except Exception as e:
     print("Exception sending", e)

def send_message_to_recipient(message_text, recipient_id, page_id):
  try:
    page_access_token = os.environ['ACCESS_TOKEN_SECRET_IGM_API']
  except KeyError:
      print('Please define the environment variable ACCESS_TOKEN_SECRET_IGM_API')
      return
  message = {
    'recipient': {
      'id': recipient_id,
    },
    'message': {
      'text': message_text,
    },
    'tag': 'human_agent',
  }

  base_graph_api_url = app.config.get('BASE_GRAPH_API_URL')
  send_api_url = '{}me/messages?access_token={}'.format(base_graph_api_url, page_access_token)
  r = requests.post(SEND_API_URL, data=json.dumps(message), headers=HEADERS)
  print("Send api response", r.json())


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')
