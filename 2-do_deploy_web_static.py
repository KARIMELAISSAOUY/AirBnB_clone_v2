#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once

env.hosts = ["34.73.0.174", "35.196.78.105"]
"""The list of host server IP addresses."""

@runs_once
def do_pack():
    """Archives the static files."""
    if not os.path.exists("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = f"versions/web_static_{cur_time.strftime('%Y%m%d%H%M%S')}.tgz"
    try:
        print(f"Packing web_static to {output}")
        local(f"tar -czf {output} web_static")
        archive_size = os.path.getsize(output)
        print(f"web_static packed: {output} -> {archive_size} Bytes")
    except Exception as e:
        print(f"An error occurred: {e}")
        output = None
    return output

def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    archive_filename = os.path.basename(archive_path)
    folder_name = archive_filename.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder_name}"
    success = False
    try:
        put(archive_path, f"/tmp/{archive_filename}")
        run(f"mkdir -p {folder_path}")
        run(f"tar -xzf /tmp/{archive_filename} -C {folder_path}")
        run(f"rm -rf /tmp/{archive_filename}")
        run(f"mv {folder_path}/web_static/* {folder_path}")
        run(f"rm -rf {folder_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_path} /data/web_static/current")
        print("New version deployed!")
        success = True
    except Exception as e:
        print(f"Deployment failed: {e}")
        success = False
    return success