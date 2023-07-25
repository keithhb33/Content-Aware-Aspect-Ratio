import os
import cv2


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
frames = [os.path.join(frames_original_dir, file) for file in os.listdir(frames_original_dir)]

class Gui:

    @staticmethod
    def delete_existing_frames():
        for frame in frames:
            os.remove(frame)
        print("Removed frames")
        return frames
    
    @staticmethod
    def run_photoshop():

        #Essentially, need to create instances of photoshop that can use the extend tool/feature in firefly automation

    @staticmethod
    def process_originals():
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
            
            Gui.run_photoshop
            #Gui.delete_existing_frames()

Gui.process_originals()
