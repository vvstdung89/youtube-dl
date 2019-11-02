import time
import os
import sys
sys.path.append(os.getcwd())

from flask import Flask, json, request

from youtube_dl import YoutubeDL

YTValids = ["18", "22", "43", "243", "247", "248", "271", "313", "272", "139", "140", "141", "249", "250", "251"]

api = Flask(__name__)


@api.route('/youtube', methods=['GET'])
def get_youtube():
    id = request.args.get('id')
    proxy = request.args.get('proxy')

    if id == "":
        return ""

    if proxy != "":
        youtubeConfig = {'nocheckcertificate': True, 'youtube_include_dash_manifest': False}

    else:
        youtubeConfig = {'nocheckcertificate': True, 'youtube_include_dash_manifest': False, 'proxy': proxy}

    start_time = time.time()
    ydl = YoutubeDL(youtubeConfig)
    r = ydl.extract_info("https://www.youtube.com/watch?v=" + id, False, "Youtube")
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
            formats.append(format)

    return json.dumps({
        'title': r['title'],
        'thumbnail': r['thumbnail'],
        'duration': r['duration'],
        'formats': formats,
    })


if __name__ == '__main__':
    api.run()
