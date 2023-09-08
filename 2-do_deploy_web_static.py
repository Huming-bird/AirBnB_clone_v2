from fabric.api import put, run, env
from datetime import datetime
import os

env.hosts = ['54.174.125.206', '35.174.185.141']


def do_deploy(archive_path):
    """ this function deploys .tgz file to my server """
    if not os.path.isfile(archive_path):
        return False

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_filename = os.path.basename(archive_path)
    name = os.path.splitext(archive_filename)[0]

    remote_tmp = "/tmp/{}".format(archive_filename)
    remote_dir = "/data/web_static/releases/{}/".format(name)

    put(archive_path, remote_tmp)
    run("mkdir -p {}".format(remote_dir))
    run("tar -xzf {} -C {}".format(remote_tmp, remote_dir))
    run("rm {}".format(remote_tmp))
    run("mv {}web_static/* {}".format(remote_dir, remote_dir))
    run("rm -rf {}web_static".format(remote_dir))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(remote_dir))

    return True
