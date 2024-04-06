# Script to slowly copy a song over to rootdir to see whether or not it will sync correctly with inotify

import os
def copy_file_slowly(src_file, dest_file, chunk_size=1024, delay=0.1):
    with open(src_file, 'rb') as fsrc:
        with open(dest_file, 'wb') as fdest:
            while True:
                chunk = fsrc.read(chunk_size)
                print(os.path.getsize(dest_file))
                if not chunk:
                    break
                fdest.write(chunk)
                # Introduce a delay between chunks
                time.sleep(delay)

# Example usage
import time

source_file = 'Avatar - Theme Song.mp3'
destination_file = '../pyFUSE/rootdir/Avatar - Theme Song.mp3'

copy_file_slowly(source_file, destination_file, chunk_size=1024, delay=0.1)

print("Done copying!")
