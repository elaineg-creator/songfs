# load the libraries that we'll use  
import mutagen
from mutagen.mp3 import MP3  
from os import listdir
  
import string    
import random # define the random module  
from os.path import isfile, join

S = 10  # number of characters in the string.  
 

onlyfiles = [join('very_big_random_library/', f) for f in listdir('very_big_random_library/') if isfile(join('very_big_random_library/', f))]


for file in onlyfiles:  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    random_album = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))   
    random_artist = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))   
    
    # turn it into an mp3 object using the mutagen library  
    try:
        mp3file = MP3(file)  
        # set the album name  
        mp3file['TPE1'] = mutagen.id3.TextFrame(encoding=3, text=[random_album])
        # set the albumartist name  
        mp3file['TALB'] = mutagen.id3.TextFrame(encoding=3, text=[random_artist])
        # save the changes that we've made  
        mp3file.save() 
    except Exception as e:
            print("Error:", e)