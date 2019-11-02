FROM python:3
RUN mkdir /src
RUN cd /src && git clone https://github.com/vvstdung89/youtube-dl
WORKDIR /src/youtube-dl
RUN git checkout http_server
RUN python3 -m venv venv
RUN pip3 install flask
COPY server/run.sh server/.
CMD ["/bin/bash","server/run.sh"]