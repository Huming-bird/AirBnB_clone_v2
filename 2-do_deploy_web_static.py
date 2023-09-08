#!/usr/bin/python3
""" this script executes a deploy function using fabric """
from fabric.api import put, run, env
from datetime import datetime
import os

env.hosts = ['54.174.125.206', '35.174.185.141']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """distributed the archive to my web servers"""
    if os.path.isfile(archive_path) is False:
        print('i am here')
        return False
    ds = archive_path.split("/")[-1]
    if put(archive_path, "/tmp/{}".format(ds)).failed:
        print('unsuccesful')
        return False
    name = ds.split(".")[0]
    if run("rm -rf /data/web_static/releases").failed:
        return False
    if run("mkdir -p /data/web_static/releases").failed:
        return False
    if run("tar -xzvf /tmp/{} -C /data/web_static/releases".
            format(ds)).failed:
        return False
    if run("mkdir /data/web_static/releases/{}".format(name)).failed:
        return False

    if run("mv /data/web_static/releases/web_static/*\
            /data/web_static/releases/{}".format(name)).failed:
        return False
    if run("rm /tmp/{}".format(ds)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(name)).failed:
        return False
    return True
