# -*- coding: utf-8 -*-
"""
Created on Wed Sept 7 8:54:35 2019

@author: xici
"""

import requests
import re
import json
import os,sys,time,logging
import codecs
import random
#import thread #2
from threading import Thread as thread #3
import types
from requests.cookies import RequestsCookieJar

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
class ChooseCourse(object):
    def __init__(self):
        
        self.session = requests.session()
        self.host="www.jpyx.cn:8080"
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            #,'Origin':'www.jpyx.cn:8080'
            #,'Referer':'http://www.jpyx.cn:8080/jpyx/a/yx/yxCurrvar'
            }
        
        self.index="http://www.jpyx.cn:8080/jpyx/a/yx/yxCurrvar"
        self.channels=[]
        self.cookie_jar = RequestsCookieJar()
        
        self.thecookies={}
        
    def setCookies(self,cookiestr):
        #JSESSIONID=F162F38C6EF8D79DA7C1E0F7AD109F2B; jeeplus.session.id=004545f27839473b8226332b5e1dcf67; pageNo=1; pageSize=100
        self.cookie_jar.set("JSESSIONID", "F162F38C6EF8D79DA7C1E0F7AD109F2B", domain=self.host)
        self.cookie_jar.set("jeeplus.session.id", "004545f27839473b8226332b5e1dcf67", domain=self.host)
        self.cookie_jar.set("pageNo", "1", domain=self.host)
        self.cookie_jar.set("pageSize", "100", domain=self.host)
        
        #res = requests.get(url, cookies=self.cookie_jar)
    
    #response: {"success":false,"errorCode":"-1","msg":"对不起，选课时间还没有到！请耐心等待!"}
    #response: {"success":false,"errorCode":"-1","msg":"非常抱歉，您已选中本课程！"}
    def choose(self,id):
        url='http://www.jpyx.cn:8080/jpyx/a/yx/yxCourse/choose?ids='+str(id)
        r=self.session.get(url)
        r.encoding='UTF-8'
        #print(r.text)
        #print(r.json())
        return r.json()
    
    def getCourseList(self):
        url='http://www.jpyx.cn:8080/jpyx/a/yx/yxCurrvar/data1?yxCourse.id=&yxCourse.name=&score=&pageNo=1&pageSize=100&orderBy=timeinterval+asc&_='+str(int(round(time.time() * 1000)))
        r=self.session.get(url)
        r.encoding='UTF-8'
        return r.json()
        
    def login(self,username,password):
        url="http://www.jpyx.cn:8080/jpyx/a/login"
        data={'username':username,'password':password}
        r=self.session.post(url,data=data)
        #print(r.text)
        if '安全退出' in r.text:
            return True
        else:
            return False
        
    def readReg(self,regx,content,index):
        #regx = u'第 (\d+) 页'
        pattern = re.compile(regx)
        ob = pattern.search(content)
        return ob.group(index)
        
    def readPrice(self,pfile='price.json'):
        content=self.readTextFile(pfile)
        #json_str = json.dumps(python2json)
        return content
        
    def readTextFile(self,file,charset='UTF-8'):
        try:
            with codecs.open(file, "r",charset) as f:
                return f.read()
        except Exception as err:
            #print(1,err)
            return ''
            
    def writeTextFile(self,file,content,charset='UTF-8'):
        with codecs.open(file, "w",charset) as f:
            f.write(content)
    
    

#######################################
    #用这个
    def loads_jsonp(self,_jsonp):
        """
        解析jsonp数据格式为json
        :return:
        """
        try:
            return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
        except:
            raise ValueError('Invalid Input')
            
        
    def printCookie(self,r):
        thecookies = requests.utils.dict_from_cookiejar(r.cookies)
        print(thecookies)
        
    def testStrReg(self):
        target='window.wx_errcode=405;window.wx_code=\'021yjD222QpF1W0kw2522XbT222yjD2l\';'
        regx = 'window.wx_code=\'(\\S+?)\';'
        print(target)
        print(regx)
        ob = re.search(regx, target)
        print(ob)
        self.wxcode=ob.group(1)
        print(self.wxcode)
    
    def validUrl(self,url):
        if self.index in url:
            return True
        else:
            return False
            
    #生产环境正式使用
    def walk(self,courselist):
        logging.info('choose course')
        for c in courselist:
            r=self.choose(c[1]['id'])
            if r['success']:
                print('选课(%s)成功'%c[0])
            else:
                print('选课(%s)失败!!! 原因 "%s"'%(c[0],r['msg']))
        
    #测试用途
    def test(self):
        #2002,趣配音
        #1996,西班牙语
        list=[['趣配音',{'id':2002}],['西班牙语',{'id':1996}],['日语',{'id':1994}],['纸艺diy',{'id':2009}]]
        list=[['西班牙语',{'id':1996}]] #pass ok
        list=[['翼- studio',{'id':1960}]]
        for c in list:
            r=self.choose(c[1]['id'])
            if r['success']:
                print('选课(%s)成功'%c[0])
            else:
                print('选课(%s)失败!!! 原因 "%s"'%(c[0],r['msg']))
        
        # 创建多个线程来执行，本程序不需要
        #for i in range(10):
        #    thread(target=self.testDownloadPic, args=("Thread-%d"%i, i, ) ).start()
        pass
        
        
if __name__ == '__main__':
    #config log to file.
    logging.basicConfig(
            #level=logging.DEBUG,
            level=logging.INFO,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',#example: 2019/03/14 17:31:47 main.py[line:139] INFO 192.168.1.56
            #format='%(asctime)s %(levelname)s %(message)s',#example: 2019/03/14 17:31:47 INFO 192.168.1.56
            datefmt='%Y/%m/%d %H:%M:%S',
            filename='yx.log',
        )
    #print log to screen& log to ScriptLog.log
    #formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', "%Y/%m/%d %H:%M:%S")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', "%Y/%m/%d %H:%M:%S")
    logHandler = logging.StreamHandler()
    logHandler.setLevel(logging.DEBUG)
    logHandler.setFormatter(formatter)
    logging.getLogger('').addHandler(logHandler)
    
    
    #设置说明，第一选择的放到最前面，当同时间段的第一选择抢不到了，程序会继续抢后面的课程。
    wander=['趣配音','西班牙语','基础日语','纸艺diy']
    user=['登录用户ID','登录密码'] #需要修改。登录用户ID是电子学生证的ID，密码是手机号码
    
    
    choose=ChooseCourse()
    choose.setCookies(None)
    if not choose.login(user[0],user[1]):
        print('login failed')
        sys.exit(1)
        
    argv=sys.argv
    if len(argv)>1:
        if argv[1]=='test':
            choose.test()
            pass
    else:
        coursedata=choose.getCourseList()
        courselist=[]
        for w in wander:
            for c in coursedata['rows']:
                if c['name']==w:
                    courselist.append([w,c])
                    break
                    
        #print(courselist)
        choose.walk(courselist)
    
    
    
    

