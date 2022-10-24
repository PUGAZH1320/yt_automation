import os
from pytube import YouTube 
  
# where to save 
SAVE_PATH = "G:\\YOUTUBE_AUTOMATION\\videos" #to_do 
  
# link of the video to be downloaded 
# opening the file 
link=open('links.txt','r') 
  
for i in link: 
    try: 
          
        # object creation using YouTube
        # which was imported in the beginning 
        yt = YouTube(i) 
    except: 
          
        #to handle exception
        print("Connection Error")  
      
    #filters out all the files with "mp4" extension 
    mp4files = yt.streams.get_highest_resolution() 
      
    # get the video with the extension and
    # resolution passed in the get() function 
    # d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution) 
    try: 
          
        # downloading the video 
        mp4files.download(SAVE_PATH) 
    except: 
        print("Some Error!") 
print('Downloading Process Completed!') 

####Renaming process 
# Function to rename multiple files
def main():

	folder = "G:\\YOUTUBE_AUTOMATION\\videos"
	for count, filename in enumerate(os.listdir(folder)):
		dst = f"vid{str(count+1)}.mp4"
		src =f"{folder}/{filename}" # foldername/filename, if .py file is outside folder
		dst =f"{folder}/{dst}"
		
		# rename() function will
		# rename all the files
		os.rename(src, dst)

# Driver Code
if __name__ == '__main__':
	
	# Calling main() function
	main()
print('Renaming Process Completed!') 