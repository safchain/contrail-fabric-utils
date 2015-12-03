#/usr/bin/python

import copy

from fabfile.config import *
from fabric.api import env, parallel, roles, run, settings, sudo, task, cd
from fabfile.testbeds import testbed

@task
@roles('database')
def start():
    with settings(warn_only=True):
        sudo("service supervisor-database start")

@task
@roles('database')
def stop():
    with settings(warn_only=True):
        sudo("service supervisor-database stop")
