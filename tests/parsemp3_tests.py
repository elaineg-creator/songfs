# Unit tests for parsemp3.py

import unittest
import sys
import os


# Import the script you want to test
sys.path.append('../songfs')
import parsemp3

class TestScript(unittest.TestCase):
    
    def test_get_dictionary(self):
        # Test cases for function1
        path = os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs").replace('\\','/')
        song_dict, song_path_dict = parsemp3.generate_music_library(path);
        self.assertListEqual(sorted(list(song_dict)), sorted(['john s', 'Unknown Artist', 'Taylor Swift']))
        #print(song_dict["Taylor Swift"])
        self.assertDictEqual(song_dict["john s"], {'Unknown Album': ['always with me always with you.mp3']})
        self.assertDictEqual(song_dict["Unknown Artist"], {'one': ['happy summer long.mp3']})
        self.assertDictEqual(song_dict["Taylor Swift"], {'1989': ["Taylor Swift - Is It Over Now_ (Taylor's Version) (From The Vault) (Lyric Video) (64 kbps).mp3", 'Bad Blood.mp3'], 'Midnights': ["You're Losing Me.mp3"]})

if __name__ == '__main__':
    # Run the tests
    unittest.main(argv=sys.argv)
