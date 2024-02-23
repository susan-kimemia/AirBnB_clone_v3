#!/usr/bin/python3
"""City modules"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_all_cities():
    """Retrieve all cities and return a valid JSON."""
    cities = [city.to_dict() for city in storage.all(City).values()]
    return jsonify(cities)


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_for_state(state_id):
    """Retrieve cities for a given state and return a valid JSON."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city and return a empty dictionary with the status code 200."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create  new city for a given state and
    return the new city with status code 201.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON' if not data else 'Missing name')

    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Update a city and return the updated city with status code 200."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
