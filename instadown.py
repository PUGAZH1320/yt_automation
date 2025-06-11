import instaloader
import os
import hashlib
import datetime

def download_instagram_video(url):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        post = instaloader.Post.from_shortcode(loader.context, url.rsplit('/', 2)[-2])

        target_dir = 'instavideos'
        os.makedirs(target_dir, exist_ok=True)  # Create the target directory if it doesn't exist

        loader.download_post(post, target=target_dir)  # Specify the target directory

        for filename in os.listdir(target_dir):
            if filename.startswith(str(post.mediaid)):
                _, ext = os.path.splitext(filename)
                unique_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + hashlib.md5(url.encode()).hexdigest() + ext
                os.rename(os.path.join(target_dir, filename), os.path.join(target_dir, unique_filename))

        print("Video downloaded successfully!")

        # Move .mp4 files to the 'instagramvideos' folder
        source_dir = target_dir
        destination_dir = 'instagramvideos'
        os.makedirs(destination_dir, exist_ok=True)  # Create the destination directory if it doesn't exist

        for filename in os.listdir(source_dir):
            if filename.endswith('.mp4'):
                source_file = os.path.join(source_dir, filename)
                destination_file = os.path.join(destination_dir, filename)
                if not os.path.exists(destination_file):
                    os.rename(source_file, destination_file)
                else:
                    print(f"Skipping file {filename} as it already exists in the destination folder.")

        print("Videos moved successfully!")
    except instaloader.exceptions.InstaloaderException as e:
        print(f"An error occurred: {e}")

def download_videos_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            download_instagram_video(url)

# Example usage
file_path = 'links.txt'
download_videos_from_file(file_path)
