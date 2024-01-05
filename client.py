#!/usr/bin/env python3
# coding: utf-8

import os
import musicpd

ALBUM_ART_DIR = os.path.join(os.getcwd(), 'album_art')

class Client():
    def __init__(self):
        self.mpd = musicpd.MPDClient()
        self.mpd.connect()
        self.albums = []

    def close(self):
        self.mpd.disconnect()
        
    def read_album_art(self, file):
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

    def read_albums(self):
        albums_list = self.mpd.list('album')
        for album_name in albums_list:
            track = self.mpd.find('album', album_name)[0]
            album_artist = None
            album_year = None
            try:
                album_artist = track['artist']
                album_artist = track['albumartist']
                album_year = track['date'][:4]
            except:
                next
            self.albums.append({
                'album': album_name,
                'artist': album_artist,
                'year': album_year
            })
            file = track['file']
            album_art = os.path.join(ALBUM_ART_DIR, album_name + '.jpg')
            if (os.path.isfile(album_art)):
                continue
            try:
                data = self.read_album_art(file)
                with open(album_art, 'wb') as file:
                    file.write(data)
            except:
                next
    
if __name__ == '__main__':
    cli = Client()
    cli.read_albums()
    cli.close()