import os
import cv2
import time

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


class Gui:

    @staticmethod
    def delete_existing_frames():
        for frame in frames:
            os.remove(frame)
        print("Removed frames")
        return frames

    @staticmethod
    def process_originals():
        
        #Remove frames_original
        dir = "frames_original"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        time.sleep(2)
        
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
            
#            Gui.delete_existing_frames()
if originals != outputs:
    Gui.process_originals()

import subprocess

#while not (len(os.listdir("frames_original")) == len(os.listdir("frames_output"))):
#    print("Still processing...")
    
if __name__ == "__main__":
    script_name = "start_process.py"

    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"An error occurred while running {script_name}.")

