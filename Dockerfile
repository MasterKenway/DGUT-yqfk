FROM alpine

LABEL maintainer="AUTUMN"

WORKDIR /app

ADD yqfk.py requirements.txt entrypoint.sh ./

RUN apk --no-cache add python3 py3-pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm requirements.txt \
    && chmod +x entrypoint.sh

RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

ENV USERNAME=
ENV PASSWORD=
ENV SCKYE=

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/entrypoint.sh"]
