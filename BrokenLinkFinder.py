import requests, threading
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print('   ****************************')
print('   *    BROKEN LINK FINDER    *')
print('   ****************************')

baseUrl = 'https://www.google.com/'

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.get(baseUrl)
driver.implicitly_wait(10)
links = driver.find_elements(By.TAG_NAME,'a')
print('\n')
print('   ----------------------')
print('   |  Finding Links...  |')
print('   ----------------------')
print('\n')
urls = []
for link in links:
    ref = link.get_attribute('href')
    if ref == None:
        pass
    else:
        it = ''
        for item in ref[0:4]:
            it = it+item
        if it == 'http':
            urls.append(ref)
len_url = len(urls)

status_code = {'400':'Bad Request','401':'Unauthorized','402':'Payment Required','403':'Forbidden','404':'Not Found','405':'Method Not Allowed','406':'Not Acceptable','407':'Proxy Authentication Required','408':'Request Timeout','409':'Conflict','410':'Gone','411':'Length Required','412':'Precondition Failed','413':'Payload Too Large','414':'URI Too Long','415':'Unsupported Media Type','416':'Range Not Satisfiable','417':'Expectation Failed','418':'I am a teapot','421':'Misdirected Request','422':'Unprocessable Entity (WebDAV)','423':'Locked (WebDAV)','424':'Failed Dependency (WebDAV)','425':'Too Early','426':'Upgrade Required','428':'Precondition Required','429':'Too Many Requests','431':'Request Header Fields Too Large','451':'Unavailable For Legal Reasons','500':'Internal Server Error','501':'Not Implemented','502':'Bad Gateway','503':'Service Unavailable','504':'Gateway Timeout','505':'HTTP Version Not Supported','506':'Variant Also Negotiates','507':'Insufficient Storage (WebDAV)','508':'Loop Detected (WebDAV)','510':'Not Extended','511':'Network Authentication Required'}
count = 0
def testUrl(url):
    global count
    res = requests.get(url)
    if str(res.status_code) in status_code.keys():
        print('>> '+colored(str(res.status_code)+str(' (')+str(status_code[str(res.status_code)])+str(') '),'cyan')+' : '+str(url))
        count+=1
        
def start():
    threads = []
    for url in urls:
        t = threading.Thread(target=testUrl, args=[url])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    driver.quit()
    if count == 0:
        print('\n',colored('[$] No Broken Links Found','green'))
    else:
        print('\n',colored('[$] '+str(count)+' Broken Link(s) Found','red'))
    print('\n')

start()



