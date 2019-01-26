import os

import xattr

from sys import platform

# Xattrs are namespaced on Linux under `user`, `trusted`, `security` and `system`.
# Mask this namespace from the user.
# https://en.wikipedia.org/wiki/Extended_file_attributes

def is_linux():
   return platform == 'linux' or platform == 'linux2'


def add_linux_prefix(key):
   return 'user.' + key


def rm_linux_prefix(key):
   return key[5:]


def set(filename, key, value=''):
    if is_linux():
        key = add_linux_prefix(key)
    xattr.setxattr(filename, bytes(key, 'utf-8'), bytes(value, 'utf-8'))


def get(filename):
    attrs = xattr.listxattr(filename)
    ret = []
    for attr in attrs:
        val = str(xattr.getxattr(filename, attr), 'utf-8')
        if is_linux():
            attr = rm_linux_prefix(attr)
        ret.append((attr, val))
    return ret


def rm(filename, key):
    if is_linux():
        key = add_linux_prefix(key)
    xattr.removexattr(filename, key)


def dir(foldername):
    dst_folder = 'marks'
    for root, dirs, files in os.walk(foldername, topdown=True):
        for name in files:
            make_link(root, name, dst_folder)


def make_link(root, filename, dst_folder):
    filepath = os.path.join(root, filename)
    original_filepath = os.path.join('..', '..', '..', filepath)
    for k, v in xattr.get_all(filepath):
        k = str(k, 'utf-8')
        v = str(v, 'utf-8')
        v_dir = os.path.join(dst_folder, k, v)
        os.makedirs(v_dir)

        new_filepath = os.path.join(v_dir, filename)
        os.symlink(original_filepath,  new_filepath)
