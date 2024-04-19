import os
import sys
from collections import defaultdict
from mutagen.mp3 import MP3

def generate_music_library(directory):
    music_library = defaultdict(lambda: defaultdict(list))
    song_to_path = defaultdict(lambda: defaultdict(list))
    seen_names = defaultdict(lambda: int)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
                new_song = True
                file_path = os.path.join(root, file)
                artist, album, song = get_mp3_metadata(os.path.normpath(file_path))
                if song in seen_names:
                    new_song = False
                    seen_names[song] += 1
                else:
                    seen_names[song] = 1
                if artist and album and song:
                    if song == "Unknown Song":
                        if new_song:
                            song_title = file
                        else:
                            filename, _ = os.path.splitext(os.path.basename(file_path))
                            song_title = filename + " " + str(seen_names[song]) + ".mp3"
                    else:
                        if new_song:
                            song_title = song + ".mp3"
                        else:
                            song_title = song + " " + str(seen_names[song]) + ".mp3"
                    music_library[artist][album].append(song_title)
                    song_to_path[song_title] = os.path.abspath(file_path)
                elif artist is None and album is None:
                    # Check if a dup file name exists in directory
                    # if it does, then add a number to the end to distinguish it
                    song_title = song
                    if new_song:
                        music_library["Excluded"]["Songs"].append(song)
                    else:
                        filename, _ = os.path.splitext(os.path.basename(file_path))
                        song_title = filename + " " + str(seen_names[song]) + ".mp3"
                        music_library["Excluded"]["Songs"].append(song_title)
                    song_to_path[song_title] = os.path.abspath(file_path)
                    # print(file_path)
    return [music_library, song_to_path]

def get_mp3_metadata(file_path): 
    # print("File path is: ", file_path)
    try:
        audio = MP3(file_path)
        # print("here")
        artist = audio['TPE1'].text[0] if 'TPE1' in audio else "Unknown Artist"
        album = audio['TALB'].text[0] if 'TALB' in audio else "Unknown Album"
        song = audio['TIT2'].text[0] if 'TIT2' in audio else "Unknown Song"
        return artist, album, song
    except Exception as e:
        print("Error:", e)
        return None, None, os.path.basename(file_path)

def print_music_library(library, song_to_path):
    for artist, albums in library.items():
        print(artist)
        for album, songs in albums.items():
            print("  |-", album)
            for song in songs:
                print("     |-", song)
                print("     |+", song_to_path[song])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python program.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print("Error: Invalid directory path")
        sys.exit(1)

    music_library = generate_music_library(directory)
    print_music_library(music_library)
