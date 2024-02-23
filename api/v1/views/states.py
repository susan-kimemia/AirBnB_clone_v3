#!/usr/bin/python3
"""state modules"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    """using to_dict() to retrieve all state into a valid JSON"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    """retrieve states id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete state if the request require that"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    creating states using POST
    an api that creates state If the HTTP body
    request is not valid JSON, raise a 400 error
    """
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON' if not data else 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """the funtion update state using PUT"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    """Updating the State object with all key-value pairs of the dictionary"""
    for key, value in data.items():
        """ignoring the created_at, updated_at, and id"""
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
