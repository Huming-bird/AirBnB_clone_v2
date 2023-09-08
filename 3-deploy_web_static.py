#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""
from fabric.api import local, put, run, env
import time
import os.path
from datetime import datetime

env.hosts = ["54.174.125.206", "35.174.185.141"]
env.user = 'ubuntu'


def do_pack():
    """create a tar file of the folder web_static"""
    path = "versions/web_static"
    now = datetime.now()
    ext = now.strftime("%Y%m%d%H%M%S")
    archive = "%s_%s.tgz" % (path, ext)

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed:
            return None
    if local("tar -cvzf {} web_static".format(archive)).failed:
        return None
    return archive


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


def deploy():
    """distributed the archive to my web servers"""
    file = do_pack()
    if file is None:
        return False
    res = do_deploy(file)
    return res
