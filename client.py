#!/usr/bin/env python3
# coding: utf-8

import os
import hashlib
import musicpd

ALBUM_ART_DIR = os.path.join(os.getcwd(), 'album_art')

class Client():
    def __init__(self):
        self.mpd = musicpd.MPDClient()
        self.mpd.connect()
        self.albums = []

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

    def read_albums(self):
        print('loading albums')
        albums_list = self.mpd.list('album')
        for album_name in albums_list:
            track = self.mpd.find('album', album_name)[0]
            file = track['file']
            album_id = self.generate_album_id(file)
            album_artist = self.get_album_artist(track)
            album_year = self.get_album_year(track)
            self.albums.append({
                "_id": album_id,
                "album": album_name,
                "artist": album_artist,
                "year": album_year
            })
            album_art_path = os.path.join(ALBUM_ART_DIR, str(album_id) + '.jpg')
            if not os.path.isfile(album_art_path):
                picture_data = self.read_picture(file)
                if picture_data is not None:
                    print('loading album art')
                    with open(album_art_path, 'wb') as file:
                        file.write(picture_data)

if __name__ == '__main__':
    cli = Client()
    cli.read_albums()
    print(cli.albums[0])
    cli.close()