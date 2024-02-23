#!/usr/bin/python3
"""Index file"""
from flask import Flask
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """return a json status OK"""
    return jsonify(status='OK'), 200, {'Content-Type': 'application/json'}


@app_views.route('/stats', strict_slashes=False)
def count():
    """endpoint that retrieves the number of each objects by type:"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
