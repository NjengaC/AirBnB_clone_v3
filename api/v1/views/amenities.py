#!/usr/bin/python3
"""Handles all default RESTFul API actions for Amenity objects"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a specific Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an Amenity"""
    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    if 'name' not in data:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.json
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
