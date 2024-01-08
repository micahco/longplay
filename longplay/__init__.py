#!/usr/bin/env python3
# coding: utf-8

import threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from .client import Client

def cache_albums():
    cli = Client()
    cli.load_albums()
    cli.close()


def create_app(test_config=None):
    t1 = threading.Thread(target=cache_albums)
    t1.start()

    app = Flask(
        __name__,
        instance_relative_config=True,
        static_url_path='',
        static_folder='build',
        template_folder='build'
    )
    CORS(app)

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route('/api', methods = ['GET', 'POST'])
    def api():
        if request.method == 'GET':
            cli = Client()
            albums = cli.load_albums()
            cli.close()
            return jsonify(albums)
        if request.method == 'POST':
            try:
                album = request.json.get('album')
                cli = Client()
                cli.play_album(album)
                cli.close()
                return jsonify(statusCode = 200), 200
            except:
                return jsonify(statusCode = 500), 500
    
    return app