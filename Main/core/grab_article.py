import re

import requests
import datetime
from bs4 import BeautifulSoup,Comment
import chardet
from Main.core.analyze_article import analyze

authorset ={'责任编辑','作者','来源'}


def getcontentfromweb(src):
    obj = requests.get(src)
    if obj.status_code==200:
        encod = chardet.detect(obj.content)['encoding']
        return obj.content.decode(encod, 'ignore')
    else:
        return False

def getcontent(html_str):
    soup =BeautifulSoup(html_str, 'html5lib')
    title =soup.title.string.encode().decode('utf-8')
    title =re.split('[-_]', title)[0]
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]
    ll = [x for x in soup.body.contents if x.name]
    maxflag = {'class': '', 'length': 0}
    getchildren(ll, '', maxflag)
    content = soup.body.find_all(class_=maxflag['class'])[0]

    reg1 = re.compile("<[^>]*>")
    wordcontent = reg1.sub('', soup.prettify()).split('\n')
    newcontent = ''.join(wordcontent)
    words = analyze(newcontent).word_cut()
    retime = re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', newcontent)
    if not retime:
        retime = str(datetime.datetime.now())
    else:
        retime = retime.group(0)

    return title, str(content), retime, words



def getchildren(ll,cls, maxflag):
    if ll:
        tmp =[]
        tmplen = 0
        for i, x in enumerate(ll):
            if x:
                item = {}
                item["text"] = ""
                item["children"] = []
                item["parentclass"] = cls
                if hasattr(x, "contents") and x.name != 'p':
                    item["children"] = getchildren(x.contents, x.get('class'), maxflag)
                else:
                    item["text"] = x.string
                tmp.append(item)
                tmplen += len(x.string) if x.string else 0
        if maxflag['length'] < tmplen:
            maxflag["class"] = cls
            maxflag["length"] = tmplen
        return tmp



def getcontet(title,lst):
    ctt = [x.strip() for x in lst]
    lstlen = [len(x.strip()) for x in ctt]
    threshold=50
    startindex = 0
    maxindex = lstlen.index(max(lstlen))
    endindex = 0
    author=''
    for i,v in enumerate(lstlen[:maxindex-3]):
        if title ==ctt[i].strip():
                startindex = i
                for j, v in enumerate(lstlen[i+1:maxindex]):
                   for key in authorset:
                       if key in ctt[j]:
                            author = ctt[j]
                            ctt[j+i] = ''
                break
    for i,v in enumerate(lstlen[maxindex:]):
        print()
        if v< threshold and (not ctt[maxindex+i+1].endswith('。') or not ctt[maxindex+i+1].endswith('。”')):
            endindex = i
            break
    content =[x for x in ctt[startindex:endindex + maxindex] if len(x.strip())>0]
    newcontent=''.join(content)
    words = analyze(newcontent).word_cut()
    retime =re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',newcontent)
    if not retime:
        retime =str(datetime.datetime.now())
    else:
        retime = retime.group(0)
    return content,retime,author,words

def run(url):
    ctthtml=getcontentfromweb(url)
    if ctthtml:
        title,content,retime,words =getcontent(ctthtml)
    return title,ctthtml,content,retime,words
