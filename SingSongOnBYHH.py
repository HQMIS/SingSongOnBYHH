#-*-coding:utf-8-*-

# script: SingSongOnBYHH.py
# author: huangqimin@baidu.com

# note: 
# 1、This Python Script use Library urlllib2、urllib、cookielib:
#    see http://docs.python.org/2/library/urllib2.html
#    see http://docs.python.org/2/library/urllib.html
#    see http://docs.python.org/2/library/cookielib.html
# 2、Want to use Library requests, but Failed:

import urllib
import urllib2
import cookielib
import random
import time

class BYHH:
    def __init__(self, username, password):
        self.id = username
        self.pw = password
 
    def login(self):
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

        params = {'id': self.id, 'pw': self.pw}
        req = urllib2.Request('http://bbs.whnet.edu.cn/cgi-bin/bbslogin', urllib.urlencode(params))
        source = opener.open(req).read()
        print source

        msg = []
        for i in range(0, 10):
            first = source.find("'")
            source = source.replace("'", '"', 1)
            second = source.find("\'")
            source = source.replace("\'", '"', 1)
            msg.append(source[first+1:second])   

        cookie = ""
        for i in range(3, 10):
            cookie = cookie + msg[i] + ";"

        return cookie

class SING:
    def __init__(self, title, text, signature=1, start=7762):
        self.title = title
        self.text = text
        self.signature = signature
        self.start = start
 
    def sing(self, url, cookies):
        params = {'title': self.title, 'signature':self.signature, 'start':self.start, 'text': self.text}
        req = urllib2.Request(url, urllib.urlencode(params))
        req.add_header("Cookie", cookie)
        print urllib2.urlopen(req).read() 
 
if __name__ == '__main__':
    username = raw_input("UserName:")
    password = raw_input("PassWord:")
    board = raw_input("Board:")
    
    url = 'http://byhh.net/cgi-bin/bbssnd?board='+board+'&file='
    print url
    sleeptime = 15

    byhh = BYHH(username, password)
    cookie = byhh.login()

    f = open("./MUSIC.md", "r")
    musicList = f.readlines()
    for music in musicList:
        if "" == music.strip():
            pass
        else:
            sing = SING(music, music)
            sing.sing(url, cookie)
            print username + ' Sing ' + music
            # BYHH会检测，是否为机器登录
            # 看到的是如果sleeptime时间为一个数，则被判为机器登录
            # 所以这里生成随机数来处理
            sleeptime = 15 + random.randint(0, 15)
            time.sleep(sleeptime)
