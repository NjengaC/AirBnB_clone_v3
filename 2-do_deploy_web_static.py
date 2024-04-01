#!/usr/bin/python3
"""
Fabric script that distributes an archive web servers
"""
from datetime import datetime
from fabric.api import *
from fabric.operations import run, put, sudo
import os

env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    distributes an archive to web servers, using the function do_deploy
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        path = "/data/web_static/releases"
        put("{}".format(archive_path), "/tmp/{}".format(archive))
        folder = archive.split(".")
        run("sudo mkdir -p {}/{}/".format(path, folder[0]))
        new_archive = '.'.join(folder)
        run("sudo tar -xzf /tmp/{} -C {}/{}/ --strip-components=1"
            .format(new_archive, path, folder[0]))
        run("sudo rm /tmp/{}".format(archive))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {}/{} /data/web_static/current"
            .format(path, folder[0]))
        print("New version deployed!")
        return True
    except Exception:
        return False
