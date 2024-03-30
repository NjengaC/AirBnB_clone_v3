#!/usr/bin/python3
"""
States APIs
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def states_fetch():
    """GETS ALL STATES"""
    if request.method == 'POST':
        data = request.get_json()
        if data is not None:
            if 'name' not in data:
                abort(400, "Missing name")
            new = State(**data)
            storage.new(new)
            storage.save()
            return jsonify(new.to_dict()), 201
        abort(400, "Not  a JSON")
    elif request.method == "GET":
        states = storage.all("State").values()
        return jsonify([obj.to_dict() for obj in states])


@app_views.route("/states/<state_id>",
                 methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def state_by_id(state_id=""):
    """GETS A STATE BY ID AND OR DELETES IT OR UPDATES IT"""
    result = [v for k, v in storage.all("State").
              items() if k.split(".")[1] == state_id]
    if result == []:
        abort(404)
    if request.method == "DELETE":
        storage.delete(result[0])
        storage.save()
        return jsonify({}), 200
    elif request.method == 'GET':
        return jsonify(result[0].to_dict())
    elif request.method == "PUT":
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(result[0], key, value)
            result[0].save()
            return jsonify(result[0].to_dict()), 200
        abort(400, "Not a  JSON")
