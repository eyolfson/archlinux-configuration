#!/usr/bin/env python

from .configs import check_configs
from .packages import check_packages
from .repos import check_repos

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

def main(args):
    hostname = get_hostname()
    check_packages(hostname)
    check_configs(hostname)
    check_repos()

if __name__ == '__main__':
    main()
