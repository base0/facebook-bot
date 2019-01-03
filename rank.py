
# coding: utf-8

# In[1]:


base = 'http://www.person.ku.ac.th/person_nap/'
file = 'report4.php'
url = base + file

from urllib.request import urlopen
html = urlopen(url)

from bs4 import BeautifulSoup
soup = BeautifulSoup(html.read(), 'html.parser')


# In[2]:


def status(url):
    result = {}
    html = urlopen(url)

    soup = BeautifulSoup(html.read(), 'html.parser')
    a = soup.find_all('tr')

    for i in a:
        try:
            b = i.find_all('td')
            name = b[1]
            status = b[3]
            if status.text.strip() != 'ออกคำสั่งแล้ว':
                result[name.text.strip()] = status.text.strip()
        except:
            pass
    return result


# In[3]:


import urllib


web_data = {}
for i in soup.find_all('a')[5:]:
    web_data.update(status(base + urllib.parse.quote(i['href'], safe='?=&')))
web_data


# In[4]:


import csv

def read_csv():
    data = {}
    with open('status.csv', mode='r', newline='', encoding='utf8') as status_file:
        status_csv = csv.reader(status_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        next(status_csv)
        for row in status_csv:
            data[row[0]] = row[1]

    return data

file_data = read_csv()


# In[5]:


changed = False

message = []
for k, v in web_data.items():
    try:
        if web_data[k] != file_data[k]:
            message.append((k, web_data[k]))
            changed = True
    except:
        pass

approved = []
for k in file_data:
    if k not in web_data:
        approved.append(k)




# In[6]:


for k in web_data:
    if k not in file_data:
        message.append((k, web_data[k]))
        changed = True


# In[7]:


import csv

def write_csv(data):
    with open('status.csv', mode='w', newline='', encoding='utf8') as status_file:
        status_csv = csv.writer(status_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        status_csv.writerow(['name', 'status'])
        for k, v in data.items():
            status_csv.writerow([k, v])



# In[8]:


message


# In[9]:


from shutil import copyfile
import datetime

if changed:
    copyfile('status.csv', 'status-{}.csv'.format(str(datetime.datetime.now()).split(' ')[0]))
    write_csv(web_data)


# In[10]:


def chat(uid, msg):
    host = 'https://graph.facebook.com/v2.6/me/'
    path = 'messages/'
    d = {
	  'access_token' : 'DQVJ0LWw4bDdVTVJ3RWN6MGNYRDRicmRiX1B0Y3A2T0NXbDZAUcUhvYkJ3RXhlUTM0c3VYYmxnNk93LW1xVkxKS1JqWHItWWdlRkJ0Qm15aWRiQ1REZAjhoNGtELTlpbm1uRVNiWC11SUFjU2NXRDFfZAVRoUkxxejhmMGNSS2R4b2ZAyRm10QVdGS0I0U2tXZAFRvTmhsMmJLNjNrSjFhVUJObEJrQWMzRWpVcGh1NUFMVTg0dDZAmaHFFOFZAGQ0h5bndzRUhzclFB',
      "messaging_type": "UPDATE",
      "recipient": {
        "id": uid
      },
      "message": {
        "text": msg
      }
    }
    url = host + path

    from urllib import request, parse
    data = parse.urlencode(d).encode()
    req =  request.Request(url, data=data) # this will make the method "POST"
    resp = request.urlopen(req)


# In[11]:

if len(message) == 0 and len(approved) == 0:
    chat('100013848789026', 'no update')

for m in approved:
    chat('100013848789026', 'ยินดีด้วยครับ ' + m)

for m in message:
    chat('100013848789026', ' '.join(m))
