FROM python:2.7
VOLUME /data

WORKDIR /spider

RUN pip install pyspider && pip install pymongo

CMD ["pyspider","-c","/data/config.json"]

EXPOSE 5000