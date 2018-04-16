import constants

import os
import pathlib

COMMON_DIR = os.path.join(constants.BASE_DIR, 'common')

def get_filesystem_abspath(relpath):
    p = pathlib.PurePath(relpath)
    for i, part in enumerate(p.parts):
        if i == 0:
            if part == 'home':
                abspath = pathlib.Path.home()
                is_home = True
            else:
                abspath = '/{}'.format(part)
                is_home = False
        elif i == 1 and is_home:
            abspath = os.path.join(abspath, '.{}'.format(part))
        else:
            abspath = os.path.join(abspath, part)
    return abspath

def check_file(package_dir, path):
    relpath = os.path.relpath(path, start=package_dir)
    abspath = get_filesystem_abspath(relpath)
    with open(path, 'r') as repo, open(abspath, 'r') as current:
        if repo.read() != current.read():
            print(abspath)

def check_configs_for_package(package_dir):
    for root, dirs, files in os.walk(package_dir):
        for f in files:
            check_file(package_dir, os.path.join(root, f))

def check_configs(hostname):
    for name in os.listdir(COMMON_DIR):
        check_configs_for_package(os.path.join(COMMON_DIR, name))
    host_dir = os.path.join(constants.HOST_SPECIFIC_DIR, hostname)
    for name in os.listdir(host_dir):
        if name == 'package-group':
            continue
        check_configs_for_package(os.path.join(host_dir, name))
