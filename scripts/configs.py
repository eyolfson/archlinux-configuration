import constants

import os
import pathlib
import subprocess

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
    return (abspath, is_home)

def check_file(package_dir, path):
    relpath = os.path.relpath(path, start=package_dir)
    abspath, is_home = get_filesystem_abspath(relpath)
    if not os.path.exists(abspath):
        args = ['install', '-D', '-m', '644', '/dev/null', abspath]
        if is_home:
            subprocess.run(args, check=True)
        else:
            subprocess.run(['sudo'] + args, check=True)
    with open(path, 'r') as repo, open(abspath, 'r') as current:
        if repo.read() != current.read():
            print(abspath)

def check_configs_for_package(package_dir):
    package_name = os.path.basename(package_dir)
    p = subprocess.run(['pacman', '-Qi', package_name], capture_output=True)
    if p.returncode != 0:
        return
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
