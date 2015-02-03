#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

is_https = False    # if your set always use ssl in v2ex setting,set is_https == True.vice-verse set it False
username = 'username'   # your v2ex username
password = 'password'    # your v2ex password ; if is_https == True use https in next 3 lines.
login_url = 'https://v2ex.com/signin'
home_page = 'https://www.v2ex.com'
mission_url = 'https://www.v2ex.com/mission/daily'
balance_url = 'https://www.v2ex.com/balance'

if not is_https:
    login_url = login_url[:4] + login_url[5:]
    home_page = home_page[:4] + home_page[5:]
    mission_url = mission_url[:4] + mission_url[5:]
    balance_url = balance_url[:4] + balance_url[5:]

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"

headers = {
        "User-Agent" : UA,
        "Host" : "www.v2ex.com",
        "Referer" : "http://www.v2ex.com/signin",
        "Origin" : "http://www.v2ex.com"
        }

v2ex_session = requests.Session()

def make_soup(url,tag,name):
    page = v2ex_session.get(url,headers=headers,verify=False).text
    soup = BeautifulSoup(page)
    soup_result = soup.find(attrs = {tag:name})
    return soup_result

once_vaule = make_soup(login_url,'name','once')['value']

post_info = {
    'u' : username,
    'p' : password,
    'once' : once_vaule,
    'next' : '/'
}

#登录
resp = v2ex_session.post(login_url,data=post_info,headers=headers,verify=False)

#检查是否已领取奖励
successful = make_soup(mission_url, 'class', 'fa fa-ok-sign')
if successful:
    localtime = time.asctime( time.localtime(time.time()))
    sys.exit('已领今日登录奖励')

#领取今日登录奖励
short_url = make_soup(mission_url, 'class', 'super normal button')['onclick']
first_quote = short_url.find("'")
last_quote = short_url.find("'", first_quote+1) #str.find(str, beg=0 end=len(string))
final_url = home_page + short_url[first_quote+1:last_quote]
page = v2ex_session.get(final_url,headers=headers,verify=False).content

#打印领取奖励结果
suceessful = make_soup(mission_url, 'class', 'fa fa-ok-sign')
if suceessful:
    localtime = time.asctime( time.localtime(time.time()))
    print '------' + localtime + '------' 
    print '领取奖励成功'
    table = make_soup(balance_url, 'class', 'data')
    balance_tr = table.findAll('tr')[1]
    current_balance = balance_tr.findAll('td')[3]
    print '当前账户余额: ' + current_balance.text
    bonus = balance_tr.findAll('td')[4].text
    print bonus
    print
else:
    print "出错了"