#TODO refactor the code and the libraries

import os
import time
import logging
import shutil
from sys import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#os.scandir() - Returns an iterator of all the objects in directory including file attribute information
#os.listdir() - Returns a list oof all files and folders iin a directory
#os.path.expanduser('~') - Finds the path of the current User
#watchdog - Allows you to listen for changes

### We check which platform the user using:
# macOS
if platform == 'darwin':
    print("You are using MAC")
    source_dir = os.path.expanduser('~') + '/Downloads'
    dest_dir_music = os.path.expanduser('~') + '/Music'
    dest_dir_video = os.path.expanduser('~') + '/Movies'
    dest_dir_image = os.path.expanduser('~') + '/Pictures'
    dest_dir_docs = os.path.expanduser('~') + '/Documents'  
# Linux
elif platform == 'linux' or platform == 'linux2':
    print("You are using Linux")
    source_dir = os.path.expanduser('~') + '/Downloads'
    dest_dir_music = os.path.expanduser('~') + '/Music'
    dest_dir_video = os.path.expanduser('~') + '/Videos'
    dest_dir_image = os.path.expanduser('~') + '/Pictures'
    dest_dir_docs = os.path.expanduser('~') + '/Documents' 
# Windows
elif platform == 'win32':
    print("You are using Windows")
    source_dir = os.path.expanduser('~') + '/Downloads'
    dest_dir_music = os.path.expanduser('~') + '/Music'
    dest_dir_video = os.path.expanduser('~') + '/Videos'
    dest_dir_image = os.path.expanduser('~') + '/Pictures'
    dest_dir_docs = os.path.expanduser('~') + '/Documents'
 
# Image file types
img_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# Video file types
vid_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# Audio file types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# Document file types
doc_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]   


def makeUnique(dest, name):
    filename, extension = os.path.splitext(name)
    cnt = 1
    # If the file exists then add a number to the end of the filename.
    while os.path.exists(name):
        name = filename + " (" + str(cnt) + ")" + extension
        cnt += 1
    return name

def move(dest, entry, name):
    # # Check if the file (filepath) exists
    if os.path.exists(dest + '/' + name):
        unique_name = makeUnique(dest, name)
        old_name = os.path.join(dest, name)
        new_name = os.path.join(dest, unique_name)
        os.rename(old_name, new_name) # (before, after)
    shutil.move(entry, dest)

# The class runs whenever there is a change in source_dir
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        #entries - All the files in the folder
        with os.scandir(source_dir) as entries:
            for entry in entries: #this line runs for each object in the list of all entries
                #print(entry.name)
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_document_files(entry, name)
                self.check_image_files(entry, name)
    
    # Check all audio files            
    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                dest = dest_dir_music
                move(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    # Check all video files
    def check_video_files(self, entry, name):
        for vid_extension in vid_extensions:
            if name.endswith(vid_extension) or name.endswith(vid_extension.upper()):
                dest = dest_dir_video
                move(dest, entry, name)
                logging.info(f"Moved video file: {name}")
    
    # Check all document files           
    def check_document_files(self, entry, name):
        for doc_extension in doc_extensions:
            if name.endswith(doc_extension) or name.endswith(doc_extension.upper()):
                dest = dest_dir_docs
                move(dest, entry, name)
                logging.info(f"Moved document file: {name}")
      
    # Check all image files          
    def check_image_files(self, entry, name):
        for img_extension in img_extensions:
            if name.endswith(img_extension) or name.endswith(img_extension.upper()):
                dest = dest_dir_image
                move(dest, entry, name)
                logging.info(f"Moved image file: {name}")
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
        
        
        
        

