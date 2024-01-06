import os
from flask import Flask, jsonify, render_template
from .client import Client

def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_url_path='',
        static_folder='build',
        template_folder='build'
    )

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route('/api')
    def api():
        cli = Client()
        data = cli.load()
        cli.close()
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    return app