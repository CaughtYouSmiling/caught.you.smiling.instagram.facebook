import os
import cv2
import random
import numpy as np
import logging
import shutil
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
from moviepy import *

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Text Related Parameters
sigma_quotes = [
    "⚠️ Yeh baat sun lo, kaam aayegi! 📢🗿",
    "🎯 Aakhri tak suno, soch badal jayegi! 🧠🗿",
    "💡 Yeh sun lo zindagi ka nazariya badal jayega!🗿",
    "🚀 Yeh baatein tumhare future ka raasta hain! 🗿",
    "⏳ Jo aaj seekhoge, kal kaam aayega! 💰🗿",
    "⛔ Scroll mat karo, samajhne ki koshish karo! 🗿",
    "🔥 Success chahiye? Toh yeh sunna zaroori hai! 🗿",
    "⚡ Chhoti baat, badi soch! 🤯🗿",
    "😱 Yeh nahi suna toh regret hoga! 🔥🗿",
    "👂 Ek baar sun lo, sochne pe majboor ho jaoge! 🗿",
    "🔑 Yeh knowledge game changer hai! 🗿",
    "🏆 Samajh liya toh jeet pakki! 🎯🗿",
    "🤔 Agar samajhna hai, toh dhyaan se suno! 🗿",
    "📌 Aage badhna hai? Yeh yaad rakhna! ✨🗿",
    "🚫 Yeh sirf video nahi, ek seekh hai! 🗿",
    "👑 Jisne samajh liya, uska jeetna tay hai! 🗿",
    "🚀 Yeh nahi suna toh opportunity miss! 💸🗿",
    "⏳ Aaj ignore mat karo, kal kaam aayega! 🗿",
    "⏳ Bas 10 sec sun lo, mind set ho jayega! 🧠⚡🗿",
    "💡 Chhoti nahi, badi reality hai! 🔥🗿",
    "🔓 Success ki chaabi hai, sun lo! 🎯🗿",
    "👀 Ek baar gaur se suno! 💯🗿",
    "💭 Life mein kuch bada karna hai? Yeh suno! 🗿",
    "😎 Words nahi, ek reality check hai! ⚡🗿",
    "⌛ Yeh samajh liya toh waqt badal sakta hai! 🗿",
    "💎 Chhoti baat, bade kaam ki! 🏆🗿",
    "⚠️ Yeh nahi suna toh important cheez miss! 🗿",
    "🚀 Jo aage badhte hain, woh yeh sunte hain! 🗿",
    "📖 Random video mat samjho, ek lesson hai! 🗿",
    "📈 Aage badhna hai? Isse ignore mat karo! 🗿",
    "⏳ Sirf ek minute sun lo, sab clear ho jayega! 🗿",
    "😬 Aaj ignore kiya, kal regret hoga! ❌🗿",
    "🧐 Sab pata hai mat socho, ek baar suno! 👂🗿",
    "🤓 Samajhdar log yeh baatein miss nahi karte! 🗿",
    "🚀 Ek baar suno, soch level up ho jayegi! 🗿",
    "🔑 Kuch Bada karna hai? Yeh samajhna padega! 🗿",
    "🤯 Ek baar gaur kar lo, sab clear ho jayega! 🗿",
    "😎 Yeh video dekh li toh soch badal jayegi! 🗿"
]
font_path = 'VIDEO_EDITING/FONTS/seguiemj_bold.ttf'
font_size = 40
text_to_overlay = random.choice(sigma_quotes)
print("text_to_overlay :", text_to_overlay)

# Video Related Parameters
video_folder_path = 'VIDEOS'
reel_folder_path = 'REELS'
reel_upload_folder_path = 'REEL_TO_UPLOAD'

# Image Related Parameters
num = random.randint(1,2)
up_overlay_image_path = f'VIDEO_EDITING/IMAGES/up_overlay_image_{num}.jpg'
down_overlay_image_path = f'VIDEO_EDITING/IMAGES/down_overlay_image.jpg'
gif_list = ["Ronaldo.gif","Messi.gif"]
gif_file = random.choice(gif_list)
overlay_gif_path = f'VIDEO_EDITING/IMAGES/{gif_file}'

# Text/csv related parameters
counter_file = 'VIDEO_EDITING/../counter.txt'  

# Reel Related Paramters      
crop_margin = 2
crop_x, crop_y, crop_w, crop_h = 0, 0, 0, 0
reel_width, reel_height = 1080, 1920

def get_reel_number():
    """Read the current counter value from the file, or initialize it."""
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            return int(file.read())
    return 0

def remove_previous_reel(reel_number):
    """
    Remove the previous day's reel from the REEL_TO_UPLOAD folder.
    
    Parameters:
        reel_number (int): The current reel number.
    """
    if reel_number > 1:
        previous_reel_path = os.path.join(reel_upload_folder_path, f'reel_{reel_number - 1}.mp4')
        if os.path.exists(previous_reel_path):
            os.remove(previous_reel_path)
            logging.info(f"Removed previous day's reel: {previous_reel_path}")
        else:
            logging.warning(f"Previous day's reel not found: {previous_reel_path}")

def get_input_video(reel_number):
    ## Loop over the video folder and get the input video path
    for filename in os.listdir(video_folder_path):
        if filename.startswith("Video") and filename.endswith(f"_{reel_number}.mp4"):
            input_video_path = os.path.join(video_folder_path, filename) 
            logging.info(f'Processing {filename} as reel_{reel_number}')

    return input_video_path

def copy_to_upload_folder(current_reel_path, reel_number):
    """
    Copy the current day's reel to the REEL_TO_UPLOAD folder.
    
    Parameters:
        current_reel_path (str): Path of the current day's processed reel.
        reel_number (int): The current reel number.
    """
    if not os.path.exists(reel_upload_folder_path):
        os.makedirs(reel_upload_folder_path)
    destination_path = os.path.join(reel_upload_folder_path, f'reel_{reel_number}.mp4')
    shutil.copy(current_reel_path, destination_path)  # Move the file to avoid duplicates
    logging.info(f"Copied reel_{reel_number} to REEL_TO_UPLOAD folder.")
    
def detect_video_area(frame):
    """
    Detect the embedded video area within a frame.
    
    Parameters:
        frame (numpy.ndarray): Input video frame.
    
    Returns:
        tuple: Cropped area's (x, y, w, h), or None if detection fails.
    """
    max_x, max_y = 0, 0
    min_w, min_h = reel_width, reel_height
    
    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Step 2: Apply Bilateral Filter blur to reduce noise
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)

    # Step 3: Multi-Scale Edge Detection (Canny + Laplacian)
    high_thresh, _ = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    low_thresh = 0.5 * high_thresh
    canny_edges = cv2.Canny(blurred, low_thresh, high_thresh)
    laplacian_edges = cv2.Laplacian(blurred, cv2.CV_8U, ksize=5)

    # Step 4: Combine Edge Maps
    edges = cv2.bitwise_or(canny_edges, laplacian_edges)

    # Step 5: Find contours in the edged image
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Step 6: Find the largest contour based on area
        largest_contour = max(contours, key=cv2.contourArea)

        # Step 7: Filter out small/noisy contours by setting a minimum area threshold
        min_contour_area = 0.1 * frame.shape[0] * frame.shape[1]  # 5% of the frame size
        if cv2.contourArea(largest_contour) < min_contour_area:
            return None

        # Step 8: Compute bounding rectangle of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Step 9: Add padding/margin and ensure boundaries are within the frame
        margin = 0  # Reduced margin for more accuracy
        max_x = max(max_x, x + margin)
        max_y = max(max_y, y + margin)
        min_w = min(min_w, w - 2*margin)
        min_h = min(min_h, h - 2*margin)

        return max_x, max_y, min_w, min_h

    return None

# Function to enhance the sharpness of the image
def sharpen_image(frame):
    logging.debug("Applying sharpening filter.")
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(frame, -1, kernel)

# Function to adjust the contrast of the image
def adjust_contrast(frame, alpha=1.2, beta=0):
    logging.debug("Adjusting contrast and brightness.")
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

# Function to enhance color
def enhance_color(frame):
    logging.debug("Enhancing color by converting to HSV and adjusting saturation.")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.addWeighted(hsv[:, :, 1], 1.3, hsv[:, :, 1], 0, 0)  # Increase saturation by 30%
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
def wrap_text(font, max_width,reel_number):
    pil_image = Image.new('RGB', (max_width, reel_height), (0, 0, 0))
    draw = ImageDraw.Draw(pil_image)
    words = text_to_overlay.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = f"{current_line} {word}".strip()
        width = draw.textbbox((0, 0), test_line, font=font)[2]
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    for x in lines:
        x = x.encode('utf-8')
        print("x = ",x)
        
    return "\n".join(lines)

def make_emoji_image(reel_number):
    emoji_font = ImageFont.truetype(font_path, font_size)

    # Create image to calculate text size and handle wrapping
    image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))

    with Pilmoji(image) as pilmoji:
        # Break the emoji text into lines if it's too wide for the video
        wrapped_text = wrap_text(emoji_font, reel_width - 200, reel_number)
        lines = wrapped_text.split("\n")
        max_width = reel_width - 200  # Use the maximum width for alignment
        text_height = sum(pilmoji.getsize(line, emoji_font)[1] for line in lines)

    # Create a new image with the calculated size
    image = Image.new("RGBA", (max_width, text_height), (0, 0, 0, 0))

    # Define some neon colors
    neon_colors = [
        (11,255,0),  # Neon green
        (255,23,112), # Deep pink
        (0,246,255),  # Cyan
        (255,241,0),  # Yellow
        (255,0,0) # Red
    ]

    with Pilmoji(image) as pilmoji:
        y_offset = 0
        for line in lines:
            words = line.split(' ')
            line_width = sum(pilmoji.getsize(word + ' ', emoji_font)[0] for word in words)
            x_offset = (max_width - line_width) // 2  # Center align the entire line

            # Choose a random word index to color
            random_word_index = random.randint(0, len(words) - 1)
            neon_color = random.choice(neon_colors)

            for i, word in enumerate(words):
                word_width, word_height = pilmoji.getsize(word + ' ', emoji_font)
                # Apply neon color to the randomly chosen word, otherwise use white
                color = neon_color if i == random_word_index else (255, 255, 255)
                pilmoji.text((x_offset, y_offset), word + ' ', color, emoji_font, emoji_scale_factor=0.9)
                x_offset += word_width
            y_offset += word_height

    return np.array(image)
            
def clean_up_files(*files):
    """Delete intermediate video files after the final video is created."""
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Deleted file: {file_path}")
        else:
            logging.warning(f"File not found, skipping deletion: {file_path}")
            
def process_video(input_video_path, reel_number):
    cropped_video_path = os.path.join(reel_folder_path, f'cropped_video_no_audio_{reel_number}.mp4')
    cropped_video_with_audio_path = os.path.join(reel_folder_path, f'cropped_video_{reel_number}.mp4')
    output_reel_path = os.path.join(reel_folder_path, f'reel_no_audio_{reel_number}.mp4')
    video_overlay_path = os.path.join(reel_folder_path, f'reel_video_{reel_number}.mp4')
    text_overlay_path = os.path.join(reel_folder_path, f'reel_text_{reel_number}.mp4')
    image_overlay_path = os.path.join(reel_folder_path, f'reel_image_{reel_number}.mp4')
    gif_overlay_path = os.path.join(reel_folder_path, f'reel_gif_{reel_number}.mp4')
    final_output_path = os.path.join(reel_folder_path, f'reel_{reel_number}.mp4')
    
    def add_audio_to_video(input_path, output_path):
        with VideoFileClip(input_video_path) as original_clip, VideoFileClip(input_path) as cropped_clip:
            final_clip = cropped_clip.with_audio(original_clip.audio)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", bitrate="5000k", audio_bitrate="192k")
    
    def crop_video():
        global crop_x, crop_y, crop_w, crop_h
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            logging.error(f"Failed to open video file: {input_video_path}")
            return
        video_area = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if video_area is None:
                video_area = detect_video_area(frame)
                if video_area:
                    x, y, w, h = video_area
                    crop_x, crop_y, crop_w, crop_h = x, y, w, h
                    logging.info(f"Detected video area: {video_area}")
                    
        cap.release()
        
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            logging.error(f"Failed to open video file: {input_video_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        x, y, w, h = crop_x, crop_y, crop_w, crop_h
        out = cv2.VideoWriter(cropped_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Crop the frame using the detected area
            cropped_frame = frame[y:y + h, x:x + w]
            # Apply enhancements: sharpening, contrast, and color enhancement
            cropped_frame = sharpen_image(cropped_frame)
            cropped_frame = adjust_contrast(cropped_frame)
            cropped_frame = enhance_color(cropped_frame)

            # Write the enhanced, cropped frame
            out.write(cropped_frame)

        cap.release()
        if out:
            out.release()
            add_audio_to_video(cropped_video_path, cropped_video_with_audio_path)
    
    def overlay_video():

        extracted_cap = cv2.VideoCapture(cropped_video_with_audio_path)
        if not extracted_cap.isOpened():
            logging.error(f"Could not open cropped video {cropped_video_with_audio_path}")
            return

        fps = extracted_cap.get(cv2.CAP_PROP_FPS)
        output_reel = cv2.VideoWriter(output_reel_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (reel_width, reel_height))
        print("reel_height = ",reel_height)
        print("reel_width = ",reel_width)

        # Load and resize down overlay image
        down_overlay_image = cv2.imread(down_overlay_image_path, cv2.IMREAD_UNCHANGED)
        down_aspect_ratio = down_overlay_image.shape[1] / down_overlay_image.shape[0]
        down_width = reel_width - 250
        down_height = int(down_width / down_aspect_ratio)
        down_overlay_image = cv2.resize(down_overlay_image, (down_width, down_height))

        # Convert down_overlay_image to have transparency by masking black pixels
        # Assumes the background is black (0, 0, 0)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([10, 10, 10])  # Small tolerance for black color
        black_mask = cv2.inRange(down_overlay_image, lower_black, upper_black)
        
        # Replace black pixels with transparent (alpha channel)
        # Add alpha channel to down_overlay_image
        bgr = down_overlay_image[:, :, :3]
        alpha = cv2.bitwise_not(black_mask)
        down_overlay_image = cv2.merge([bgr, alpha])
        
        while extracted_cap.isOpened():
            ret, frame = extracted_cap.read()
            if not ret:
                break
            frame_height, frame_width = frame.shape[:2]
            # print("frame_height = ",frame_height)
            # print("frame_width = ",frame_width)
            aspect_ratio = frame_width / frame_height
            # print("aspect_ratio = ",aspect_ratio)
            if aspect_ratio > (reel_width / reel_height):
                new_width, new_height = reel_width, int(reel_width / aspect_ratio)
            else:
                new_width, new_height = int((reel_height) * aspect_ratio), reel_height

            temp_width = new_width
            temp_height = new_height
            new_width = new_width - 200
            new_height = new_height - 400
            if new_width <= 700:
                new_width = temp_width
            if new_height <= 600:
                new_height = temp_height
            
            # print("new_width = ",new_width)
            # print("new_height = ",new_height)
            
            resized_frame = cv2.resize(frame, (new_width, new_height))
            # print("resized_frame = ",resized_frame)
            black_background = np.zeros((reel_height, reel_width, 3), dtype=np.uint8)
            center_x, center_y = (reel_width - new_width) // 2, int((reel_height - new_height) // 1.2)
            
            # Round the new height to the nearest 500
            rounded_height = 500 * round(new_height / 500)

            # Adjust `center_y` based on the rounded height
            if rounded_height == 500:  # Nearest to 500 or 1000
                center_y = int(center_y // 1.5)  # Replace with your desired value
            
            if rounded_height == 1000:
                center_y = int(center_y // 1.2)  # Replace with your desired value
            
            # print("center_x = ", center_x)
            # print("center_y = ", center_y)
            
            # Create an RGBA image for rounded corners
            rounded_frame = np.zeros((new_height, new_width, 4), dtype=np.uint8)

            # Convert frame to RGBA
            resized_frame_rgba = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2BGRA)

            # Create rounded mask
            mask = np.zeros((new_height, new_width, 4), dtype=np.uint8)
            mask[:, :, 3] = 255  # Set alpha to fully opaque

            radius = min(new_width, new_height) // 17  # Adjust roundness
            pil_mask = Image.fromarray(mask)
            draw = ImageDraw.Draw(pil_mask)
            draw.rounded_rectangle((0, 0, new_width, new_height), radius=radius, fill=(255, 255, 255, 255))
            mask = np.array(pil_mask)

            # Apply rounded corners mask
            rounded_frame = cv2.bitwise_and(resized_frame_rgba, mask)

            # Convert back to BGR (discard alpha since black bg is used)
            rounded_frame_bgr = cv2.cvtColor(rounded_frame, cv2.COLOR_BGRA2BGR)

            # Place the rounded video on the black background
            black_background[center_y:center_y + new_height, center_x:center_x + new_width] = rounded_frame_bgr

            # Add down overlay image (with transparency)
            down_center_y = (reel_height - new_height) // 2 + new_height - 200
            overlay_y1 = down_center_y
            overlay_y2 = down_center_y + down_height
            overlay_x1 = (reel_width - down_width) // 2
            overlay_x2 = overlay_x1 + down_width

            # Apply transparency of the down_overlay_image
            for y in range(down_height):
                for x in range(down_width):
                    if down_overlay_image[y, x, 3] > 0:  # Check if alpha is not 0 (not transparent)
                        black_background[overlay_y1 + y, overlay_x1 + x] = down_overlay_image[y, x, :3]  # Copy RGB
                        
            output_reel.write(black_background)

        extracted_cap.release()
        output_reel.release()
        add_audio_to_video(output_reel_path, video_overlay_path)
        return center_x,center_y

    def overlay_text(center_x,center_y):
        """
        Overlays text onto the final video.

        """

        # Load video
        video = VideoFileClip(video_overlay_path)

        # creates the text image to insert
        text_overlay_image = make_emoji_image(reel_number)

        # Resizing
        text_overlay_aspect_ratio = text_overlay_image.shape[1] / text_overlay_image.shape[0]
        text_overlay_width = text_overlay_image.shape[1]
        text_overlay_height = int(text_overlay_width / text_overlay_aspect_ratio)
        
        text_overlay_image_resized = Image.fromarray(text_overlay_image).resize((int(text_overlay_width),int(text_overlay_height)))
        
        # Convert the resized image to a numpy array again for ImageClip
        text_overlay_clip = ImageClip(np.array(text_overlay_image_resized), duration=video.duration)

        # Repositioning
        text_y = center_y - text_overlay_height - 40
        text_overlay_clip = text_overlay_clip.with_position((center_x,text_y)) 

        # Merge text image with video
        final_clip = CompositeVideoClip([video, text_overlay_clip])

        # Save output    
        final_clip.write_videofile(text_overlay_path, codec="libx264", audio_codec="aac", fps=video.fps)
        
        # Close the Clip
        final_clip.close()
        return text_y
        
    def overlay_image(text_y):
        """
        Overlays an image onto the final video.

        """
        # Load the final video
        video = VideoFileClip(text_overlay_path)

        # Load the overlay image using Pillow
        overlay_image = Image.open(up_overlay_image_path)

        # Convert Pillow image to a numpy array for MoviePy
        overlay_image_np = np.array(overlay_image)
        
        # Resize overlay image if needed
        overlay_image_aspect_ratio = overlay_image_np.shape[1] / overlay_image_np.shape[0]
        overlay_image_width = overlay_image_np.shape[1] - 400
        overlay_image_height = int(overlay_image_width / overlay_image_aspect_ratio)
        overlay_image = overlay_image.resize((int(overlay_image_width),int(overlay_image_height)))  # Adjust size as needed

        # Convert Pillow image to a numpy array for MoviePy
        overlay_image_np = np.array(overlay_image)

        # Create an ImageClip from the numpy array
        overlay_image_clip = ImageClip(overlay_image_np, duration=video.duration)

        # Set the overlay image position (adjust as needed)
        image_y = text_y - overlay_image_height - 40
        overlay_image_clip = overlay_image_clip.with_position(("center", image_y))

        # Merge overlay image with video
        final_clip = CompositeVideoClip([video, overlay_image_clip])

        # Save the output video
        final_clip.write_videofile(image_overlay_path, codec="libx264", audio_codec="aac", fps=video.fps)
        
        # Close the Clip
        final_clip.close()
        
    def overlay_gif():
        """
        Overlays a GIF onto the final video efficiently.
        """
        # Load the final video
        video = VideoFileClip(image_overlay_path)

        # Load the GIF as a VideoClip
        overlay_gif_clip = VideoFileClip(overlay_gif_path, has_mask=True)  # 'has_mask' keeps transparency

        # Resize GIF
        overlay_gif_clip = overlay_gif_clip.resized(width=video.w - 580)
   
        # Trim or Loop the GIF to match the video duration
        print("gif duration = ",overlay_gif_clip.duration)
        print("video duration =",video.duration)
        
        if overlay_gif_clip.duration > video.duration:
            overlay_gif_clip = overlay_gif_clip.subclipped(0, video.duration)  # Trim GIF

        # Set overlay position
        gif_y = 1630
        gif_x = -130
        
        print(f"GIF Position: (x={gif_x}, y={gif_y})")
        print(f"GIF Dimensions: (w={overlay_gif_clip.w}, h={overlay_gif_clip.h})")
        print(f"Video Dimensions: (w={video.w}, h={video.h})")
    
        overlay_gif_clip = overlay_gif_clip.with_position((gif_x, gif_y))

        # Merge overlay GIF with video
        final_clip = CompositeVideoClip([video, overlay_gif_clip])

        # Save the output video
        final_clip.write_videofile(gif_overlay_path, codec="libx264", audio_codec="aac", fps=video.fps)

        # Close the Clip
        final_clip.close()
    
    # Step 1 - Crop the Video Out
    crop_video()
    # Step 2 - Overlay the cropped Video on a Black Background
    center_x, center_y = overlay_video()
    # Step 3 - Overlay Text
    text_y = overlay_text(center_x,center_y)
    # Step 4 - Overlay Image
    overlay_image(text_y)
    # Step 5 - Overlay Gifs
    overlay_gif()
    # Step 6 - Clean up some files
    shutil.copy(gif_overlay_path,final_output_path)
    clean_up_files(cropped_video_path, cropped_video_with_audio_path, output_reel_path, video_overlay_path, text_overlay_path, image_overlay_path, gif_overlay_path)

def main():
    # Getting the reel number from counter file.
    reel_number = get_reel_number()
    print(f"Reel Number : {reel_number}")
    
    # Remove the previous day's reel before starting today's processing
    remove_previous_reel(reel_number)
    
    # Get the input video from video folder.
    input_video_path = get_input_video(reel_number)
    
    # Process the input video
    process_video(input_video_path, reel_number)
            
    # Copy the final processed reel to REEL_TO_UPLOAD
    final_reel_path = os.path.join(reel_folder_path, f'reel_{reel_number}.mp4')
    copy_to_upload_folder(final_reel_path, reel_number)
            
if __name__ == "__main__":
    main()
