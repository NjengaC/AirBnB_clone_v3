#!/usr/bin/python3
""" Fabric script to generate a .tgz archive from web_static """

from datetime import datetime
from fabric.api import env, local, put, run, runs_once
from fabric.operations import run, put, sudo
import os

env.hosts = ["54.144.140.209", "34.202.233.3"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


@runs_once
def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    local("mkdir -p versions")

    now = datetime.now()
    file_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

    archive_path = local("tar -cvzf versions/{} web_static".format(file_name))

    if archive_path.succeeded:
        return "versions/{}".format(file_name)
    else:
        return None
    local("sudo mkdir -p /tmp/")
    archive = archive_path.split("/")[-1]
    local("mv {} /tmp/".format(archive_path))
    path = "/data/web_static/releases"
    folder = archive.split(".")
    local("sudo mkdir -p /data/web_static/shared")
    local("sudo mkdir -p {}/{}/".format(path, folder[0]))
    new_archive = '.'.join(folder)
    local("sudo tar -xzf /tmp/{} -C {}/{}/ --strip-components=1"
          .format(new_archive, path, folder[0]))
    local("sudo rm /tmp/{}".format(archive))
    local("sudo rm -rf /data/web_static/current")
    local("sudo ln -sf {}/{} /data/web_static/current"
          .format(path, folder[0]))


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
        run("sudo tar -xzf /tmp/{} -C {}/{}/"
            .format(new_archive, path, folder[0]))
        run("sudo rm /tmp/{}".format(archive))
        run("sudo mv {}/{}/web_static/* {}/{}"
            .format(path, folder[0], path, folder[0]))
        run("sudo rm -rf {}/{}/web_static".format(path, folder[0]))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {}/{} /data/web_static/current"
            .format(path, folder[0]))
        print("New version deployed!")

        return True
    except Exception:
        return False


def deploy():
    """
    Create and archive and get its path
    """
    archive_path = do_pack()

    return do_deploy(archive_path) if archive_path else False
