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
        return False
    ds = archive_path.split("/")[-1]
    if put(archive_path, "/tmp/{}".format(ds)).failed is True:
        return False
    name = ds.split(".")[0]
    if sudo("rm -rf /data/web_static/releases").failed is True:
        return False
    if sudo("mkdir -p /data/web_static/releases").failed is True:
        return False
    if sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(ds, name)).failed is True:
        return False
    if sudo("rm /tmp/{}".format(ds)).failed is True:
        return False
    if sudo("rm -rf /data/web_static/current").failed is True:
        return False
    if sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current".
            format(name)).failed is True:
        return False
    return True
