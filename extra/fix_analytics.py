#/usr/bin/python

import copy

from fabfile.config import *
from fabric.api import env, parallel, roles, run, settings, sudo, task, cd
from fabfile.testbeds import testbed

@task
@roles('collector')
def fix_packages():
    with settings(warn_only=True):
        sudo("yum remove -y python-redis")
