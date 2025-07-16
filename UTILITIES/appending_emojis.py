import pandas as pd
import random

def add_random_emojis(input_csv, output_csv, column_name, emoji_list):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Check if column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the CSV file.")

    # Function to add random emojis
    def append_emoji(text):
        emojis_to_add = "".join(random.sample(emoji_list, random.randint(1, 1)))
        return f"{text} {emojis_to_add}"

    # Apply transformation
    df[column_name] = df[column_name].astype(str).apply(append_emoji)

    # Save to new CSV file
    df.to_csv(output_csv, index=False)

# Example usage
emoji_list = ["😮", "😲", "😱"]
input_csv = "VIDEO_EDITING/extracted_texts.csv"  # Original CSV file
output_csv = "VIDEO_EDITING/output_with_emojis.csv"  # New file
column_name = "Text"  # Change this to your actual column name

add_random_emojis(input_csv, output_csv, column_name, emoji_list)
print(f"Updated CSV saved as '{output_csv}'")