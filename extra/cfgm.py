#/usr/bin/python

import copy

from fabfile.config import *
from fabric.api import env, parallel, roles, run, settings, sudo, task, cd
from fabfile.testbeds import testbed

@task
@roles('cfgm')
def start():
    with settings(warn_only=True):
        sudo("service supervisor-config start")

@task
@roles('cfgm')
def stop():
    with settings(warn_only=True):
        sudo("service supervisor-config stop")
