#!/usr/bin/python3
"""abric script that generates a .tgz archive from the
   contents of the web_static folder of your AirBnB Clone repository"""
from fabric.api import local
import time
import os.path
from datetime import datetime


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
