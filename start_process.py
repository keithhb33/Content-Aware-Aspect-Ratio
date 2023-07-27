import subprocess
from moviepy.editor import VideoFileClip
# The Python script you want to run
script_name = "run_matlab.py"
processes = []


# Run the Python script 10 times
for i in range(24):
    # Start the script and add the Popen object to the list
    proc = subprocess.Popen(["python", script_name, str(i)])
    processes.append(proc)
    

for proc in processes:
    proc.wait()

from moviepy.editor import *
import os

def compile_frames_to_video(frames_dir, output_video_path, fps=24):
    frames_list = sorted(os.listdir(frames_dir), key=lambda x: int(x.split('frame')[1].split('.')[0]))
    frames_list = [f for f in frames_list if f.endswith('.jpg')]
    clips = [ImageClip(os.path.join(frames_dir, frame)).set_duration(1/fps)
             for frame in frames_list]
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_video_path, fps=fps)


def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def append_audio_to_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path)

def get_fps_of_video(video_path):
    video = VideoFileClip(video_path)
    return video.fps

def find_video_and_get_fps(directory):
    # Find the first MP4 video in the specified directory
    video_file = next((file for file in os.listdir(directory) if file.endswith('.mp4')), None)

    if video_file:
        video_path = os.path.join(directory, video_file)
        fps = get_fps_of_video(video_path)
        print(f"The FPS of the video {video_file} is {fps}")
        return fps
    else:
        print(f"No MP4 video found in directory {directory}")





if __name__ == "__main__":
    frames_dir = "frames_output"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_video_path = os.path.join(output_dir, "final.mp4")

    # Compile frames to video
    compile_frames_to_video(frames_dir, output_video_path, (find_video_and_get_fps("original")))

    # Find the original video in the "original" directory
    original_video_path = next((file for file in os.listdir("original") if file.endswith('.mp4')), None)

    if original_video_path:
        # Extract audio from the original video and save it as MP3
        original_audio_path = "original.mp3"
        extract_audio_from_video(os.path.join("original", original_video_path), original_audio_path)

        # Get the duration of the generated video
        generated_video_duration = VideoFileClip(output_video_path).duration

        # Get the duration of the original audio file
        original_audio_duration = AudioFileClip(original_audio_path).duration

        # Check if the durations match (rounded to two decimal places)
        #if round(generated_video_duration, 2) == round(original_audio_duration, 2):
        # Append audio to the generated video and save as a new file
        final_output_video_path = os.path.join(output_dir, "final_with_audio.mp4")
        append_audio_to_video(output_video_path, original_audio_path, final_output_video_path)
    else:
        print("No original video file found in the 'original' directory.")


