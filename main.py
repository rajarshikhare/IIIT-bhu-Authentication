from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import re

url_site = 'http://intranet.iiit-bh.ac.in'

#print("Opening Site....")
s = requests.Session()

credentials = []

print("Logging out for new Session")

try:
    s.request('GET', 'http://172.16.1.11:1000/logout?0a050d02040b002a', timeout=5)
except:
    time.sleep(5)


session_url = ''
while True:
    for cred in credentials:
        
        try:
        	site = urlopen(url_site)
        except:
        	print("No internet... Trying again")
        	time.sleep(3)
        	continue

        soup = BeautifulSoup(site, 'html.parser')

        if soup.title.string != 'Firewall Authentication':
            print("Already logged in...")
            print("Maintaining Session")
            if session_url :
                while True:
                    time.sleep(5)
                    try:
                        s.request('GET', session_url, timeout=5)
                    except:
                        print("Authentication gone!! restarting process")
                        time.sleep(5)
                        break;
            else:
                exit()

        print('Attemtping to login with ', cred[0])
        form = soup.find('form')
        fields = form.findAll('input')
        formdata = dict( (field.get('name'), field.get('value')) for field in fields)
        formdata['username'] = cred[0]
        formdata['password'] = cred[1]

        #print("Logging in.....")
        post_url = url_site + form['action']
        try:
            r = s.post(post_url, data=formdata, timeout=5)
        except:
            print("Athentication not responding.. Trying another Authentication")
            time.sleep(6)
            continue
        response_soup = BeautifulSoup(r.content, 'html.parser')
        if response_soup.title.string == 'Firewall Authentication':
            print("Athentication Overlimt.. Trying another Authentication")
            continue
        else:
            print('Logged in as', cred[0])
            print("Maintaining Session")
            response_soup = BeautifulSoup(r.content, 'html.parser')
            script = response_soup.find('script')

            session_url = (re.findall('\"(.+?)\"', script.string))[0]
            while True:
                time.sleep(5)
                try:
                    s.request('GET', session_url, timeout=5)
                except:
                    print("Authentication gone!! restarting process")
                    time.sleep(5)
                    break;



print("Better luck next time")