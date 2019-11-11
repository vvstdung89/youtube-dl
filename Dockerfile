FROM python:3.7-alpine
RUN apk add --no-cache git
RUN mkdir -p /src/youtube-dl
WORKDIR /src/youtube-dl
RUN pip3 install pika

RUN echo v0.2
RUN cd /src && git clone --depth 1  --single-branch --branch http_server https://github.com/vvstdung89/youtube-dl
COPY server/server.py server/.

CMD ["/bin/sh","server/run.sh"]