#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import stat

from fuse import FUSE, FuseOSError, Operations
from parsemp3 import generate_music_library, print_music_library

#S_IFDIR = 16384

class Passthrough(Operations):
    def __init__(self, root):
        self.root = root
        self.music_library = generate_music_library(root)
        print_music_library(self.music_library)

    # Helper method to get full path
    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Override readdir to list directories and files corresponding to artists, albums, and songs
    def readdir(self, path, fh):
        full_path = self._full_path(path)
        dirents = ['.', '..']
        
        if path == '/':  # Root directory - list artists
            dirents.extend(self.music_library.keys())
        elif path.startswith('/artist'):
            artist = path.split('/')[2]
            if artist in self.music_library:
                dirents.extend(self.music_library[artist].keys())
        elif path.startswith('/artist/album'):
            artist, album = path.split('/')[2:]
            if artist in self.music_library and album in self.music_library[artist]:
                dirents.extend(self.music_library[artist][album])
        
        for r in dirents:
            yield r

    # Override getattr to provide metadata for directories and files
    def getattr(self, path, fh=None):
        full_path = self._full_path(path)

        # Default metadata for directories
        st = os.lstat(full_path)
        attrs = {
            'st_atime': st.st_atime,
            'st_ctime': st.st_ctime,
            'st_gid': st.st_gid,
            'st_mode': st.st_mode,
            'st_mtime': st.st_mtime,
            'st_nlink': st.st_nlink,
            'st_size': st.st_size,
            'st_uid': st.st_uid
        }

        if path == '/':
            return attrs
        
        # Override metadata for directories and files corresponding to artists, albums, and songs
        parts = path.strip('/').split('/')
        if len(parts) == 1:  # Artist directory
            if parts[0] in self.music_library:
                attrs['st_mode'] = stat.S_IFDIR | 0o755 #(st.st_mode | 0o111) if attrs['st_mode'] & 0o111 else st.st_mode
                return attrs
        elif len(parts) == 2:  # Album directory
            artist, album = parts
            if artist in self.music_library and album in self.music_library[artist]:
                attrs['st_mode'] = stat.S_IFDIR | 0o755 #(st.st_mode | 0o111) if attrs['st_mode'] & 0o111 else st.st_mode
                return attrs
        elif len(parts) == 3:  # Song file
            artist, album, song = parts
            if artist in self.music_library and album in self.music_library[artist] and song in self.music_library[artist][album]:
                attrs['st_mode'] = stat.S_IFREG | 0o644 #1024  # Set size to non-zero to mark it as a file
                return attrs

        raise FuseOSError(errno.ENOENT)

def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
