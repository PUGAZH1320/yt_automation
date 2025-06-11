import os
import subprocess

# Function to download YouTube videos
def download_video(link, save_path):
    try:
        # Run youtube-dl command to download the video with verbose mode
        subprocess.run(["youtube-dl", "--verbose", "--output", os.path.join(save_path, "%(title)s.%(ext)s"), link], check=True)

    except subprocess.CalledProcessError as e:
        # Handle exception
        print(f"Error downloading video: {e}")

# Path of the file containing YouTube links
link_file = 'links.txt'

# Path to save the downloaded videos
save_path = "H:\\YOUTUBE_AUTOMATION\\videos"  # Modify the path accordingly

# Check if the save path exists, otherwise create it
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Open the link file
with open(link_file, 'r') as file:
    links = file.readlines()

# Download videos for each link
for link in links:
    link = link.strip()  # Remove leading/trailing whitespaces
    if link:
        download_video(link, save_path)

print('Downloading Process Completed!')
