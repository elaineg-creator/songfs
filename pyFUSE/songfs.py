#!/usr/bin/env python
###########################################
#                                         #
#   Passthrough FUSE commands to Kernel   #
#                                         #
###########################################

# python songfs.py [dir to mount] [mountpoint]
# eg python3 songfs.py rootdir/ mountdir/
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
        self.music_library = generate_music_library(root) # Make dict of mp3s
        #print_music_library(self.music_library) # print for sanity checks

    # get full path
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
            print('Adding artists', file=sys.stderr)
            dirents.extend(self.music_library.keys())
        elif path.startswith('/artist'): # 1 level down, list albums for given artist
            print('Adding albums', file=sys.stderr)
            artist = path.split('/')[2]
            if artist in self.music_library:
                dirents.extend(self.music_library[artist].keys())
        elif path.startswith('/artist/album'): # 2 levels down, list songs
            print('Adding songs', file=sys.stderr)
            artist, album = path.split('/')[2:]
            if artist in self.music_library and album in self.music_library[artist]:
                dirents.extend(self.music_library[artist][album])
        
        # if path == '/':
        #     dirents.extend(self.music_library.keys())
        # else:
        #     # Check if the path corresponds to an artist directory
        #     parts = path.strip('/').split('/')
        #     if len(parts) == 1 and parts[0] in self.music_library:
        #         # List albums and songs under the artist directory
        #         print("Showing albums by " + parts[0])
        #         dirents.extend(self.music_library[parts[0]].keys())
        print("Dirlist: " + str(dirents), file=sys.stderr)

        for r in dirents:
            yield r # return entries

    # Override getattr to provide metadata for directories and files
    def getattr(self, path, fh=None):
        full_path = self._full_path(path)

        # Default metadata for dirs
        st = os.lstat(full_path)

        # attrs = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
        #              'st_gid', 'st_mtime', 'st_uid', 'st_nlink'))
        
        # # Set the S_IFDIR flag to indicate that it's a directory
        # attrs['st_mode'] = stat.S_IFDIR | 0o755

        attrs = {}
        
        # Set the S_IFDIR flag to indicate that it's a directory
        attrs['st_ctime'] = attrs['st_atime'] = attrs['st_mtime'] = 0
        attrs['st_uid'] = attrs['st_gid'] = 0
        attrs['st_nlink'] = 1
        attrs['st_mode'] = stat.S_IFDIR | 0o755
        
        return attrs
                 
        # attrs = {
        #     'st_atime': st.st_atime,
        #     'st_ctime': st.st_ctime,
        #     'st_gid': st.st_gid,
        #     'st_mode': stat.S_IFDIR | 0o755, #st.st_mode,
        #     'st_mtime': st.st_mtime,
        #     'st_nlink': st.st_nlink,
        #     'st_size': st.st_size,
        #     'st_uid': st.st_uid
        # }


        # if path == '/':
        #     return attrs
        
        # # Spoof metadata for dirs and files corresponding to artists, albums, and songs
        # parts = path.strip('/').split('/')
        # if len(parts) == 1:  # Artist directory
        #     print("Spoofing artist dir " + parts[0])
        #     if parts[0] in self.music_library:
        #         attrs['st_mode'] = stat.S_IFDIR | 0o755 #(st.st_mode | 0o111) if attrs['st_mode'] & 0o111 else st.st_mode
        #         return attrs
        # elif len(parts) == 2:  # Album directory
        #     artist, album = parts
        #     if artist in self.music_library and album in self.music_library[artist]:
        #         attrs['st_mode'] = stat.S_IFDIR | 0o755 #(st.st_mode | 0o111) if attrs['st_mode'] & 0o111 else st.st_mode
        #         return attrs
        # elif len(parts) == 3:  # Song file
        #     artist, album, song = parts
        #     if artist in self.music_library and album in self.music_library[artist] and song in self.music_library[artist][album]:
        #         attrs['st_mode'] = stat.S_IFREG | 0o644 #1024  # Set size to non-zero to mark it as a file
        #         return attrs

        # raise FuseOSError(errno.ENOENT)

def main(mountpoint, root):
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True) # Pass through to default FUSE

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
