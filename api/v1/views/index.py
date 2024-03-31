#!/usr/bin/python3
"""
index - status OK
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns server status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def stats():
    """
    endpoint that retrieves the number of each objects by type:
    """
    result = {
        'amenities': storage.count("Amenity"),
        'cities': storage.count("City"),
        'places': storage.count("Place"),
        'reviews': storage.count("Review"),
        'states': storage.count("State"),
        'users': storage.count("User")
    }

    return jsonify(result)
