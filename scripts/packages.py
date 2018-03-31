#!/usr/bin/env python

import os
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
PACKAGE_GROUP_DIR = os.path.join(BASE_DIR, 'package-group')

def get_installed_packages():
    p = subprocess.run(['pacman', '-Qqe'],
                       stdout=subprocess.PIPE,
                       universal_newlines=True)
    installed_packages = set()
    for line in p.stdout.splitlines():
        installed_packages.add(line)
    return installed_packages

def add_packages_from_group(packages, group):
    p = subprocess.run(['pacman', '-Sg', group],
                       stdout=subprocess.PIPE,
                       universal_newlines=True)
    for line in p.stdout.splitlines():
        _, package = line.split(' ')
        packages.add(package)

def add_packages_from_file(packages, path):
    for line in open(path, 'r'):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        packages.add(s)

def add_packages_from_package_group(packages, group):
    add_packages_from_file(packages, os.path.join(PACKAGE_GROUP_DIR, group))

def check_packages(hostname):
    installed_packages = get_installed_packages()
    wanted_packages = set()
    add_packages_from_group(wanted_packages, 'base')
    add_packages_from_group(wanted_packages, 'base-devel')
    path = os.path.join(BASE_DIR, 'host-specific', hostname, 'package-group')
    with open(path, 'r') as f:
        for line in f:
            s = line.strip()
            if s.startswith('#'):
                continue
            add_packages_from_package_group(wanted_packages, s)
    missing_packages = wanted_packages - installed_packages
    unwanted_packages = installed_packages - wanted_packages
    if len(missing_packages) > 0:
        args = ['sudo', 'pacman', '-S'] + list(missing_packages)
        print(' '.join(args))
        subprocess.run(args)
    if len(unwanted_packages) > 0:
        args = ['sudo', 'pacman', '-Rs'] + list(unwanted_packages)
        print(' '.join(args))
        subprocess.run(args)

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

def main():
    hostname = get_hostname()
    check_packages(hostname)

if __name__ == '__main__':
    main()
