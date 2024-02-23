#!/usr/bin/python3
"""
defines routes for places resources
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from models.city import City
from models.user import User


@app_views.route('cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def city_places(city_id):
    """
    routes places resources
    """

    city_id = 'City.' + city_id
    cities = storage.all(City)
    if city_id not in cities:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in cities[city_id].places]
        return jsonify(places)
    elif request.method == 'POST':
        data = request.get_json()
        users = storage.all(User)
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        elif 'user_id' not in data:
            return jsonify({"error": "Missing user_id"}), 400
        elif 'name' not in data:
            return jsonify({"error": "Missing name"}), 400
        elif 'User.' + data['user_id'] not in users:
            abort(404)
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def places(place_id):
    """
    routes a specific place resource
    """

    places = storage.all(Place)
    id_ = 'Place.' + place_id

    if id_ not in places:
        abort(404)
    if request.method == 'GET':
        return jsonify(places[id_].to_dict())
    elif request.method == 'DELETE':
        storage.delete(places[id_])
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.json
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        for attribute in data:
            if attribute not in ('id', 'created_at', 'updated_at'):
                setattr(places[id_], attribute, data[attribute])
        places[id_].save()
        storage.save()
        return jsonify(places[id_].to_dict()), 200
