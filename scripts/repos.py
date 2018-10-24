import os
import pathlib
import subprocess

SRC_DIRECTORY = os.path.join(
    pathlib.Path.home(),
    'src',
)

ORIGIN_URI_TEMPLATE = 'git@eyl.io:jon/{}'
GITHUB_URI_TEMPLATE = 'git@github.com:eyolfson/{}'
ECGIT_URI_TEMPLATE = 'git@ecgit.uwaterloo.ca:jeyolfso/{}'
BITBUCKET_URI_TEMPLATE = 'git@bitbucket.org:eyolfson/{}'

PUBLIC_REPOSITORIES = [
    'archlinux-configuration',
    'aur',
    'configuration',
    'configuration-check',
    'django-ssh',
    'eyl-desktop',
    'eyl-irc',
    'eyl-launcher',
    'eyl-nes-emulator',
    'eyl-software-development',
    'hack-assembler',
    'hello-vulkan',
    'llvm-static-analysis-examples',
    'matasano-challenge',
    'site-eyl',
    'site-eyl-blog',
    'the-big-book-of-computing',
]

PRIVATE_REPOSITORIES = [
    'eudyptula-challenge',
    'home-password-store',
    'notepad',
    'postdoc',
]

UCLA_REPOSITORIES = [
    'jdk8',
    'jdk8-corba',
    'jdk8-hotspot',
    'jdk8-jaxp',
    'jdk8-jaxws',
    'jdk8-jdk',
    'jdk8-langtools',
    'jdk8-nashorn',
    'mlopt',
]

UWATERLOO_REPOSITORIES = [
    'research-2016-ecoop-paper',
    '2017-empirical-static-const',  
    'clang-immutability-check',
    'django-cpp-doc',
    'immutability-experiments',
    'llvm-immutability-analysis',
    'phd-thesis',
]

EXTERNAL_REPOSITORIES = [
    ('Bear',
     'https://github.com/rizsotto/Bear',
     []),
    ('clang',
     'http://llvm.org/git/clang.git',
     []),
    ('clang-tools-extra',
     'http://llvm.org/git/clang-tools-extra.git',
     []),
    ('cores',
     'https://github.com/PaulStoffregen/cores.git',
     []),
    ('linux',
     'git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git',
     [('next',
       'git://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git')]),
    ('llvm',
     'http://llvm.org/git/llvm.git',
     []),
]

def clone(git_directory, uri):
    if not os.path.exists(git_directory):
        directory = os.path.dirname(git_directory)
        subprocess.run(["git", "clone", uri],
                       check=True,
                       cwd=directory)

def check_remote(git_directory, name, uri):
    p = subprocess.run(["git", "remote", "get-url", name],
                       cwd=git_directory,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       universal_newlines=True)
    if p.returncode == 0:
        current_uri = p.stdout.strip()
        if current_uri != uri:
            subprocess.run(["git", "remote", "set-url", name, uri],
                           check=True,
                           cwd=git_directory)
            print("\033[36mRemote '{}' changed\033[m".format(name))
    else:
        subprocess.run(["git", "remote", "add", name, uri],
                       check=True,
                       cwd=git_directory)
        print("\033[36mRemote '{}' added\033[m".format(name))

def check_repos():
    print("\033[1;34mPrivate Repositories\033[m")
    for repo_name in PRIVATE_REPOSITORIES:
        print("\033[1;36mRepository '{}'\033[m".format(repo_name))
        git_directory = os.path.join(SRC_DIRECTORY, "private", repo_name)
        origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
        clone(git_directory, origin_uri)
        check_remote(git_directory, "origin", origin_uri)

    print("\033[1;34mPublic Repositories\033[m")
    for repo_name in PUBLIC_REPOSITORIES:
        print("\033[1;36mRepository '{}'\033[m".format(repo_name))
        git_directory = os.path.join(SRC_DIRECTORY, "public", repo_name)
        origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
        github_uri = GITHUB_URI_TEMPLATE.format(repo_name)
        clone(git_directory, origin_uri)
        check_remote(git_directory, "origin", origin_uri)
        check_remote(git_directory, "github", github_uri)

    print("\033[1;34mUCLA Repositories\033[m")
    for repo_name in UCLA_REPOSITORIES:
        print("\033[1;36mRepository '{}'\033[m".format(repo_name))
        git_directory = os.path.join(SRC_DIRECTORY, "ucla", repo_name)
        origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
        bitbucket_uri = BITBUCKET_URI_TEMPLATE.format(repo_name)
        clone(git_directory, origin_uri)
        check_remote(git_directory, "origin", origin_uri)
        check_remote(git_directory, "bitbucket", bitbucket_uri)

    print("\033[1;34mUWaterloo Repositories\033[m")
    for repo_name in UWATERLOO_REPOSITORIES:
        print("\033[1;36mRepository '{}'\033[m".format(repo_name))
        git_directory = os.path.join(SRC_DIRECTORY, "uwaterloo", repo_name)
        origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
        ecgit_uri = ECGIT_URI_TEMPLATE.format(repo_name)
        clone(git_directory, origin_uri)
        check_remote(git_directory, "origin", origin_uri)
        check_remote(git_directory, "ecgit", ecgit_uri)

    print("\033[1;34mExternal Repositories\033[m")
    for entry in EXTERNAL_REPOSITORIES:
        repo_name, upstream_uri, external_remotes = entry
        print("\033[1;36mRepository '{}'\033[m".format(repo_name))
        git_directory = os.path.join(SRC_DIRECTORY, "external", repo_name)
        origin_uri = ORIGIN_URI_TEMPLATE.format(repo_name)
        clone(git_directory, origin_uri)
        check_remote(git_directory, "origin", origin_uri)
        check_remote(git_directory, "upstream", upstream_uri)
        for remote_name, remote_uri in external_remotes:
            check_remote(git_directory, remote_name, remote_uri)
