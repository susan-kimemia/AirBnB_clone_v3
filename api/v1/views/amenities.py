#!/usr/bin/python3
"""amenity modules"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity():
    """using to_dict() to retrieve all amenities into a valid JSON"""
    amenities = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()
        ]
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """retrieve amenity id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity if the request require that"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    creating amenity using POST
    an api that creates amenity If the HTTP body
    request is not valid JSON, raise a 400 error
    """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON' if not data else 'Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """the funtion update amenity using PUT"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    """Updating the Amenity object with all key-value pairs of the dict"""
    for key, value in data.items():
        """ignoring the created_at, updated_at, and id"""
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
