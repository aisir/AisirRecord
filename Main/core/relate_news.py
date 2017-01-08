import urllib
import requests
import chardet
from bs4 import BeautifulSoup
from threading import Thread
import redis
import jieba
def getnewlistfromweb(word):
    url = 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs{}=&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=newstitle&word={}'.format(word, word)
    obj = requests.get(url)
    news = []
    if obj.status_code==200:
        encod = chardet.detect(obj.content)['encoding']
        content = obj.content.decode(encod, 'ignore')
        soup = BeautifulSoup(content,'html5lib')
        newlist = soup.find_all(class_='result title', limit=1)
        for n in newlist:
            tmp={}
            tmp['title'] = n.find(class_='c-title').get_text()
            tmp['href'] = n.find(class_='c-title').find('a')['href']
            srcdat =  list(n.find(class_='c-title-author').stripped_strings)[0]
            tmp['srcdate'] =srcdat.replace(u'\xa0', u' ').replace(u'\xa5', u' ').replace(u'\xa6', u' ')
            news.append(tmp)
        return news
    else:
        return False

class MyThread(Thread):

    def __init__(self, word):
        Thread.__init__(self)
        self.word = word

    def run(self):
        self.result = getnewlistfromweb(self.word)

    def get_result(self):
        return self.result


def multitask(qie):
    threads = []
    result =[]

    for q in qie:
        t1 = MyThread(q)
        threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    for t in threads:
        result.extend(t.get_result())
    tmpresult = []
    for r in result:
        if r in tmpresult:
            continue
        else:
            tmpresult.append(r)

    return tmpresult


def redisresult(record):
    r = redis.Redis(host='127.0.0.1', port=6379)
    if r.exists(record.id):
        result = r.lrange(record.id, 0, -1)
        tmp = [eval(x) for x in result]
        return tmp
    else:
        qie = jieba.cut(record.title, cut_all=False)
        result = multitask(qie)
        for i in result:
            r.rpush(record.id, i)
        r.expire(record.id, 10)
        return result
