import time
import pika
import json
import threading
import urllib.parse as urlparse
from urllib.parse import parse_qs
import os
import sys

sys.path.append(os.getcwd())

from youtube_dl import YoutubeDL

YTValids = ["18", "22", "43", "243", "247", "248", "271",
            "313", "272", "139", "140", "141", "249", "250", "251"]

rmq = os.environ.get('rmq')
if rmq == None:
    rmq = "localhost"
print(rmq)

clientID = os.environ.get('clientID')
if clientID == None:
    clientID = "N/A"

def on_request(ch, method, props, body):
    try:
        jsonObj = json.loads(body)
        print(jsonObj)

        if "proxy" not in jsonObj:
            youtubeConfig = {'nocheckcertificate': True,
                             'youtube_include_dash_manifest': False}
        else:
            youtubeConfig = {'nocheckcertificate': True,
                             'youtube_include_dash_manifest': False, 'proxy': jsonObj["proxy"]}

        start_time = time.time()
        ydl = YoutubeDL(youtubeConfig)
        r = ydl.extract_info(
            "https://www.youtube.com/watch?v=" + jsonObj['id'], False, "Youtube")
        elapsed_time = time.time() - start_time
        print(elapsed_time)

        formats = []
        for item in r['formats']:
            itag = item['format_id']
            if itag in YTValids:
                format = {
                    'itag': itag,
                    'url': item['url'],
                    'size': item['filesize'],
                    'ext': item['ext'],
                }
                parsed = urlparse.urlparse(item['url'])
                if len(parse_qs(parsed.query)['expire']) > 0:
                    format['expire'] = parse_qs(parsed.query)['expire'][0]
                formats.append(format)

        res = json.dumps({
            'type': "youtube",
            'id': jsonObj['id'],
            'title': r['title'],
            'thumbnail': r['thumbnail'],
            'duration': r['duration'],
            'formats': formats,
        })
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(res))

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as ex:
        if 'Error 429: Too Many Requests' in str(ex):
            print('Error 429: Too Many Requests detect')
            ch.close()
            return

        res = json.dumps({
            'type': "youtube",
            'id': jsonObj['id'],
            'clientID': clientID,
            'error': True,
        })

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(res))

        ch.basic_ack(delivery_tag=method.delivery_tag)

def run():
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rmq, port=15672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='getlink', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='getlink', on_message_callback=on_request)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()



def xrange(x):
    return iter(range(x))


def start(max_threads):
    for i in xrange(max_threads):
        print(i)
        t = threading.Thread(target=run)
        t.start()
        t.join(0)


if __name__ == '__main__':
    start(5)
