import youtube_dl
from flask import Flask

from flask_restful import Api, Resource, reqparse


class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_song(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        return ydl.download([url])


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('url')


class Song(Resource):
    def get(self):
        url = parser.parse_args()['url']
        download_success = download_song(url)
        return {'downloaded': bool(download_success)}


api.add_resource(Song, '/')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
