import string

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from collections import OrderedDict

BASE_URL = "http://www.facebook.com"
MOBILE_URL = "http://m.facebook.com"
SAVE_FILE = "fb_info.txt"
TOP_FRIENDS = 20

browser = webdriver.Firefox()

def login(url=BASE_URL):
    """ Login to Facebook """
    global browser
    browser.get(url)
    
    browser.find_element_by_id('email').clear()
    browser.find_element_by_id('email').send_keys("<YOUR EMAIL>")
    
    browser.find_element_by_id('pass').clear()
    browser.find_element_by_id('pass').send_keys("<YOUR PASSWORD>")
    browser.find_element_by_id('pass').submit()

login()

dom = str(browser.page_source.encode('utf-8'))

i = dom.index(',list:')
if i < 0:
    raise Exception("Can't find chat data!")

line = dom[i+6:]
line = line[:line.index(']')+1]



id_list = line.replace('","', ' ').replace('"', '').replace('-0', '').replace('-2', '').split()[:TOP_FRIENDS]
place_holder = ['(unnamed)' for x in range(len(id_list))]
id_dict = OrderedDict(zip(id_list, place_holder))

for k, v in id_dict.items():
    browser.get(BASE_URL+'/'+k)
    try:
        friend = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.ID, 'fb-timeline-cover-name'))
        )
    except:
        continue
    
    id_dict[k] = ''.join(filter(lambda x: x in string.printable, friend.text))#.encode('utf-8').decode('utf-8')
    print(id_dict[k])

print(id_dict)

with open(SAVE_FILE, 'w') as f:
    for i, name in enumerate(id_dict.values()):
        weight = TOP_FRIENDS-i
        if weight < 0:
            weight = 0
            
        friend_name = str(name)+', '+str(weight)+'\n'
        f.write(friend_name)
