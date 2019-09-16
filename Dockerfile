FROM python:3.6
VOLUME /data

WORKDIR /spider

ENV ALL_PROXY 10.10.21.2:1087

RUN curl https://ip.cn/
RUN pip install pyspider 
RUN pip install pymongo
RUN pip install wsgidav==2.4.1

CMD ["pyspider","-c","/data/config.json"]

EXPOSE 5000