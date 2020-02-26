import re
import requests
import time

url = "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html"

session = requests.Session()

origin = session.get(url=url)
html = origin.content.decode('utf-8')

pattern = re.compile(r"var token = \"(.*?)\";$", re.MULTILINE | re.DOTALL)

token_tmp = pattern.search(html).group(1)

# 填写自己的中央认证账号及密码
username = ""

password = ""

cookies = {"languageIndex": "0", "last_oauth_appid": "illnessProtectionHome", "last_oauth_state": "home"}

datas = {'username': username, 'password': password, '__token__': token_tmp, 'wechat_verif': ''}

headers = {'Host': 'cas.dgut.edu.cn',
           'Connection': 'keep-alive',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.3',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Origin': 'https://cas.dgut.edu.cn',
           'Sec-Fetch-Site': 'same-origin',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Dest': 'empty',
           'Referer': 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,es;q=0.5,ru;q=0.4,pt;q=0.3,ja;q=0.2'}

response_json = session.post(url=url, headers=headers, cookies=cookies, data=datas)

pattern = re.compile(r"\"info\":\"(.*?)\"}$", re.MULTILINE | re.DOTALL)

target = pattern.search(response_json.json()).group(1)

time_fmt = time.strftime("%Y-%m-%d", time.localtime())

session.close()

yqjk_session = requests.Session()

yqjk_acesstoken = yqjk_session.get(url=target.replace('\\', ''))

pattern = re.compile(r"access_token=(.*?)$", re.MULTILINE | re.DOTALL)

access_token = pattern.search(yqjk_acesstoken.url).group(1)

headers_2 = {'Host': 'yqfk.dgut.edu.cn',
             'Connection': 'keep-alive',
             'Accept': 'application/json',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4051.0 Safari/537.36 Edg/82.0.425.3',
             'authorization': 'Bearer ' + access_token,
             'Origin': 'http://yqfk.dgut.edu.cn',
             'Referer': 'http://yqfk.dgut.edu.cn/main',
             'Accept-Encoding': 'gzip, deflate'}

yqjk_session.get(url=yqjk_acesstoken.url)

yqjk_info = yqjk_session.get('http://yqfk.dgut.edu.cn/home/base_info/getBaseInfo', headers=headers_2).json()

yqjk_json = yqjk_info['info']

counter = 0

result_save = ""

while True:
    result = yqjk_session.post(url="http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers_2,
                               json=yqjk_json).json()
    counter += 1
    if counter == 1:
        result_save = result
    if result['message'] == "今日已提交，请勿重复操作":
        break

if counter == 1:
    print(result_save)
else:
    print(result)
