import instaloader
import os
import hashlib
import datetime
import os
from pytube import YouTube
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def download_instagram_video(url):
    loader = instaloader.Instaloader()

    try:
        post = instaloader.Post.from_shortcode(loader.context, url.rsplit("/", 2)[-2])

        target_dir = "instavideos"
        os.makedirs(target_dir, exist_ok=True)
        loader.download_post(post, target=target_dir)
        for filename in os.listdir(target_dir):
            if filename.startswith(str(post.mediaid)):
                _, ext = os.path.splitext(filename)
                unique_filename = (
                    datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    + "_"
                    + hashlib.md5(url.encode()).hexdigest()
                    + ext
                )
                os.rename(
                    os.path.join(target_dir, filename),
                    os.path.join(target_dir, unique_filename),
                )

        print("Video downloaded successfully!")

        source_dir = target_dir
        destination_dir = "instagramvideos"
        os.makedirs(destination_dir, exist_ok=True)
        for filename in os.listdir(source_dir):
            if filename.endswith(".mp4"):
                source_file = os.path.join(source_dir, filename)
                destination_file = os.path.join(destination_dir, filename)
                if not os.path.exists(destination_file):
                    os.rename(source_file, destination_file)
                else:
                    print(
                        f"Skipping file {filename} as it already exists in the destination folder."
                    )

        print("Videos moved successfully!")
    except instaloader.exceptions.InstaloaderException as e:
        print(f"An error occurred: {e}")


def download_videos_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            url = line.strip()
            download_instagram_video(url)


# Example usage
file_path = "links.txt"
download_videos_from_file(file_path)


def main():
    folder = "G:\\YOUTUBE_AUTOMATION\\instagramvideos"
    for count, filename in enumerate(os.listdir(folder)):
        dst = f"vid{str(count+1)}.mp4"
        src = f"{folder}/{filename}"
        dst = f"{folder}/{dst}"
        os.rename(src, dst)


if __name__ == "__main__":
    main()
print("Renaming Process Completed!")


#### upload script #######
options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
options.add_argument(
    "user-data-dir=C:\\Users\\EMPTY\\AppData\\Local\\Google\\Chrome Beta\\User Data\\"
)
options.binary_location = (
    "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
)
print(
    "\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in the bot directory. Please make sure to name the video files like this --> Ex: vid1.mp4 vid2.mp4 vid3.mp4 etc.."
)
time.sleep(6)

print(
    "\033[1;31;40m IMPORTANT: Please make sure the name of the videos are like this: vid1.mp4, vid2.mp4, vid3.mp4 ...  etc"
)
dir_path = ".\\instagramvideos"
count = 0

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
print("   ", count, " Videos found in the videos folder, ready to upload...")
time.sleep(6)

for i in range(count):
    service = Service("chromedriver.exe")
    bot = webdriver.Chrome(service=service, options=options)

    bot.get("https://studio.youtube.com")
    time.sleep(3)
    upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
    upload_button.click()
    time.sleep(1)

    file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
    simp_path = "instagramvideos/vid{}.mp4".format(str(i + 1))
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
print("Uploading Process Completed!")


# remove process

directory = "G:\\YOUTUBE_AUTOMATION\\instagramvideos"

files_in_directory = os.listdir(directory)
print(files_in_directory)
filtered_files = [file for file in files_in_directory if file.endswith(".mp4")]

for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)

print("Remove Process Completed!")

def delete_files_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)

        for file in files:
            file_path = os.path.join(folder_path, file)

            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"Skipping subdirectory: {file_path}")

        print("Deletion completed.")
    except Exception as e:
        print(f"An error occurred: {e}")


folder_path_to_delete_from = "instavideos"
delete_files_in_folder(folder_path_to_delete_from)
