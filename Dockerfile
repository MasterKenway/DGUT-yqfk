FROM alpine

ENV USERNAME=
ENV PASSWORD=
ENV CHATID=
ENV BOTTOKN=

WORKDIR /yqfk

RUN apk --no-cache add wget python unzip py-pip \
    && pip install --no-cache-dir apscheduler \
    && wget https://github.com/MasterKenway/DGUT-yqfk/archive/master.zip \
    && unzip master.zip \
    && rm master.zip \
    && cd DGUT-yqfk-master \

CMD ["python", "yqfk.py", "$USERNAME", "$PASSWORD", "$CHATID", "$BOTTOKN"]