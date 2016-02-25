"""
This file contains utilities for other commands to use.

Copyright 2015 Fetch Robotics Inc.
Author: Alex Henning
"""

from argcomplete.completers import ChoicesCompleter
import subprocess


def ssh(user, host, command, password=None, fname=None):
    "Run the command on the remote host as the given user."

    userhost = user + "@" + host
    ssh_command = ["ssh", "-t", userhost, command]

    e_vars = None
    if password:
        ssh_command = ["sshpass", "-e"] + ssh_command
        e_vars = {"SSHPASS": password}

    pipe = open(fname + ".txt", 'w') if fname else None

    proc = subprocess.Popen(ssh_command, env=e_vars, stdout=pipe, stderr=pipe)
    proc.wait()
    if fname:
        pipe.close()
    return proc.returncode


# Arguments
robots = ["freight" + str(i) for i in range(9)] + \
         ["fetch" + str(i) for i in range(7)]
users = subprocess.check_output(["awk", "-F:", "{ print $1}", "/etc/passwd"]) \
                  .split()


def add_user(parser):
    arg = parser.add_argument("--user", action="store",
                              help="User account to use on robot")
    arg.completer = ChoicesCompleter(users)


def add_robot(parser):
    arg = parser.add_argument("--robot", action="store", help="Robot to use")
    arg.completer = ChoicesCompleter(robots)


def add_workspace(parser):
    parser.add_argument("--workspace", action="store",
                        help="Catkin worspace to use")
