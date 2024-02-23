#!/usr/bin/python3
"""
Defines routes for Reviews resource
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('places/<place_id>/reviews', strict_slashes=False,
                 methods=["GET", "POST"])
def place_reviews(place_id):
    """
    Retrieves review resources on a place
    """
    places = storage.all(Place)
    id = 'Place.' + place_id

    if id not in places:
        abort(404)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in places[id].reviews]
        return jsonify(reviews)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        elif 'user_id' not in data:
            return jsonify({"error": "Missing user_id"}), 400
        elif 'text' not in data:
            return jsonify({"error": "Missing text"}), 400
        elif 'User.' + data['user_id'] not in data:
            abort(404)
        review = Review(**data)
        return jsonify(review.to_dict()), 201


@app_views.route('reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def review(review_id):
    """
    Retreives a review via its id
    """

    id = 'Review.' + review_id
    reviews = storage.all(Review)
    if id not in reviews:
        abort(404)

    if request.method == 'GET':
        return jsonify(reviews[id].to_dict())
    elif request.method == 'PUT':
        data = request.get_json()

        if not data:
            return jsonify({"error": "Not a json"})
        for attribute in data:
            if attribute not in ('id', 'created_at', 'updated_at'):
                setattr(reviews[id], attribute, data[attribute])
        storage.save()
        return jsonify(reviews[id].to_dict())
    storage.delete(reviews[id])
    storage.save()
