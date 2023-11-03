import subprocess
from moviepy.editor import VideoFileClip
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.editor import concatenate_audioclips, vfx
import os

# The Python script you want to run
script_name = "run_matlab.py"
processes = []

# Run the Python script 10 times
for i in range(16):
    # Start the script and add the Popen object to the list
    proc = subprocess.Popen(["python", script_name, str(i)])
    processes.append(proc)

for proc in processes:
    proc.wait()

def compile_frames_to_video_ffmpeg(frames_dir, output_video_path, fps):
    command = [
        'ffmpeg',
        '-y',  # overwrite output file if it exists
        '-framerate', str(fps),  # set the framerate
        '-i', os.path.join(frames_dir, 'frame%d.jpg'),  # input file pattern
        '-c:v', 'libx264',  # video codec
        '-vf', 'format=yuv420p',  # pixel format
        '-crf', '18',  # quality level
        output_video_path  # output file
    ]
    subprocess.run(command, check=True)

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

def append_audio_to_video(video_path, audio_path, output_path, audio_delay):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Adjust the audio track by the specified delay
    if audio_delay != 0:
        # Create a silent audio segment of duration `audio_delay`
        silence = AudioFileClip(audio_path).volumex(0).subclip(0, abs(audio_delay))
        if audio_delay > 0:
            # If the delay is positive, add silence at the beginning
            audio = concatenate_audioclips([silence, audio])
        else:
            # If the delay is negative, cut the audio at the beginning
            audio = audio.subclip(-audio_delay)
    
    video = video.set_audio(audio)
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')


def get_fps_of_video(video_path):
    video = VideoFileClip(video_path)
    fps = video.fps
    video.reader.close()
    video.audio.reader.close_proc()
    return fps

def find_video_and_get_fps(directory):
    video_file = next((file for file in os.listdir(directory) if file.endswith('.mp4')), None)
    if video_file:
        video_path = os.path.join(directory, video_file)
        fps = get_fps_of_video(video_path)
        print(f"The FPS of the video {video_file} is {fps}")
        return fps
    else:
        print("No MP4 video found in directory.")
        return 24  # Default FPS

if __name__ == "__main__":
    frames_dir = "frames_output"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Find the FPS of the original video
    fps = find_video_and_get_fps("original")

    # Compile frames to video
    output_video_path = os.path.join(output_dir, "video_no_audio.mp4")
    compile_frames_to_video_ffmpeg(frames_dir, output_video_path, fps)

    # Find the original video in the "original" directory
    original_video_path = next((file for file in os.listdir("original") if file.endswith('.mp4')), None)
    
    if original_video_path:
        # Extract audio from the original video
        original_audio_path = os.path.join(output_dir, "original_audio.mp3")
        extract_audio_from_video(os.path.join("original", original_video_path), original_audio_path)
        
        # Append audio to the generated video and save as a new file
        # Delay the audio by 0.56 seconds
        final_output_video_path = os.path.join(output_dir, "final_with_audio.mp4")
        append_audio_to_video(output_video_path, original_audio_path, final_output_video_path, 0.56)
        
        print("Process completed successfully.")
    else:
        print("No original video file found in the 'original' directory.")



