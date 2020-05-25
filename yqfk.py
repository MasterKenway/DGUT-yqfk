#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import re
import requests
import time
import sys
import json

username = ""
password = ""
sckey = ""  # ServerChan Key


def get_page(message, target):
    url = "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html"
    session = requests.Session()
    origin = session.get(url=url)
    html = origin.content.decode('utf-8')
    pattern = re.compile(r"var token = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
    token_tmp = pattern.search(html).group(1)
    cookies = {"languageIndex": "0", "last_oauth_appid": "illnessProtectionHome", "last_oauth_state": "home"}
    data = {'username': username, 'password': password, '__token__': token_tmp, 'wechat_verif': ''}
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response = session.post(url=url, headers=headers, cookies=cookies, data=data).json()

    response_json = json.loads(response)

    if response_json['message'] != '验证通过':
        console_msg("登陆验证失败", 1)
        message.append(response_json['message'])
        return 1
    else:
        console_msg("登陆验证成功", 0)

    target.append(response_json['info'])
    session.close()
    return 0


def post_form(message, target):
    console_msg(target[0])
    yqfk_session = requests.Session()
    yqfk_acesstoken = yqfk_session.get(url=target[0])
    pattern = re.compile(r"access_token=(.*?)$", re.MULTILINE | re.DOTALL)
    access_token = pattern.search(yqfk_acesstoken.url).group(1)
    headers_2 = {'authorization': 'Bearer ' + access_token}
    yqfk_session.get(url=yqfk_acesstoken.url)
    yqfk_info = yqfk_session.get('http://yqfk.dgut.edu.cn/home/base_info/getBaseInfo', headers=headers_2).json()
    yqfk_json = yqfk_info['info']

    console_msg(yqfk_info['message'])
    message.append(yqfk_info['message'])
    result = yqfk_session.post(url="http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers_2,
                               json=yqfk_json).json()

    console_msg(result['message'])
    message.append(result['message'])

    if '已提交' in result['message'] or '成功' in result['message']:
        console_msg('二次提交，确认成功', 0)
        result = yqfk_session.post(url="http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers_2,
                                   json=yqfk_json).json()
        console_msg(result['message'])
        message.append(result['message'])
        return 0
    console_msg("二次提交，确认失败", 1)
    return 1


def post_message(text, desp=None):
    if sckey is not None:
        url = "https://sc.ftqq.com/" + sckey + ".send?text=" + text
        if desp is not None:
            url = url + "&desp="
            for d in desp:
                url = url + str(d) + "%0D%0A%0D%0A"
        rep = requests.get(url=url).json()
        if rep['errno'] == 0:
            console_msg('ServerChan 发送成功', 0)
        else:
            console_msg('ServerChan 发送失败', 1)


def run():
    message = []
    target = []
    result = get_page(message, target)
    if result == 0:
        res = post_form(message, target)
        if res == 0:
            message.append('任务完成: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            post_message("疫情防控: 成功", message)
            console_msg('任务完成', 0)
        else:
            post_message("疫情防控: 二次验证失败", message)
    else:
        post_message("疫情防控: 获取页面失败", message)


def console_msg(msg, level=2):
    header = ('[SUCCESS]', '[ERROR]', '[INFO]')
    color = ("\033[32;1m", "\033[31;1m", "\033[36;1m")
    print(color[level], header[level], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg + "\033[0m")


if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        console_msg("参数出错", 1)
        console_msg(sys.argv[0] + " <username> <password> [<sckey>]")
        exit(1)
    else:
        console_msg("Username: " + sys.argv[1])
        console_msg("Password: " + sys.argv[2])
        username = sys.argv[1]
        password = sys.argv[2]
    if len(sys.argv) == 4:
        console_msg("ServerChan Key: " + sys.argv[3])
        sckey = sys.argv[3]
    else:
        console_msg("不启用 Server 酱")

    schedule = BlockingScheduler()
    schedule.add_job(run, 'cron', hour=0, minute=10)
    console_msg('任务开始')
    run()
    schedule.start()
