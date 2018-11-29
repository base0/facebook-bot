
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request as frequest
from urllib import request as urequest
from urllib import parse

VERIFY_TOKEN = ''
ACCESS_TOKEN = ''

app = Flask(__name__)

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
    print(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']
                    message_text = messaging_event['message']['text']
                    chat(sender_id, message_text)
    return 'ok'

