#!/usr/bin/python3
"""It is time to start your API!"""
from flask import Flask, jsonify, make_response
from models import *
from models import storage
from api.v1.views import app_views
from flask import Blueprint
import os
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r'/*': {"origins": "0.0.0.0"}})

"""Registering the blue print of appviews"""
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def not_found_error(error):
    """
    a handler for 404 errors that returns a
    JSON-formatted 404 status code response
    """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    declare a method to handle
    @app.teardown_appcontext that calls storage.close()
    """
    storage.close()


if __name__ == '__main__':
    """get the host env variable or use default"""
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
