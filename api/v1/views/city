#!/usr/bin/python3

""" City Class Flask blueprint"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def state_cities(state_id):
    """ Routes all cities of a state."""

    states = storage.all(State)
    # Validates resource
    if not 'State.' + state_id in states:
        abort(404)

    state = states['State.' + state_id]
    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]

        return jsonify(cities)
    # handles post request
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if not data['name']:
            return jsonify({'error': 'Missing name'}), 400
        city = City(name=data['name'], state_id=state_id)
        for attribute in data:
            if attribute not in ('state_id'):
                city[attribute] = data[attribute]
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """ Routes the city resource """

    cities = storage.all(City)

    if not 'City.' + city_id in cities:
        abort(404)

    city = cities['City.' + city_id]
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"})
        for attribute in data:
            if attribute not in ('id', 'state_id', 'created_at',
                                 'updated_at'):
                setattr(city, attribute, data[attribute])
        storage.save()
        return jsonify(city.to_dict()), 200
