import os

def find_missing_files(folder_path):
    # Get all files in the folder
    files = os.listdir(folder_path)
    
    # Extract numbers from file names that match the pattern
    numbers = []
    for file in files:
        if file.startswith("cropped_video") and file.endswith(".mp4"):
            try:
                # Split the filename on underscores and dots to extract the number
                parts = file.split("_")
                # print(parts)
                number_str = parts[2].split(".")[0]
                # print(number_str)
                num = int(number_str)
                numbers.append(num)
            except ValueError:
                continue
    
    # Find the missing numbers
    if numbers:
        numbers.sort()
        max_num = numbers[-1]
        all_numbers = set(range(1, max_num + 1))  # Start from 1
        missing_numbers = sorted(all_numbers - set(numbers))
        return missing_numbers
    else:
        return []

# Example usage
folder_path = "REELS"  # Replace with the path to your folder
missing_files = find_missing_files(folder_path)

if missing_files:
    print(f"Missing video numbers: {missing_files}")
else:
    print("No missing files found.")