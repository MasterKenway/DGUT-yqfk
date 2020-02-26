import re
import requests
import time
import json
import datetime

flag = False

current_time = time.localtime()


def login(username, password):
    url = "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html"

    session = requests.Session()

    origin = session.get(url=url)
    html = origin.content.decode('utf-8')

    pattern = re.compile(r"var token = \"(.*?)\";$", re.MULTILINE | re.DOTALL)

    token_tmp = pattern.search(html).group(1)

    cookies = {"languageIndex": "0",
               "last_oauth_appid": "illnessProtectionHome",
               "last_oauth_state": "home"}

    datas = {'username': username, 'password': password,
             '__token__': token_tmp, 'wechat_verif': ''}

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

    session.close()

    return target


def submitform(target):
    time_fmt = time.strftime("%Y-%m-%d", time.localtime())

    # 表单信息需要通过抓包获取较为稳妥，避免数据出错被辅导员查水表

    form = {"submit_time": time_fmt,
            "campus": 1,
            "card_number": "",
            "identity_type": 1,
            "tel": "",
            "connect_person": "",
            "connect_tel": "",
            "health_situation": 1,
            "have_contact_hubei_people": 0,
            "have_contact_illness_people": 0,
            "recent_travel_situation": "无",
            "remark": "无",
            "family_situation": [0],
            "is_specific_people": 1,
            "have_diagnosis": "null",
            "diagnosis_result": "null",
            "processing_method": "null",
            "have_gone_important_area": 0,
            "important_area": "null",
            "leave_important_area_time": "null",
            "last_time_contact_hubei_people": "null",
            "last_time_contact_illness_people": "null",
            "have_isolation_in_dg": 0,
            "end_isolation_time": "null",
            "is_in_dg": 2,
            "current_in_city": "null",
            "current_region": ["142", "", "", ],
            "plan_back_dg_time": "null",
            "back_dg_transportation": "null",
            "plan_details": "null",
            "card_type": 49,
            "huji_region": [],
            "jiguan_region": [],
            "family_region": [],
            "family_address_detail": "",
            "have_stay_area": 0,
            "importantArr": ['false', 'false', 'false', 'false', 'false',
                             'false', 'false', 'false', 'false', 'false',
                             'false', 'false', 'false', 'false', 'false',
                             'false', 'false', 'false', 'false', 'false',
                             'false', 'false', 'false', 'false', 'false',
                             'false', 'false', 'false'],
            "familyArr": ["true", "false", "false", "false", "false"]}

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

    result_json = yqjk_session.post(url="http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers_2, json=form)

    result = json.loads(result_json.text)

    

    print(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) + result['message'])

    return result


# 填写中央认证账号
def circle():

    username = ""

    password = ""

    code = 400

    while code != 200:
        result = submitform(login(username, password))

        if result['message'] == "今日已提交，请勿重复操作":
            break

        code = result['code']

        time.sleep(10)


def timetask():
    global flag
    global current_time

    another_time = time.localtime()
    day_1 = time.strftime("%d", current_time)
    day_2 = time.strftime("%d", another_time)

    if not flag:
        circle()
        flag = True

    else:
        if another_time > current_time and day_2 > day_1:
            flag = False


if __name__ == "__main__":

    while True:
        timetask()

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        today_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) + 1
        tomorrow_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))

        print("下次执行时间" + time.strftime("%H:%M:%S", tomorrow_time))

        time.sleep(tomorrow_time - today_time)

