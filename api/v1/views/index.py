#!/usr/bin/python3
"""
Index view
"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of the web server
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Stats of the web server
    """
    from models.review import Review
    from models.state import State
    from models.user import User
    from models.place import Place
    from models.amenity import Amenity
    from models.city import City

    class_list = {'amenities': Amenity, 'cities': City, 'places': Place,
                  'reviews': Review, 'states': State, 'users': User}
    count_dict = {}

    for key, value in class_list.items():
        count = storage.count(value)
        count_dict[key] = count

    return jsonify(count_dict)

