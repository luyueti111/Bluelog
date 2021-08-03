from flask import request, redirect, url_for
import requests, random
from bs4 import BeautifulSoup


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def login_bnu():
    poll = {"code": "0", "msg": "ok",
            "obj": [{"port": "37749", "ip": "182.34.61.137"}, {"port": "11041", "ip": "139.211.152.61"},
                    {"port": "37060", "ip": "220.175.247.143"}, {"port": "17679", "ip": "122.140.178.94"},
                    {"port": "31312", "ip": "171.114.208.13"}, {"port": "34521", "ip": "112.66.245.114"},
                    {"port": "34596", "ip": "42.235.171.114"}, {"port": "12933", "ip": "220.179.102.49"},
                    {"port": "22531", "ip": "116.209.101.168"}, {"port": "18160", "ip": "218.66.162.135"}], "errno": 0}
    poll = poll['obj']
    action = "https://sslvpn.bnu.edu.cn/dana-na/auth/url_default/login.cgi"
    params = {'tz_offset': '480',
              'username': '201811030421',
              'password': 'yml381281',
              'realm': 'LDAP-User',
              'btnSubmit': '登 陆'
              }
    r = requests.post(url=action,
                      proxies=random.choice(poll),
                      data=params,
                      headers={
                          'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                        "like Gecko) Chrome/92.0.4515.107 Safari/537.36"})
    r.encoding = 'utf-8'
    bs0bj = BeautifulSoup(r.text, features='html.parser')
    flag = bs0bj.find('span', {'class': 'cssSmall'})
    print(flag)
    return r.text
