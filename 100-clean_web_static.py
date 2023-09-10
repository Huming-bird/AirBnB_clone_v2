#!/usr/bin/python3
""" this script executes a deploy function using fabric """
from fabric.api import put, run, env, local
from datetime import datetime
import os

env.hosts = ['54.174.125.206', '35.174.185.141']
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


directory = "/data/web_static/releases/"


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
