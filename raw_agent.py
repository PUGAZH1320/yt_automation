import instaloader
import os
import hashlib
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            if url:  # Skip empty lines
                download_instagram_video(url)


def rename_videos():
    folder = "instagramvideos"
    if not os.path.exists(folder):
        os.makedirs(folder)

    for count, filename in enumerate(os.listdir(folder)):
        if filename.endswith(".mp4"):
            dst = f"vid{str(count+1)}.mp4"
            src = os.path.join(folder, filename)
            dst_path = os.path.join(folder, dst)
            os.rename(src, dst_path)


def setup_chrome_driver():
    """Setup Chrome driver with proper options to avoid common errors"""
    options = webdriver.ChromeOptions()

    # Add arguments to prevent common issues
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")
    options.add_argument("--disable-javascript")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--remote-debugging-port=9222")

    # Use a temporary user data directory instead of the default one
    temp_user_data = os.path.join(os.getcwd(), "temp_chrome_data")
    options.add_argument(f"--user-data-dir={temp_user_data}")

    # Alternative: Use your existing profile (uncomment if you want to use your logged-in Chrome)
    # options.add_argument("user-data-dir=C:\\Users\\EMPTY\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"

    return options


def upload_videos_to_youtube():
    """Upload videos to YouTube with improved error handling"""
    dir_path = "instagramvideos"

    if not os.path.exists(dir_path):
        print("No videos folder found!")
        return

    # Count video files
    video_files = [f for f in os.listdir(dir_path) if f.endswith(".mp4")]
    count = len(video_files)

    if count == 0:
        print("No video files found!")
        return

    print(f"Found {count} videos ready to upload...")
    time.sleep(3)

    for i in range(count):
        print(f"Uploading video {i+1}/{count}...")

        try:
            # Setup Chrome driver
            options = setup_chrome_driver()
            service = Service("chromedriver.exe")
            bot = webdriver.Chrome(service=service, options=options)

            # Set implicit wait
            bot.implicitly_wait(10)
            wait = WebDriverWait(bot, 20)

            # Navigate to YouTube Studio
            bot.get("https://studio.youtube.com")
            time.sleep(5)

            # Wait for and click upload button
            upload_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="upload-icon"]'))
            )
            upload_button.click()
            time.sleep(2)

            # Find and use file input
            file_input = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/input'))
            )

            video_path = os.path.abspath(f"instagramvideos/vid{i+1}.mp4")
            file_input.send_keys(video_path)
            time.sleep(10)

            # Click next button 3 times
            for j in range(3):
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="next-button"]'))
                    )
                    next_button.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"Error clicking next button {j+1}: {e}")
                    break

            # Click done button
            try:
                done_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="done-button"]'))
                )
                done_button.click()
                time.sleep(5)
                print(f"Video {i+1} uploaded successfully!")
            except Exception as e:
                print(f"Error clicking done button: {e}")

        except Exception as e:
            print(f"Error uploading video {i+1}: {e}")

        finally:
            try:
                bot.quit()
            except:
                pass
            time.sleep(5)  # Wait between uploads


def cleanup_files():
    """Clean up downloaded files"""
    directories_to_clean = ["instagramvideos", "instavideos"]

    for directory in directories_to_clean:
        if os.path.exists(directory):
            try:
                files = os.listdir(directory)
                for file in files:
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                print(f"Cleanup completed for {directory}")
            except Exception as e:
                print(f"Error cleaning {directory}: {e}")


def main():
    """Main function to run the entire process"""
    try:
        # Step 1: Download videos from Instagram
        print("Step 1: Downloading Instagram videos...")
        file_path = "links.txt"
        if os.path.exists(file_path):
            download_videos_from_file(file_path)
        else:
            print("links.txt not found. Please create it with Instagram URLs.")
            return

        # Step 2: Rename videos
        print("Step 2: Renaming videos...")
        rename_videos()
        print("Renaming completed!")

        # Step 3: Upload to YouTube
        print("Step 3: Uploading to YouTube...")
        upload_videos_to_youtube()
        print("Upload process completed!")

        # Step 4: Cleanup
        print("Step 4: Cleaning up files...")
        cleanup_files()
        print("All processes completed!")

    except Exception as e:
        print(f"An error occurred in main process: {e}")


if __name__ == "__main__":
    main()
