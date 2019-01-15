#!/usr/bin/env python2

import subprocess

NAMETRANS_UWATERLOO_PAIRS = [
    ('INBOX.Drafts', 'drafts'),
    ('INBOX', 'inbox'),
    ('INBOX.Sent', 'sent'),
    ('INBOX.SPAM', 'spam'),
    ('INBOX.Trash', 'trash')
]

def get_password(name):
    return subprocess.check_output(['pass', 'show', name]).splitlines()[0]

def nametrans_uwaterloo_local(name):
    for remote, local in NAMETRANS_UWATERLOO_PAIRS:
        if name == local:
            return remote
    return name

def nametrans_uwaterloo_remote(name):
    for remote, local in NAMETRANS_UWATERLOO_PAIRS:
        if name == remote:
            return local
    return name
