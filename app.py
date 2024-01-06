#!/usr/bin/env python3
# coding: utf-8

import os
from pathlib import Path
import hashlib
from flask import Flask, jsonify, send_from_directory
import musicpd

class Client():
    def __init__(self):
        self.mpd = musicpd.MPDClient()
        self.mpd.connect()

    def close(self):
        self.mpd.disconnect()

    def generate_album_id(self, file):
        return int(hashlib.md5(file.encode('utf-8')).hexdigest(), 16)
        
    def read_picture(self, file):
        try:
            offset = 0
            pic = self.mpd.readpicture(file, offset)
            bin = int(pic['binary'])
            size = int(pic['size'])
            data = pic['data']
            while (offset + bin < size):
                offset += bin
                pic = self.mpd.readpicture(file, offset)
                data += pic['data']
            return data
        except:
            return None
    
    def get_album_artist(self, track):
        try:
            album_artist = track['artist']
            album_artist = track['albumartist']
            return album_artist
        except:
            return None

    def get_album_year(self, track):
        try:
            return track['date'][:4]
        except:
            return None

    def load(self):
        data = []
        albums_list = self.mpd.list('album')
        # TODO: include progress bar
        for album_name in albums_list:
            # read metadata
            track = self.mpd.find('album', album_name)[0]
            file = track['file']
            album_id = self.generate_album_id(file)
            album_artist = self.get_album_artist(track)
            album_year = self.get_album_year(track)
            data.append({
                "_id": album_id,
                "album": album_name,
                "artist": album_artist,
                "year": album_year
            })
            # read and save album art
            album_art_dir = os.path.join(os.getcwd(), 'static', 'img')
            album_art_path = os.path.join(album_art_dir, str(album_id) + '.jpg')
            if not os.path.isfile(album_art_path):
                picture_data = self.read_picture(file)
                if picture_data is not None:
                    Path(os.path.dirname(album_art_path)).mkdir(parents=True, exist_ok=True)
                    with open(album_art_path, 'wb') as file:
                        file.write(picture_data)
        return data

if __name__ == '__main__':
    app = Flask(__name__, static_url_path='')

    @app.route('/')
    def index():
        return send_from_directory('web', 'index.html')
    
    @app.route('/api')
    def api():
        cli = Client()
        data = cli.load()
        cli.close()
        return jsonify(data)
    
    app.run()