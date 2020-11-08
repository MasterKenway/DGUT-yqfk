## Usage

```
USERNAME   # 学号
PASSWORD   # 中央认证系统密码
SCKEY      # Server 酱密钥
```

[Server 酱密钥获取](http://sc.ftqq.com/)

默认在 00:10 的时候提交

### 方法一 (docker-compose)

```yaml
version: "3.1"

services:
  yqfk:
    image: masterkenway/dgut_yqfk
    environment:
      - USERNAME=
      - PASSWORD=
      - SCKEY=
    restart: always
```

### 方法二 (screen)

可以使用`screen`将程序放置在后台运行

```shell script
$ git clone https://github.com/MasterKenway/DGUT-yqfk.git && cd DGUT-yqfk 
$ pip install -r requirements.txt # 如果运行时报错找不到模块，请确认安装了pip3并将本条命令开头的pip改为pip3
$ screen -US yqfk # Ctrl + A + D 离开 screen
$ python3 yqfk.py USERNAME PASSWORD SCKEY
```

