#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import local, runs_once


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
