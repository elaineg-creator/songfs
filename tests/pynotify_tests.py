# Unit tests for pynotify_tests.py

import time
import unittest
import sys
import os
import subprocess

# Import the script you want to test
sys.path.append('../songfs')


import threading



def thread_function():

    os.system("python3 ../songfs.py ../mp3_directory/pynotify_test_songs/ test_mountpoint/")
    artist_dirs_list = [f for f in os.listdir(os.getcwd()+'/test_mountpoint') if os.path.isdir(f)]
    print('this is in thread')
    print(artist_dirs_list)


class TestScript(unittest.TestCase): 
    def __init__(self, *args, **kwargs):
        super(TestScript, self).__init__(*args, **kwargs)

    
    def test_initialize_mountpoint(self):

        
        # curr_dir = os.path.abspath('copyfs_1/tests')
        # Test cases for function1
        # os.chdir(curr_dir)
        print(os.getcwd())
        
        
        # x.join()
        print(os.getcwd()+'/test_mountpoint')
        time.sleep(2)

        
        artist_dirs_list = os.listdir(os.getcwd()+'/test_mountpoint')
        artist_dirs_list.sort()
        print(artist_dirs_list)
        self.assertEqual(artist_dirs_list, ['Taylor Swift', 'Unknown Artist', 'john s'])
        

    
    def test_add_mp3(self):

        
        # curr_dir = os.path.abspath('copyfs_1/tests')
        # Test cases for function1
        os.system("cp ../mp3_directory/Selena_slay.mp3 ../mp3_directory/pynotify_test_songs/Selena_slay.mp3")
        # os.chdir(curr_dir)
        print(os.getcwd())
        
        
        # x.join()
        print(os.getcwd()+'/test_mountpoint')
        time.sleep(2)

        
        artist_dirs_list = os.listdir(os.getcwd()+'/test_mountpoint')
        artist_dirs_list.sort()
        print(artist_dirs_list)
        self.assertEqual(artist_dirs_list, ['Selena', 'Taylor Swift', 'Unknown Artist', 'john s'])
    
        os.system("rm ../mp3_directory/pynotify_test_songs/Selena_slay.mp3")
        # self.assertEqual(song_dict["Unknown Artist"], {'one': ['happy summer long']})
        # self.assertEqual(song_dict["Taylor Swift"], {'1989': ['Bad Blood', 'Unknown Song'], 'Midnights': ["You're Losing Me"]})
        # self.assertEqual(song_path_dict["always with me always with you"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/always-with-me-always-with-you-long-21256.mp3").replace('/','\\'))
        # self.assertEqual(song_path_dict["Unknown Song"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/Taylor Swift - Is It Over Now_ (Taylor's Version) (From The Vault) (Lyric Video) (64 kbps).mp3").replace('/','\\'))
   
    def test_remove_mp3(self):

        
        # curr_dir = os.path.abspath('copyfs_1/tests')
        # Test cases for function1
        os.system("cp ../mp3_directory/pynotify_test_songs/always-with-me-always-with-you-long-21256.mp3 ../mp3_directory/always-with-me-always-with-you-long-21256.mp3")
        os.system("rm ../mp3_directory/pynotify_test_songs/always-with-me-always-with-you-long-21256.mp3")
        # os.chdir(curr_dir)
        print(os.getcwd())
        
        
        # x.join()
        print(os.getcwd()+'/test_mountpoint')
        time.sleep(2)

        
        artist_dirs_list = os.listdir(os.getcwd()+'/test_mountpoint')
        artist_dirs_list.sort()
        print(artist_dirs_list)
        self.assertEqual(artist_dirs_list, ['Taylor Swift', 'Unknown Artist'])

        
        
        os.system("cp ../mp3_directory/always-with-me-always-with-you-long-21256.mp3 ../mp3_directory/pynotify_test_songs/always-with-me-always-with-you-long-21256.mp3")
        # self.assertEqual(song_dict["Unknown Artist"], {'one': ['happy summer long']})
        # self.assertEqual(song_dict["Taylor Swift"], {'1989': ['Bad Blood', 'Unknown Song'], 'Midnights': ["You're Losing Me"]})
        # self.assertEqual(song_path_dict["always with me always with you"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/always-with-me-always-with-you-long-21256.mp3").replace('/','\\'))
        # self.assertEqual(song_path_dict["Unknown Song"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/Taylor Swift - Is It Over Now_ (Taylor's Version) (From The Vault) (Lyric Video) (64 kbps).mp3").replace('/','\\'))
    


    # def test_remove_song_from_artist(self):

        
    #     # curr_dir = os.path.abspath('copyfs_1/tests')
    #     # Test cases for function1
    #     os.system("cp ../mp3_directory/pynotify_test_songs/baddy_blood.mp3 ../mp3_directory/baddy_blood.mp3")
    #     os.system("rm ../mp3_directory/pynotify_test_songs/baddy_blood.mp3")
    #     # os.chdir(curr_dir)
    #     print(os.getcwd())
        
        
    #     # x.join()
    #     print(os.getcwd()+'/test_mountpoint')
    #     time.sleep(2)

        
    #     artist_dirs_list = os.listdir(os.getcwd()+'/test_mountpoint')
    #     artist_dirs_list.sort()
    #     print(artist_dirs_list)
    #     self.assertEqual(artist_dirs_list,  ['Taylor Swift', 'Unknown Artist'])
    
    #     os.system("cd Taylor\ Swift/1989/")
    #     artist_dirs_list = os.listdir(os.getcwd())
    #     artist_dirs_list.sort()
    #     print(os.getcwd())
    #     print(artist_dirs_list)
    #     self.assertEqual(artist_dirs_list, ['Taylor Swift', 'Unknown Artist', 'john s'])
        

        
        
    #     os.system("cp  ../mp3_directory/baddy_blood.mp3 ../mp3_directory/pynotify_test_songs/baddy_blood.mp3")
    #     # self.assertEqual(song_dict["Unknown Artist"], {'one': ['happy summer long']})
    #     # self.assertEqual(song_dict["Taylor Swift"], {'1989': ['Bad Blood', 'Unknown Song'], 'Midnights': ["You're Losing Me"]})
    #     # self.assertEqual(song_path_dict["always with me always with you"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/always-with-me-always-with-you-long-21256.mp3").replace('/','\\'))
    #     # self.assertEqual(song_path_dict["Unknown Song"], os.path.normpath(os.getcwd() + "/mp3_directory/parsemp3_test_songs/Taylor Swift - Is It Over Now_ (Taylor's Version) (From The Vault) (Lyric Video) (64 kbps).mp3").replace('/','\\'))
     


if __name__ == '__main__':
    # Run the tests
    x = threading.Thread(target=thread_function)
    x.start()

    unittest.main( exit=False)
