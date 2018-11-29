from urllib import request, parse

ACCESS_TOKEN = ''

def send_file(uid, url):
    host = 'https://graph.facebook.com/v2.6/me/'
    path = 'messages/'
    d = {
        'access_token' : ACCESS_TOKEN,
        'messaging_type' : "UPDATE",
        'recipient' : {
            'id' : uid
        },
        'message' : {
            'attachment' : {
                'type' : "file",
                'payload' : {
                    'url' : url,
                    'is_reusable' : 'true'
                }
            }
        }
    }

    url = host + path

    data = parse.urlencode(d).encode()
    req =  request.Request(url, data=data) 
    resp = request.urlopen(req)

send_file('100014056506071', 'http://pirun.ku.ac.th/%7efsciwss/temp/qa.pdf')