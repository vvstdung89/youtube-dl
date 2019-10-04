import time

from flask import Flask, json, request

from youtube_dl import YoutubeDL

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/get', methods=['GET'])
def get_companies():
    ydl = YoutubeDL({'nocheckcertificate': True, 'youtube_include_dash_manifest': False})
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
