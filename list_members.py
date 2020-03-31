host = 'https://graph.facebook.com/v2.12/'
path = '%s&access_token='
url = host + path

a = []

cmd = '774280952719501/members?fields=email'
result = requests.get(url % cmd).json()
a.extend(result['data'])
stop = False
while not stop:
  try:
    print(result['paging']['next'])
    result = requests.get(result['paging']['next']).json()
    a.extend(result['data'])
  except:
    stop = True

a
