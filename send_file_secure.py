'''
!pip install msgpack
!pip install requests
'''

import requests

ACCESS_TOKEN = ''

def send_file(uid, file, typ='image', sub_typ='image/png'): # t can be image, file
    url = 'https://graph.facebook.com/v2.6/me/messages'
    payload = {
            'access_token' : ACCESS_TOKEN,
            'messaging_type' : "UPDATE",
            'recipient' : '{"id":"%s"}' % uid,
            'message' : '{"attachment":{"type":"%s", "payload":{"is_reusable":true}}}' % typ,
    }
    files = {'filedata': (file, open(file, 'rb'), sub_typ)}
    r = requests.post(url, files=files, data=payload)
    print(r.status_code)
    print(r.text)
    

#send_file('100015355776911', 'model.png')
send_file('100015355776911', 'm.pdf', 'file', 'application/pdf')