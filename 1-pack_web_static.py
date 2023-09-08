#!/usr/bin/python3
"""abric script that generates a .tgz archive from the
   contents of the web_static folder of your AirBnB Clone repository"""
from fabric.api import local
from fabric.api import get
from fabric.api import put
from fabric.api import reboot
from fabric.api import run
from fabric.api import sudo
from fabric.context_managers import cd
import time
import os.path
from datetime import datetime


def do_pack():
    """create a tar file of the folder web_static"""

    now = datetime.now()
    ext = now.strftime("%Y%m%d%H%M%S")
    archive = "web_static_{}.tgz".format(ext)

    local("mkdir -p versions")

    with cd("versions"):
        result = local("tar -czvf {} ../web_static".format(archive))
        if result.failed:
            return None

    return local("ls versions/*.tgz")
