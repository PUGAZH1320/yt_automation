from pytube import YouTube

# Enter the URL of the YouTube video you want to download
video_url = "https://www.youtube.com/shorts/oq9wYwLi_m0"

# Create a YouTube object with the video URL
yt = YouTube(video_url)

# Select the highest resolution video (or another format if you prefer)
video = yt.streams.get_highest_resolution()

# Download the video to the current working directory
video.download()
