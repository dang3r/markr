import os

import xattr

def set_mark(filename, key, value):
    xattr.set(filename, key, value)

def get_mark(filename):
    attrs = xattr.get_all(filename)
    for k, v in attrs:
        print('{} : {}'.format(str(k, 'utf-8'),str(v, 'utf-8')))

def rm_mark(filename, key):
    xattr.remove(filename, key)

def dir_mark(foldername):
    dst_folder = 'marks'
    for root, dirs, files in os.walk(foldername, topdown=True):
        for name in files:
            make_link(root, name, dst_folder)

def make_link(root, filename, dst_folder):
    filepath = os.path.join(root, filename)
    for k, v in xattr.get_all(filepath):
        k = str(k, 'utf-8')
        new_dir = os.path.join(dst_folder, k)
        os.makedirs(new_dir)

        new_filepath = os.path.join(new_dir, filename)
        os.symlink('../../' + filepath, new_filepath)
