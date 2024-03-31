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
import pyinotify
import functools

from fuse import FUSE, FuseOSError, Operations
from parsemp3 import generate_music_library, print_music_library

#S_IFDIR = 16384

# Function that is run when files are deleted or created in root
def on_loop(notifier, songfs):
    songfs.music_library, songfs.song_to_path = generate_music_library(songfs.root) 

class SongFS(Operations):
    def __init__(self, root):
        self.root = root
        self.music_library, self.song_to_path = generate_music_library(root) # Make dict of mp3s
        
        # Create pyinotify objects
        wm = pyinotify.WatchManager()  # Watch Manager
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
        on_loop_func = functools.partial(on_loop, songfs=self)
        notifier = pyinotify.ThreadedNotifier(wm, default_proc_fun=on_loop_func)
        wdd = wm.add_watch(os.getcwd() + "/" + sys.argv[1], mask, rec=True)
        notifier.start()
        #print_music_library(self.music_library) # print for sanity checks

    # get full path
    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # def readlink(self, path):
    #     # Spoof metadata for dirs and files corresponding to artists, albums, and songs
    #     parts = [i for i in path.split('/') if i != '']
    #     artist, album, song = parts
    #     if artist in self.music_library and album in self.music_library[artist] and song in self.music_library[artist][album]:
    #         pathname = self.song_to_path[song]
    #         if pathname.startswith("/"):
    #             # Path name is absolute, sanitize it.
    #             return os.path.relpath(pathname, self.root)
    #         else:
    #             return pathname
                
                
    #     return ''
        
        
    # Override readdir to list directories and files corresponding to artists, albums, and songs
    def readdir(self, path, fh):
        # full_path = self._full_path(path)
        dirents = ['.', '..']
        
        
        # Spoof metadata for dirs and files corresponding to artists, albums, and songs
        parts = [i for i in path.split('/') if i != '']
        

        print(parts)
        if parts == []:
            dirents.extend(self.music_library.keys())
            for r in dirents:
                yield r # return entries
            return
        
        if len(parts) == 0:  # Artist directory
            dirents.extend(self.music_library.keys())
        elif len(parts) == 1:  # Album directory
            artist = parts[0]
            if artist in self.music_library:
                dirents.extend(self.music_library[artist].keys())
        elif len(parts) == 2:  # Song file
            # print('Adding songs', file=sys.stderr)
            artist, album = parts
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
        # print("Dirlist: " + str(dirents), file=sys.stderr)

        for r in dirents:
            yield r # return entries

    # Override getattr to provide metadata for directories and files
    def getattr(self, path, fh=None):
        # full_path = self._full_path(path)

        # Default metadata for dirs
        # st = os.lstat(full_path)

        # attrs = dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
        #              'st_gid', 'st_mtime', 'st_uid', 'st_nlink'))
        
        # # Set the S_IFDIR flag to indicate that it's a directory
        # attrs['st_mode'] = stat.S_IFDIR | 0o755

        attrs = {}
        
        # Set the S_IFDIR flag to indicate that it's a directory
        attrs['st_ctime'] = attrs['st_atime'] = attrs['st_mtime'] = 0
        attrs['st_uid'] = attrs['st_gid'] = 0
        attrs['st_nlink'] = 1
        attrs['st_mode'] = stat.S_IFDIR | 0x777
        # attrs['st_ino'] = 1858
        # attrs['st_dev'] = 1858
        # attrs['st_size'] = 1858
        
        print(path)
        # Spoof metadata for dirs and files corresponding to artists, albums, and songs
        parts = [i for i in path.split('/') if i != '']
        

        print(parts)
        if parts == []:
            return attrs
        
        if len(parts) == 1:  # Artist directory
            print("Spoofing artist dir " + parts[0])
            if parts[0] in self.music_library:
                attrs['st_mode'] = stat.S_IFDIR | 0x777 #(st.st_mode | 0o111) if attrs['st_mode'] & 0o111 else st.st_mode
                return attrs
        elif len(parts) == 2:  # Album directory
            artist, album = parts
            if artist in self.music_library and album in self.music_library[artist]:
                attrs['st_mode'] = stat.S_IFDIR | 0x777 #(st.st_mode | 0o111) if attrs['st_mode'] & 0o111 else st.st_mode
                return attrs
        elif len(parts) == 3:  # Song file 
            artist, album, song = parts
            if artist in self.music_library and album in self.music_library[artist] and song in self.music_library[artist][album]:
                full_path = os.path.abspath(self.song_to_path[song])
                st = os.lstat(full_path)
                return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))     

        return attrs
        # raise FuseOSError(errno.ENOENT)

    def open(self, path, flags):
        print('tried to open')
        print(path)
        parts = [i for i in path.split('/') if i != '']
        artist, album, song = parts
        full_path = os.path.abspath(self.song_to_path[song])
        print(full_path)
        return os.open(full_path, flags)
    

    def read(self, path, length, offset, fh):
        print('tried to read')
        print(path)
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

def main(mountpoint, root):
    print("here")
    FUSE(SongFS(root), mountpoint, nothreads=True, foreground=True) # Pass through to default FUSE

if __name__ == '__main__':

    main(sys.argv[2], sys.argv[1])
