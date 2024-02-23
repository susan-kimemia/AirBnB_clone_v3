#!/usr/bin/python3
"""
Defines route linking Places and Amenities resources
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request
from os import getenv


@app_views.route('places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def place_amenities(place_id):
    """
    Route amenities linked to the place with place_id
    """

    places = storage.all(Place)
    place_id = 'Place.' + place_id
    if place_id not in places:
        abort(404)

    amenities = [amenity.to_dict() for amenity in places[place_id].amenities]

    return jsonify(amenities), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST', 'DELETE'])
def del_place_amenities(place_id, amenity_id):
    """
    Processes POST or DELETE request
    """

    places = storage.all(Place)
    amenities = storage.all(Amenity)
    place_id = 'Place.' + place_id
    amenity_id = 'Amenity.' + amenity_id

    if place_id not in places:
        abort(404)
    elif amenity_id not in amenities:
        abort(404)
    place = places[place_id]
    amenity = amenities[amenity_id]

    if amenity not in place.amenities:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        place.amenity_ids.remove(amenity)
        place.save()
        return jsonify({}), 200
    else:
        place.amenities.remove(amenity)
        place.save()
        return jsonify({}), 200
