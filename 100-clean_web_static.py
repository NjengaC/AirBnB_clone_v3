#!/usr/bin/python3
""" Function that deploys """
from fabric.api import env
from fabric.operations import run, local, sudo
from fabric.context_managers import lcd, cd

env.hosts = ['54.144.140.209', '34.202.233.3']
env.user = "ubuntu"


def do_clean(number=0):
    """ Clean up some archive """

    number = int(number)
    path = '/data/web_static/releases'

    if number == 0 or number == 1:
        number = 1
    else:
        number -= 1

    with cd("{}".format(path)):
        sudo("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number + 1)))

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number + 1))


#    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
#    path = '/data/web_static/releases'
#    run('cd {} ; ls -t | tail -n +{} | xargs sudo rm -rf'.format(path, number))
