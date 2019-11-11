FROM python:3
RUN mkdir /src
RUN echo v4
RUN cd /src && git clone --depth 1  --single-branch --branch http_server https://github.com/vvstdung89/youtube-dl
WORKDIR /src/youtube-dl
RUN python3 -m venv venv
RUN pip3 install pika
COPY server/run.sh server/.
COPY server/server.py server/.
CMD ["/bin/bash","server/run.sh"]