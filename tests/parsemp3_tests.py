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
        self.assertEqual(list(song_dict), ['john s', 'Unknown Artist', 'Taylor Swift'])
        print(song_dict["Taylor Swift"])
        self.assertEqual(song_dict["john s"], {'Unknown Album': ['always with me always with you']})
        self.assertEqual(song_dict["Unknown Artist"], {'one': ['happy summer long']})
        self.assertEqual(song_dict["Taylor Swift"], {'1989': ['Bad Blood', 'Unknown Song'], 'Midnights': ["You're Losing Me"]})
        self.assertEqual(song_path_dict["always with me always with you"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/always-with-me-always-with-you-long-21256.mp3").replace('/','\\'))
        self.assertEqual(song_path_dict["Unknown Song"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/Taylor Swift - Is It Over Now_ (Taylor's Version) (From The Vault) (Lyric Video) (64 kbps).mp3").replace('/','\\'))
    

if __name__ == '__main__':
    # Run the tests
    unittest.main(argv=sys.argv)
