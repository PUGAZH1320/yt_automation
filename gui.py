import instaloader
import os
import hashlib
import datetime
import time
import shutil
from pathlib import Path
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def download_videos_from_file(file_path):
    loader = instaloader.Instaloader()

    with open(file_path, "r") as file:
        for url in file:
            url = url.strip()
            if not url:
                continue
            try:
                post = instaloader.Post.from_shortcode(
                    loader.context, url.rsplit("/", 2)[-2]
                )

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

                print(f"Video downloaded successfully: {url}")

                # Move to final destination
                destination_dir = "instagramvideos"
                os.makedirs(destination_dir, exist_ok=True)
                for filename in os.listdir(target_dir):
                    if filename.endswith(".mp4"):
                        source_file = os.path.join(target_dir, filename)
                        destination_file = os.path.join(destination_dir, filename)
                        if not os.path.exists(destination_file):
                            os.rename(source_file, destination_file)
                        else:
                            print(
                                f"Skipping file {filename} as it already exists in the destination folder."
                            )

                print(f"Video moved successfully: {url}")

            except Exception as e:
                print(f"Error processing {url}: {e}")


def rename_videos(folder):
    folder_path = Path(folder)
    for file in folder_path.glob("*.mp4"):
        hash_val = hashlib.md5(file.name.encode()).hexdigest()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{timestamp}_{hash_val}.mp4"
        file.rename(folder_path / new_name)
        print(f"Renamed: {file.name} → {new_name}")


def move_videos(source_folder, destination_folder):
    src = Path(source_folder)
    dst = Path(destination_folder)
    dst.mkdir(exist_ok=True)

    for file in src.glob("*.mp4"):
        shutil.move(str(file), dst / file.name)
        print(f"Moved: {file.name}")


def upload_videos_to_youtube(video_folder):
    video_folder = Path(video_folder)
    videos = sorted(video_folder.glob("*.mp4"))

    for idx, video in enumerate(videos):
        print(f"Uploading {video.name}...")

        service = Service("chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-data-dir=C:\\Users\\EMPTY\\AppData\\Local\\Google\\Chrome Beta\\User Data"
        )
        options.binary_location = (
            "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
        )

        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get("https://studio.youtube.com")
            time.sleep(6)

            driver.find_element(By.ID, "upload-icon").click()
            time.sleep(3)

            # Use pyautogui to interact with file dialog
            abs_path = str(video.resolve())
            pyautogui.write(abs_path)
            pyautogui.press("enter")
            time.sleep(10)

            for _ in range(3):
                next_btn = driver.find_element(By.ID, "next-button")
                next_btn.click()
                time.sleep(2)

            driver.find_element(By.ID, "done-button").click()
            time.sleep(20)

            print(f"Uploaded: {video.name}")

        except Exception as e:
            print(f"Upload failed for {video.name}: {e}")
        finally:
            driver.quit()


def clean_folders(folders):
    for folder in folders:
        path = Path(folder)
        if path.exists():
            for file in path.glob("*.*"):
                try:
                    file.unlink()
                    print(f"Deleted: {file.name}")
                except Exception as e:
                    print(f"Error deleting {file.name}: {e}")


if __name__ == "__main__":
    print("Starting Instagram Video Automation...")

    # Step 1: Download and Move
    download_videos_from_file("links.txt")

    # Step 2: Upload to YouTube
    upload_videos_to_youtube("instagramvideos")

    # Step 3: Clean up
    clean_folders(["instavideos", "instagramvideos"])

    print("✅ All operations completed successfully!")
