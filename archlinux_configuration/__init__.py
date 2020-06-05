#!/usr/bin/env python

from .configs import check_configs
from .packages import check_packages
from .repos import check_repos

from .constants import BASE_DIR

import os
import subprocess

def get_hostname():
    path = '/etc/hostname'
    try:
        contents = open(path, 'r').read()
    except FileNotFoundError:
        print('\033[31m{} not found\033[0m'.format(path))
        exit(1)
    if contents[-1] != '\n':
        print('\033[31m{} missing newline\033[0m'.format(path))
        exit(1)
    return contents[:-1]

def get_version():
    p = subprocess.run([os.path.join(BASE_DIR, 'version.sh')],
                       check=True,
                       stdout=subprocess.PIPE,
                       text=True)
    return p.stdout.strip()

def main(args):
    hostname = get_hostname()
    title = '\033[1;34mArch Linux Configuration\033[0m \033[36m{}\033[0m'
    version = get_version()
    print(title.format(version))
    check_packages(hostname)
    check_configs(hostname)
    check_repos()

if __name__ == '__main__':
    main()
