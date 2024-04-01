#!/usr/bin/python3
"""Handles all default RESTFul API actions for Place objects"""
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")

    user_id = data['user_id']
    if not storage.get(User, user_id):
        abort(404)

    place = Place(city_id=city_id, **data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())
