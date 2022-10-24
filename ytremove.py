import os
directory = "G:\\YOUTUBE_AUTOMATION\\videos"

files_in_directory = os.listdir(directory)
print(files_in_directory)
filtered_files = [file for file in files_in_directory if file.endswith(".mp4")]

for file in filtered_files:
	path_to_file = os.path.join(directory, file)
	os.remove(path_to_file)

print('Remove Process Completed!') 