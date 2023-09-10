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
    """ this fnc deletes old archives from a server """
    run(f"ls -ltr {directory} > file_list.txt")

    if number > 1:
        run(f"head -n {number} file_list.txt > selected_files.txt")

    if number == 0 or number == 1:
        run("tail -n 1 file_list.txt > selected_files.txt")

    with cd(directory):
        run("while read -r line; do "
            "filename=$(echo \"$line\" | awk '{print $NF}'); "
            "if [ -f \"$filename\" ]; then "
            "rm -f \"$filename\"; "
            "echo \"Deleted: $filename\"; "
            "else "
            "echo \"File not found: $filename\"; "
            "fi; "
            "done < selected_files.txt")

    run("rm -f file_list.txt selected_files.txt")
