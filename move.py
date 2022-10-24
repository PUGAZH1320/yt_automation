import os
 
source = 'G:\YOUTUBE_AUTOMATION\ytdownvid'
destination = 'G:\YOUTUBE_AUTOMATION\videos'
 
# gather all files
allfiles = os.listdir(source)
 
# iterate on all files to move them to destination folder
for f in allfiles:
    src_path = os.path.join(source, f)
    dst_path = os.path.join(destination, f)
    os.rename(src_path, dst_path)