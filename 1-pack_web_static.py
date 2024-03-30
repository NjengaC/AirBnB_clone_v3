#!/usr/bin/python3
""" Fabric script to generate a .tgz archive from web_static """

from fabric.api import local
from datetime import datetime


def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder """
    local("mkdir -p versions")

    now = datetime.now()
    file_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

    result = local("tar -cvzf versions/{} web_static".format(file_name))

    if result.succeeded:
        return "versions/{}".format(file_name)
    else:
        return None
