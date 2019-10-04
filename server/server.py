import time

from flask import Flask, json, request

from youtube_dl import YoutubeDL

api = Flask(__name__)
ydl = YoutubeDL({'nocheckcertificate': True, 'youtube_include_dash_manifest': False, 'proxy': "http://localhost:1080"})

@api.route('/get', methods=['GET'])
def get_video():
    id = request.args.get('id')
    if id == "":
        return ""
    start_time = time.time()
    r = ydl.extract_info("https://www.youtube.com/watch?v=" + id, False, "Youtube")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    return json.dumps(r)


if __name__ == '__main__':
    api.run()
