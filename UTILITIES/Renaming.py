import os

# Specify the folder containing the files
folder_path = 'VIDEOS'

# List all files in the folder
files = os.listdir(folder_path)

# Loop through each file in the folder
for filename in files:
    # Check if the file name matches the pattern "reel_{number}.mp4"
    if filename.startswith("reel_") and filename.endswith(".mp4"):
        # Extract the number from the original file name
        number = filename.split('_')[1].split('.')[0]
        
        print("Number = ",number)
        print("Filename = ",filename)
        
        # Create the new file name using the same number
        new_name = f"Video_{number}.mp4"
        
        # Get the full path of the current file and the new file name
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_name)
        
        # Rename the file
        os.rename(old_file, new_file)

print("Files renamed successfully!")