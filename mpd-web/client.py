#!/usr/bin/env python3
# coding: utf-8

import musicpd
import os
from pathlib import Path
import hashlib

class Client():
    def __init__(self):
        self.mpd = musicpd.MPDClient()
        self.mpd.connect()

    def close(self):
        self.mpd.disconnect()

    def generate_album_id(self, file):
        return str(int(hashlib.md5(file.encode('utf-8')).hexdigest(), 16))
        
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
            
            # read and save album art
            album_art_dir = os.path.join(os.path.dirname(__file__), 'build', 'static', 'img')
            album_art_path = os.path.join(album_art_dir, album_id + '.jpg')
            album_artwork = True
            if not os.path.isfile(album_art_path):
                picture_data = self.read_picture(file)
                if picture_data is not None:
                    Path(os.path.dirname(album_art_path)).mkdir(parents=True, exist_ok=True)
                    with open(album_art_path, 'wb') as file:
                        file.write(picture_data)
                else:
                    album_artwork = False

            data.append({
                "id": album_id,
                "name": album_name,
                "artist": album_artist,
                "year": album_year,
                "artwork": album_artwork
            })
        return data