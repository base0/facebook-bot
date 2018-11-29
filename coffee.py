
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request as frequest
from urllib import request as urequest
from urllib import parse

VERIFY_TOKEN = ''
ACCESS_TOKEN = ''

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/webhook', methods=['GET'])
def handle_verification():
    if (frequest.args.get('hub.verify_token', '') == VERIFY_TOKEN):
        print('Verified')
        return frequest.args.get('hub.challenge', '')
    else:
        print('Wrong token')
        return 'Error, wrong validation token'

@app.route('/webhook', methods=['POST'])
def handle_message():
    data = frequest.get_json()

    print(order)
    if data['object'] == 'page':
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']
        if 'quick_reply' in message:
            get_quick_reply(sender, message)
        else:
            get_plaintext(sender, message)

    return 'ok'

def chat(uid, msg):
    host = 'https://graph.facebook.com/v2.6/me/'
    path = 'messages/'
    d = {
	  'access_token' : ACCESS_TOKEN,
      "messaging_type": "UPDATE",
      "recipient": {
        "id": uid
      },
      "message": {
        "text": msg
      }
    }
    url = host + path

    data = parse.urlencode(d).encode()
    req =  urequest.Request(url, data=data) # this will make the method "POST"
    resp = urequest.urlopen(req)

def qchat(uid, text, menu):
    host = 'https://graph.facebook.com/v2.6/me/'
    path = 'messages/'
    d = {
	  'access_token' : ACCESS_TOKEN,
      "messaging_type": "UPDATE",
      "recipient": {
        "id": uid
      },
      "message": {
        "text": text,
        "quick_replies": [ {"content_type": "text", "title" : i, "payload" : text + "_" + i} for i in menu]
      }
    }
    url = host + path

    data = parse.urlencode(d).encode()
    req =  urequest.Request(url, data=data) # this will make the method "POST"
    resp = urequest.urlopen(req)

order = {}

def get_quick_reply(sender, message):
    payload = message['quick_reply']['payload']
    if payload.startswith('coffee'):
        order[sender] = payload.split('_')[1]
        qchat(sender, 'sweet', ['หวาน', 'หวานมาก'])
    elif payload.startswith('sweet'):
        order[sender] = order[sender] + ' ' + payload.split('_')[1]
        chat(sender, 'คุณสั่ง ' + order[sender] + ' ขอบคุณค่ะ')
        del(order[sender])

def get_plaintext(sender, message):
    global order
    text = message['text']
    if text == 'coffee':
        qchat(sender, text, ['Latte', 'Capu', 'Mocha'])

