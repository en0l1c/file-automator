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

# We check which platform the user using:
if platform == 'darwin':
    print("You are using MAC")
    source_dir = os.path.expanduser('~') + '/Downloads'
    dest_dir_music = os.path.expanduser('~') + '/Music'
    dest_dir_video = os.path.expanduser('~') + '/Movies'
    dest_dir_image = os.path.expanduser('~') + '/Pictures'
    dest_dir_docs = os.path.expanduser('~') + '/Documents'
elif platform == 'linux' or platform == 'linux2':
    print("You are using Linux")
    source_dir = os.path.expanduser('~') + '/Downloads'
    dest_dir_music = os.path.expanduser('~') + '/Music'
    dest_dir_video = os.path.expanduser('~') + '/Videos'
    dest_dir_image = os.path.expanduser('~') + '/Pictures'
    dest_dir_docs = os.path.expanduser('~') + '/Documents'
elif platform == 'win32':
    print("You are using Windows")
    source_dir = os.path.expanduser('~') + '/Downloads'
    dest_dir_music = os.path.expanduser('~') + '/Music'
    dest_dir_video = os.path.expanduser('~') + '/Videos'
    dest_dir_image = os.path.expanduser('~') + '/Pictures'
    dest_dir_docs = os.path.expanduser('~') + '/Documents'
    
# with os.scandir(source_dir) as entries:
#     for entry in entries: #this line runs for each object in the list of all entries
#         print(entry.name)


def move(dest, entry, name):
    # # Check if the file (filepath) exists
    # file_exists = os.path.exists(dest + '/' + name)
    # # If that file already exists, then the name changed to a unique name
    # if file_exists:
    #     unique_name = makeUnique(name)
    #     os.ranme(entry, unique)
    shutil.move(entry,dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        #entries - All the files in the folder
        with os.scandir(source_dir) as entries:
            for entry in entries: #this line runs for each object in the list of all entries
                print(entry.name)
                name = entry.name
                dest = source_dir
                
                if name.endswith('.wav') or name.endswith('.mp3'):
                    #if entry.stat().st_size < 25000000 or "SFX" in name:
                    dest = dest_dir_music
                    move(dest, entry, name)
                    
                    print('success!')
                elif name.endswith('.mov') or name.endswith('.mp4') or name.endswith('.avi'):
                    dest = dest_dir_video
                    move(dest, entry, name)
                    
                    print('success!')

                elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png') or name.endswith('.psd') or name.endswith('.gif') or name.endswith('.svg') or name.endswith('.tiff'):
                    dest = dest_dir_image
                    move(dest, entry, name)
                    
                    print('success!')
                elif name.endswith('.pdf') or name.endswith('.doc') or name.endswith('.docx') or name.endswith('.epub'):
                    dest = dest_dir_docs
                    move(dest, entry, name)
                    
                    print('success!')

                
        
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
        
        
        
        

