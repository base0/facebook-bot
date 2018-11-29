import requests

ACCESS_TOKEN = ''

def f(uid, text):
    url = 'https://graph.facebook.com/v2.6/me/messages'
    payload = {
            'access_token' : ACCESS_TOKEN,
            'messaging_type' : 'UPDATE',
            'type' : 'image',
            'recipient' : {
                'id' : uid
            },
            'message': {
                'text': text
            }
        }
    r = requests.post(url, json=payload)
    print(r.status_code)
    print(r.text)
    

f('100015311', 'สวัสดี')