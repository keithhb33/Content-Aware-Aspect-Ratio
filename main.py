import os
import cv2
import time
from moviepy.editor import VideoFileClip
from numba import jit, cuda 
import subprocess

original_dir = "original"
frames_original_dir = "frames_original"
frames_output_dir = "frames_output"
output_dir = "output"

if not os.path.isdir(original_dir):
    os.mkdir(original_dir)

if not os.path.isdir(frames_original_dir):
    os.mkdir(frames_original_dir)

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

if not os.path.isdir(frames_output_dir):
    os.mkdir(frames_output_dir)

originals = [os.path.join(original_dir, file) for file in os.listdir(original_dir)]
outputs = [os.path.join(frames_output_dir, file) for file in os.listdir(frames_output_dir)]
frames = [os.path.join(frames_original_dir, file) for file in os.listdir(frames_original_dir)]

def check_aspect_ratio(dir_path):
    files = os.listdir(dir_path)
    for file in files:
        if file.endswith(".mp4"):
            file_path = os.path.join(dir_path, file)
            clip = VideoFileClip(file_path)
            
            width = clip.size[0]
            height = clip.size[1]
            
            # Calculate aspect ratio
            aspect_ratio = width / height

            # Check if aspect ratio is 4:3
            if aspect_ratio == 4/3:
                return True
            else:
                return False
    return False

def crop_to_ratio(input_path):
    # Load the video
    clip = VideoFileClip(input_path)
    
    # Get video dimensions
    width, height = clip.size
    
    # Calculate the new width for 4:3 aspect ratio
    new_width = int(height * 4 / 3)
    
    # Calculate the amount to crop from left and right
    crop_left = (width - new_width) // 2
    crop_right = width - new_width - crop_left
    
    # Crop the video
    cropped_clip = clip.crop(x_center=width/2, width=new_width)
    
    # Write the cropped video to the same input path, effectively replacing it
    cropped_clip.write_videofile(input_path, codec='libx264')



is_correct_aspect_ratio = check_aspect_ratio("original")
if is_correct_aspect_ratio == False:
    print("Video is not 4:3")
    crop_question = str(input("Would you like to centrally crop this video to 4:3? (y/n): "))
    
    if crop_question.lower() == "y":
        directory_path = "original"

        mp4_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4')]
        if mp4_files:
            input_video_path = os.path.join(directory_path, mp4_files[0])
            crop_to_ratio(input_video_path)
        else:
            print("No MP4 file found in the 'original' directory.")
            
            
    os._exit()

    

class Gui:

    @staticmethod
    def delete_existing_frames():
        for frame in frames:
            os.remove(frame)
        print("Removed old frames.")
        print("Generating original video frames...")
        return frames

    @staticmethod
    def process_originals():
        
        #Remove frames_original
        dir = "frames_output"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        time.sleep(1)
        
        for i, original in enumerate(originals):
            video = cv2.VideoCapture(original)
            frame_number = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                filename = os.path.join(frames_original_dir, f'frame{frame_number}.jpg')
                cv2.imwrite(filename, frame)
                frame_number += 1

            video.release()
            

if __name__ == "__main__":
    script_name = "start_process.py"
    print("Generating new altered frames...")
    if len(os.listdir(original_dir)) > 1:
        print("Ensure only a single file is in 'original' directory")
        os._exit(0)
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"An error occurred while running {script_name}.")

