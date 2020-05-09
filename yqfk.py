#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import re
import requests
import time
import sys

username = ""
password = ""
chat_id = ""
bot_token = ""


def get_page(message):
    url = "https://cas.dgut.edu.cn/home/Oauth/getToken/appid/illnessProtectionHome/state/home.html"
    session = requests.Session()
    origin = session.get(url=url)
    html = origin.content.decode('utf-8')
    pattern = re.compile(r"var token = \"(.*?)\";$", re.MULTILINE | re.DOTALL)
    token_tmp = pattern.search(html).group(1)
    cookies = {"languageIndex": "0", "last_oauth_appid": "illnessProtectionHome", "last_oauth_state": "home"}
    data = {'username': username, 'password': password, '__token__': token_tmp, 'wechat_verif': ''}
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response_json = session.post(url=url, headers=headers, cookies=cookies, data=data).json()

    pattern = re.compile(r"\"message\":\"(.*?)\",\"(.*?)\"}$", re.MULTILINE | re.DOTALL)
    login_info = pattern.search(response_json).group(1)

    print(login_info)
    if login_info == '登录错误':
        message.append(login_info)
        return;

    pattern = re.compile(r"\"info\":\"(.*?)\"}$", re.MULTILINE | re.DOTALL)
    target = pattern.search(response_json).group(1)
    session.close()
    return target


def post_form(target, message):
    yqfk_session = requests.Session()
    yqfk_acesstoken = yqfk_session.get(url=target.replace('\\', ''))
    pattern = re.compile(r"access_token=(.*?)$", re.MULTILINE | re.DOTALL)
    access_token = pattern.search(yqfk_acesstoken.url).group(1)
    headers_2 = {'authorization': 'Bearer ' + access_token}
    yqfk_session.get(url=yqfk_acesstoken.url)
    yqfk_info = yqfk_session.get('http://yqfk.dgut.edu.cn/home/base_info/getBaseInfo', headers=headers_2).json()
    yqfk_json = yqfk_info['info']

    while yqfk_json is None:
        print('获取失败，重新获取')
        message.append('获取失败，重新获取')
        yqfk_info = yqfk_session.get('http://yqfk.dgut.edu.cn/home/base_info/getBaseInfo', headers=headers_2).json()
        yqfk_json = yqfk_info['info']

    print(yqfk_info['message'])
    message.append(yqfk_info['message'])
    result = yqfk_session.post(url="http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers_2,
                               json=yqfk_json).json()

    while result is None:
        print('提交失败，重新提交')
        message.append('提交失败，重新提交')
        result = yqfk_session.post(url="http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers_2,
                                   json=yqfk_json).json()

    print(result['message'])
    message.append(result['message'])

    if result['message'] == '已提交' or result['message'] == '提交成功':
        print('二次提交，确认成功')
        result = yqfk_session.post(url="http://yqfk.dgut.edu.cn/home/base_info/addBaseInfo", headers=headers_2,
                                   json=yqfk_json).json()
        print(result['message'])
        message.append(result['message'])


def run():
    message = []
    target = get_page(message)
    if target is not None:
        post_form(target, message)
        print('任务完成: ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
        message.append('任务完成: ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
    if chat_id is not None:
        tgbot_url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + chat_id + '&text='
        for text in message:
            tgbot_url = tgbot_url + str(text) + '\n'
        tgbot_result = requests.get(url=tgbot_url).json()
        print('tgbot发送成功: ', tgbot_result['ok'])


if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print("参数出错")
        print(sys.argv[0], " <username> <password> [<ChatID> <BotToken>]")
        exit(0)
    elif len(sys.argv) == 3:
        print("Username: ", sys.argv[1])
        print("Password: ", sys.argv[2])
        username = sys.argv[1]
        password = sys.argv[2]
    elif len(sys.argv) == 4:
        print("Username: ", sys.argv[1])
        print("Password: ", sys.argv[2])
        print("ChatID: ", sys.argv[3])
        print("TgBotToken: ", sys.argv[4])
        username = sys.argv[1]
        password = sys.argv[2]
        chat_id = sys.argv[3]
        bot_token = sys.argv[4]

    schedule = BlockingScheduler()
    schedule.add_job(run, 'cron', hour=0, minute=10)
    print('任务开始: ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
    run()
    schedule.start()

