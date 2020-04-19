# [DGUT-yqfk](https://github.com/MasterKenway/DGUT-yqfk)



在脚本的三个参数里面输入对应的值

```
username = ""	#学号
password = ""	#中央认证系统密码
chat_id = "" 	#telegram用户ID（可选）
bot_token = ""	#tgbot token
```

默认时间在00:10的时候自动提交，可自行修改时间

定时运行使用了`apscheduler`

```
pip install apscheduler
```

可以使用`screen`将程序放置在后台运行

```
screen -S yqfk
python3 yqfk.py #Ctrl + A + D 退出当前的screen
```

