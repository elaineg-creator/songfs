# Unit tests for parsemp3.py

import unittest
import sys
import os


# Import the script you want to test
sys.path.append('../pyFUSE')
import parsemp3

class TestScript(unittest.TestCase):
    
    def test_get_dictionary(self):
        # Test cases for function1
        path = os.path.normpath(os.getcwd() + "/../songfs/mp3_directory/parsemp3_test_songs").replace('\\','/')
        print(path)
        song_dict, song_path_dict = parsemp3.generate_music_library(path)
        parsemp3.print_music_library(song_dict, song_path_dict)
        sd_list = list(song_dict)
        sd_list.sort()
        self.assertEqual(sd_list,  ['Taylor Swift', 'Unknown Artist', 'john s'])
        print(song_dict["Taylor Swift"])
        
        self.assertEqual(song_dict["john s"], {'Unknown Album': ['always with me always with you.mp3']})
        self.assertEqual(song_dict["Unknown Artist"], {'one': ['happy summer long.mp3']})
        self.assertEqual(song_dict["Taylor Swift"], {'1989': ['Bad Blood.mp3', 'Taylor Swift - Is It Over Now_ (Taylor\'s Version) (From The Vault) (Lyric Video) (64 kbps).mp3'], 'Midnights': ["You're Losing Me.mp3"]})
        self.assertEqual(song_path_dict["always with me always with you.mp3"], os.path.normpath(os.getcwd() + "/../songfs/mp3_directory/parsemp3_test_songs/always-with-me-always-with-you-long-21256.mp3"))
        self.assertEqual(song_path_dict["Taylor Swift - Is It Over Now_ (Taylor's Version) (From The Vault) (Lyric Video) (64 kbps).mp3"], os.path.normpath(os.getcwd() + "/../songfs/mp3_directory/parsemp3_test_songs/Taylor Swift - Is It Over Now_ (Taylor's Version) (From The Vault) (Lyric Video) (64 kbps).mp3"))


if __name__ == '__main__':
    # Run the tests
    unittest.main(argv=sys.argv)
