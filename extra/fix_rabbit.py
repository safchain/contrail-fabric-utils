#/usr/bin/python

import copy

from fabfile.config import *
from fabric.api import env, parallel, roles, run, settings, sudo, task, cd
from fabfile.testbeds import testbed

@task
@roles('cfgm')
def fix_selinux():
    with settings(warn_only=True):
        sudo("restorecon -Rv /etc/rabbitmq/")
        sudo("service supervisor-support-service stop")
        sudo("service supervisor-support-service start")
