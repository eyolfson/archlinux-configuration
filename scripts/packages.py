import constants

import os
import subprocess

PACKAGE_GROUP_DIR = os.path.join(constants.BASE_DIR, 'package-group')

def get_installed_packages():
    p = subprocess.run(['pacman', '-Qqe'],
                       check=True,
                       stdout=subprocess.PIPE,
                       universal_newlines=True)
    installed_packages = set()
    for line in p.stdout.splitlines():
        installed_packages.add(line)
    return installed_packages

def add_packages_from_group(packages, group):
    p = subprocess.run(['pacman', '-Sg', group],
                       check=True,
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

def add_unneeded_packages(packages):
    p = subprocess.run(['pacman', '-Qdtq'],
                       stdout=subprocess.PIPE,
                       universal_newlines=True)
    for line in p.stdout.splitlines():
        packages.add(line)

def check_packages(hostname):
    installed_packages = get_installed_packages()
    wanted_packages = set()
    add_packages_from_group(wanted_packages, 'base')
    add_packages_from_group(wanted_packages, 'base-devel')
    path = os.path.join(constants.HOST_SPECIFIC_DIR, hostname, 'package-group')
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
        subprocess.run(args, check=True)
    add_unneeded_packages(unwanted_packages)
    if len(unwanted_packages) > 0:
        args = ['sudo', 'pacman', '-Rs'] + list(unwanted_packages)
        print(' '.join(args))
        subprocess.run(args, check=True)
