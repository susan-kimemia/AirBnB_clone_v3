#!/usr/bin/python3
"""
Defines Routes to users resources
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('users', strict_slashes=False,
                 methods=['GET', 'POST'])
@app_views.route('users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def users(user_id=None):
    """routes user resources. """

    users = storage.all(User)

    if not user_id:
        users = [user.to_dict() for user in users.values()]
        if request.method == 'GET':
            return jsonify(users)
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"error": "Not a JSON"}), 400
            elif 'email' not in data:
                return jsonify({"error": "Missing email"}), 400
            elif 'password' not in data:
                return jsonify({"error": "Missing password"}), 400
            user = User(password=data['password'], email=data['email'])
            for attribute in data:
                if attribute not in ('id', 'created_at', 'updated_at'):
                    setattr(user, attribute, data[attribute])
            user.save()
            return jsonify(user.to_dict()), 201

    id = 'User.' + user_id

    if id not in users:
        abort(404)
    elif request.method == 'GET':
        return jsonify(users[id].to_dict())
    elif request.method == 'DELETE':
        storage.delete(users[id])
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Not a JSON'}), 400
        for attribute in data:
            if attribute not in ('id', 'created_at', 'updated_at'):
                setattr(users[id], attribute, data[attribute])
        storage.save()
        return jsonify(users[id].to_dict())
