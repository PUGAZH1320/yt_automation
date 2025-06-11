import os
from pytube import YouTube
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# where to save
SAVE_PATH = "H:\\YOUTUBE_AUTOMATION\\videos"  # to_do

# link of the video to be downloaded
# opening the file
link = open('links.txt', 'r')

for i in link:
    try:
        # object creation using YouTube
        yt = YouTube(i)
        print(yt.title)

        # filters out all the files with "mp4" extension
        mp4files = yt.streams.get_highest_resolution()

        # get the video with the extension and
        # resolution passed in the get() function
        # d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)

        # downloading the video
        mp4files.download(SAVE_PATH) 

    except Exception as e:
        # to handle exception
        print(f"Error downloading video: {e}")

# close the file
link.close()
print('Downloading Process Completed!')

# Renaming process

# Function to rename multiple files


def main():

    folder = "H:\\YOUTUBE_AUTOMATION\\videos"
    for count, filename in enumerate(os.listdir(folder)):
        dst = f"vid{str(count+1)}.mp4"
        # foldername/filename, if .py file is outside folder
        src = f"{folder}/{filename}"
        dst = f"{folder}/{dst}"

        # rename() function will
        # rename all the files
        os.rename(src, dst)


# Driver Code
if __name__ == '__main__':

    # Calling main() function
    main()
print('Renaming Process Completed!')

#### upload script #######
options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
options.add_argument("user-data-dir=C:\\Users\\EMPTY\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
print("\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in the bot directory. Please make sure to name the video files like this --> Ex: vid1.mp4 vid2.mp4 vid3.mp4 etc..")
time.sleep(6)

print("\033[1;31;40m IMPORTANT: Please make sure the name of the videos are like this: vid1.mp4, vid2.mp4, vid3.mp4 ...  etc")
dir_path = '.\\videos'
count = 0

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
print("   ", count, " Videos found in the videos folder, ready to upload...")
time.sleep(6)

for i in range(count):
    bot = webdriver.Chrome(
        executable_path="chromedriver.exe", chrome_options=options)

    bot.get("https://studio.youtube.com")
    time.sleep(3)
    upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
    upload_button.click()
    time.sleep(1)

    file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
    simp_path = 'videos/vid{}.mp4'.format(str(i+1))
    abs_path = os.path.abspath(simp_path)

    file_input.send_keys(abs_path)

    time.sleep(7)

    next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
    for i in range(3):
        next_button.click()
        time.sleep(1.5)

    done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
    done_button.click()
    time.sleep(30)
    bot.quit()
print('Uploading Process Completed!')


#remove process

directory = "H:\\YOUTUBE_AUTOMATION\\videos"

files_in_directory = os.listdir(directory)
print(files_in_directory)
filtered_files = [file for file in files_in_directory if file.endswith(".mp4")]

for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)

print('Remove Process Completed!')


