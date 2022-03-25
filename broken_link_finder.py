import requests, threading, os
from bs4 import BeautifulSoup
from termcolor import colored
os.system('color')

print('   ****************************')
print('   *    BROKEN LINK FINDER    *')
print('   ****************************')

def fetch_urls():
    special_char = ['~','`','!','@','#','$','%','^','&','*','(',')',',','?','{','}','-','+','|','[',']','=','_','.','<','>']
    fetched_urls = []
    global list_of_urls
    for links in soup.find_all('a'):
        link = links.get('href')
        if link == None:
            pass
        elif link in fetched_urls:
            pass
        elif link[0] in special_char:
            pass
        elif link[:3] == 'tel':
            pass
        elif link[:4] == 'mail':
            pass
        elif link[0] == ' ':
            link = link.replace(' ','')
            fetched_urls.append(link)
        else:
            fetched_urls.append(link)
            
    for lnk in fetched_urls:
        item = ''
        for letter in lnk[0:4]:
            item += letter
        if item == 'http':
            list_of_urls.append(lnk)
        elif item[0] == '/':
            temp1 = url+lnk
            list_of_urls.append(temp1)
        else:
            temp2 = url+'/'+lnk
            list_of_urls.append(temp2)

status_code = {'300':'Multiple Choice','301':'Moved Permanently','302':'Found','303':'See Other','304':'Not Modified','307':'Temporary Redirect','308':'Permanent Redirect','400':'Bad Request','400':'Bad Request','401':'Unauthorized','402':'Payment Required','403':'Forbidden','404':'Not Found','405':'Method Not Allowed','406':'Not Acceptable','407':'Proxy Authentication Required','408':'Request Timeout','409':'Conflict','410':'Gone','411':'Length Required','412':'Precondition Failed','413':'Payload Too Large','414':'URI Too Long','415':'Unsupported Media Type','416':'Range Not Satisfiable','417':'Expectation Failed','418':'I am a teapot','421':'Misdirected Request','422':'Unprocessable Entity (WebDAV)','423':'Locked (WebDAV)','424':'Failed Dependency (WebDAV)','425':'Too Early','426':'Upgrade Required','428':'Precondition Required','429':'Too Many Requests','431':'Request Header Fields Too Large','451':'Unavailable For Legal Reasons','500':'Internal Server Error','501':'Not Implemented','502':'Bad Gateway','503':'Service Unavailable','504':'Gateway Timeout','505':'HTTP Version Not Supported','506':'Variant Also Negotiates','507':'Insufficient Storage (WebDAV)','508':'Loop Detected (WebDAV)','509':'Bandwidth Limit Exceeded (Apache)','510':'Not Extended','511':'Network Authentication Required','598':'Network Read Timeout Error','599':'Network Connect Timeout Error'}
broken_link_count = 0
total_link_count = 0            
def testUrl(url):
    global broken_link_count, total_link_count
    try:
        res = requests.get(url)
        total_link_count+=1
        if str(res.status_code) in status_code.keys():
            print('>> '+colored(str(res.status_code)+str(' (')+str(status_code[str(res.status_code)])+str(') '),'cyan')+' : '+str(url))
            broken_link_count+=1
    except:
        print(colored('[#] Not checked: '+str(url),'yellow'))
        
def start():
    threads = []
    for url in list_of_urls:
        t = threading.Thread(target=testUrl, args=[url])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    if broken_link_count == 0:
        print('\n')
        print(colored('[$] No Broken Links Found','green'))
    else:
        print('\n')
        print(colored('[$] '+str(broken_link_count)+' Broken Link(s) Found','red'))
    print(colored('[$] Total '+str(total_link_count)+' Link(s) Found','yellow'))


"""-----EXECUTE-----"""
status = True
while status:
    print('[eg: https://www.google.com]\n')
    url = str(input('Test URL: '))
    if 'https://' in url or 'http://' in url:
        print('\n')
        print('   ----------------------')
        print('   |  Finding Links...  |')
        print('   ----------------------')
        print('\n')
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        list_of_urls = []
        fetch_urls()
        start()
        xit = True
        while xit:
            nxt = str(input('\nDo you want to continue?(Y or N): ')).lower()
            if nxt == 'y':
                xit = False
                status = True
                broken_link_count = 0
                total_link_count = 0
            elif nxt == 'n':
                xit = False
                status = False
            else:
                xit = True
        print('\n')
    else:
        print('URL Incorrect! Please try again..')
        status = True





