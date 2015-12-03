#/usr/bin/python

import copy

from fabfile.config import *
from fabric.api import env, parallel, roles, run, settings, sudo, task, cd
from fabfile.testbeds import testbed

@task
@EXECUTE_TASK
@roles('database')
def configure_cassandra():
    if env.roledefs['database']:
        execute("configure_cassandra_node", env.host_string)

@task
def configure_cassandra_node(*args):
    database_nodes = copy.deepcopy(env.roledefs['database'])
    seeds = [node.split('@')[1] for node in database_nodes]

    for host_string in args:
        with settings(host_string=host_string):
            host = host_string.split('@')[1]
            cmd = ("sed -i -e 's/listen_address:.*/listen_address: %s/' "
                   "/etc/cassandra/conf/cassandra.yaml") % host
            sudo(cmd)

            cmd = ("sed -i -e 's/seeds:.*/seeds: \"%s\"/' "
                   "/etc/cassandra/conf/cassandra.yaml") % ','.join(seeds)
            sudo(cmd)

            cmd = ("sed -i -e 's/start_rpc:.*/start_rpc: true/' "
                   "/etc/cassandra/conf/cassandra.yaml")
            sudo(cmd)

            cmd = ("sed -i -e 's/rpc_address:.*/rpc_address: %s/' "
                   "/etc/cassandra/conf/cassandra.yaml") % host
            sudo(cmd)

            cmd = ("mkdir -p /var/lib/cassandra")
            sudo(cmd)

            cmd = ("chown cassandra:cassandra /var/lib/cassandra")
            sudo(cmd)

            cmd = ("sed -i -e 's/CASSANDRA_PROG=.*/CASSANDRA_PROG=\/sbin\/cassandra/' "
                   "/etc/init.d/cassandra")
            sudo(cmd)

            cmd = ("systemctl daemon-reload")
            sudo(cmd)

@task
@roles('database')
def start_cassandra():
    with settings(warn_only=True):
        sudo("service cassandra start")

@task
@roles('database')
def stop_cassandra():
    with settings(warn_only=True):
        sudo("service cassandra stop")
