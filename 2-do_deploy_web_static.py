#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.25.168.28', '100.26.238.37']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_folder = archive_filename.replace('.tgz', '').replace('.tar.gz', '')


        put(archive_path, '/tmp/')

        run('mkdir -p /data/web_static/releases/{}'.format(archive_folder))

        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(archive_filename, archive_folder))

        run('rm /tmp/{}'.format(archive_filename))

        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
            .format(archive_folder, archive_folder))
        
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_folder))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
