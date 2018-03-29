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

def check_packages():
    pass

def main():
    installed_packages = get_installed_packages()
    wanted_packages = set()
    add_packages_from_group(wanted_packages, 'base')
    add_packages_from_group(wanted_packages, 'base-devel')
    add_packages_from_package_group(wanted_packages, 'android')
    add_packages_from_package_group(wanted_packages, 'audio')
    add_packages_from_package_group(wanted_packages, 'bluetooth')
    add_packages_from_package_group(wanted_packages, 'development')
    add_packages_from_package_group(wanted_packages, 'intel')
    add_packages_from_package_group(wanted_packages, 'laptop')
    add_packages_from_package_group(wanted_packages, 'latex')
    add_packages_from_package_group(wanted_packages, 'shell')
    add_packages_from_package_group(wanted_packages, 'wayland')
    add_packages_from_package_group(wanted_packages, 'wifi')
    add_packages_from_package_group(wanted_packages, 'x11')
    add_packages_from_package_group(wanted_packages, 'x11-audio')
    add_packages_from_package_group(wanted_packages, 'x11-intel')
    missing_packages = wanted_packages - installed_packages
    unwanted_packages = installed_packages - wanted_packages
    if len(missing_packages) > 0:
        print('\033[1;33m{} missing package{}\033[0m'.format(
            len(missing_packages), 's' if len(missing_packages) > 1 else ''))
        subprocess.run(['sudo', 'pacman', '-S'] + list(missing_packages))
    if len(unwanted_packages) > 0:
        print('\033[1;33m{} unwanted package{}\033[0m'.format(
            len(unwanted_packages), 's' if len(unwanted_packages) > 1 else ''))
        subprocess.run(['sudo', 'pacman', '-Rs'] + list(unwanted_packages))

if __name__ == '__main__':
    main()

# os.uname().nodename
# installed packages
# configuration files
# by use... bluetooth email
