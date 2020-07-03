#!/usr/bin/python3

import json
import os
from os import path
import subprocess
import sys

CONNECTIONS_DIR = "/var/run/rmtadm/"

def connect(client_hostname):
    client_file = path.join(CONNECTIONS_DIR, client_hostname + ".client")

    with open(client_file) as client:
        info = json.loads(client.readline().strip())

    ssh = ["ssh", 
           "-p", info["port"], 
           "-o", "UserKnownHostsFile /dev/null",
           "-o", "StrictHostKeyChecking no",
           info["username"] + "@localhost"]

    subprocess.run(ssh, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def list():
    for conn_file in os.listdir(CONNECTIONS_DIR):
        with open(path.join(CONNECTIONS_DIR, conn_file)) as conn_file:
            info = json.loads(conn_file.read())
            print(f"{info['username']}@{info['hostname']} (available at localhost:{info['port']})")

