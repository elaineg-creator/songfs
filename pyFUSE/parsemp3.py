import os
import sys
from collections import defaultdict
from mutagen.mp3 import MP3

def generate_music_library(directory):
    music_library = defaultdict(lambda: defaultdict(list))
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                print("Scanning " + file_path)
                artist, album, song = get_mp3_metadata(os.path.normpath(file_path))
                if artist and album and song:
                    music_library[artist][album].append(song)
    print("FINISHED LIB SCAN!")
    return music_library

def get_mp3_metadata(file_path):
    try:
        audio = MP3(file_path)
        artist = audio['TPE1'].text[0] if 'TPE1' in audio else "Unknown Artist"
        album = audio['TALB'].text[0] if 'TALB' in audio else "Unknown Album"
        song = audio['TIT2'].text[0] if 'TIT2' in audio else "Unknown Song"
        return artist, album, song
    except Exception as e:
        print("Error:", e)
        print(file_path)
        return None, None, None

# Test function/visual of tree
def print_music_library(library):
    for artist, albums in library.items():
        print(artist)
        for album, songs in albums.items():
            print("  |-", album)
            for song in songs:
                print("     |-", song)

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python program.py <directory>")
#         sys.exit(1)
    
#     directory = sys.argv[1]
#     if not os.path.isdir(directory):
#         print("Error: Invalid directory path")
#         sys.exit(1)

#     music_library = generate_music_library(directory)
#     print_music_library(music_library)
