import os
import cv2
import time
import subprocess
import shutil
from pathlib import Path
from moviepy.editor import VideoFileClip

ORIGINAL_DIR = "original"
FRAMES_ORIGINAL_DIR = "frames_original"
FRAMES_OUTPUT_DIR = "frames_output"
OUTPUT_DIR = "output"


def ensure_directories_exist():
    """
    Create necessary directories if they do not exist.
    """
    for directory in [ORIGINAL_DIR, FRAMES_ORIGINAL_DIR, FRAMES_OUTPUT_DIR, OUTPUT_DIR]:
        if not os.path.isdir(directory):
            os.mkdir(directory)


def get_file_list(directory):
    """
    Return full paths of files in a given directory.
    """
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]


def check_aspect_ratio(directory):
    """
    Check if at least one MP4 video in the directory has a 4:3 aspect ratio.
    Returns True if 4:3 is detected, False otherwise.
    """
    for file in os.listdir(directory):
        if file.endswith(".mp4"):
            file_path = os.path.join(directory, file)
            with VideoFileClip(file_path) as clip:
                width, height = clip.size
                aspect_ratio = width / height
                # If it's within a tiny epsilon of 4/3, treat it as 4:3
                if abs(aspect_ratio - (4 / 3)) < 1e-6:
                    return True
                else:
                    return False
    return False


def crop_to_ratio(input_path):
    """
    Centrally crop a given video to 4:3 aspect ratio.
    Writes to a NEW file to avoid partial overwriting issues.
    Returns the path of the new cropped file.
    """
    input_file = Path(input_path)
    # We'll create a new output name so we don't overwrite the original file
    output_file = input_file.with_name(f"{input_file.stem}_CROPPED{input_file.suffix}")

    with VideoFileClip(str(input_file)) as clip:
        width, height = clip.size
        original_aspect = width / height

        # If it's already 4:3, just return original
        if abs(original_aspect - (4 / 3)) < 1e-6:
            print("Aspect ratio is already 4:3. No cropping performed.")
            return str(input_file)

        if original_aspect > (4 / 3):
            # Video is wider than 4:3; crop left/right
            new_width = int(height * (4 / 3))
            x_center = width / 2
            cropped_clip = clip.crop(x_center=x_center, width=new_width)
        else:
            # Video is taller than 4:3; crop top/bottom
            new_height = int(width * (3 / 4))
            y_center = height / 2
            cropped_clip = clip.crop(y_center=y_center, height=new_height)

        cropped_clip.write_videofile(
            str(output_file),
            codec='libx264',
            audio_codec='aac',
            fps=clip.fps  # preserve original FPS
        )

    return str(output_file)


class Gui:
    @staticmethod
    def delete_existing_frames():
        """
        Remove all frames from the frames_original directory.
        """
        frames = get_file_list(FRAMES_ORIGINAL_DIR)
        for frame in frames:
            os.remove(frame)
        print("Removed old frames.")
        print("Generating original video frames...")
        return frames

    @staticmethod
    def process_originals():
        """
        Remove old processed frames, then extract frames from the original video
        and save them to frames_original directory.
        """
        # Clear frames_output
        for f in os.listdir(FRAMES_OUTPUT_DIR):
            os.remove(os.path.join(FRAMES_OUTPUT_DIR, f))
        time.sleep(1)

        # Find MP4 in original
        originals = [f for f in os.listdir(ORIGINAL_DIR) if f.endswith('.mp4')]
        if not originals:
            print("No MP4 file found in 'original' directory.")
            return

        original = os.path.join(ORIGINAL_DIR, originals[0])
        video = cv2.VideoCapture(original)
        frame_number = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break
            filename = os.path.join(FRAMES_ORIGINAL_DIR, f'frame{frame_number}.jpg')
            cv2.imwrite(filename, frame)
            frame_number += 1
        video.release()


if __name__ == "__main__":
    ensure_directories_exist()

    original_files = [f for f in os.listdir(ORIGINAL_DIR) if f.endswith('.mp4')]
    if len(original_files) == 0:
        print("Place a 4:3 video file in the 'original' directory.")
        os._exit(0)
    elif len(original_files) > 1:
        print("Ensure only a single file is in the 'original' directory.")
        os._exit(0)

    # Check aspect ratio
    is_correct_aspect_ratio = check_aspect_ratio(ORIGINAL_DIR)
    if not is_correct_aspect_ratio:
        print("Video is not 4:3.")
        crop_question = input("Would you like to centrally crop this video to 4:3? (y/n): ").strip().lower()
        if crop_question == "y":
            input_video_path = os.path.join(ORIGINAL_DIR, original_files[0])
            new_cropped_path = crop_to_ratio(input_video_path)
            # If we actually produced a new file, rename it to replace the original
            if new_cropped_path != input_video_path:
                os.remove(input_video_path)
                shutil.move(new_cropped_path, input_video_path)
        else:
            print("Exiting without cropping.")
            os._exit(0)

    # Extract frames from the (possibly cropped) video
    Gui.process_originals()

    # Run the next process (start_process.py)
    script_name = "start_process.py"
    print("Generating new altered frames...")
    try:
        subprocess.run(["python3", script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"An error occurred while running {script_name}.")
