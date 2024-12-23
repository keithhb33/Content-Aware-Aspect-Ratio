import os
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

SCRIPT_NAME = "run_matlab.py"
FRAMES_DIR = "frames_output"
OUTPUT_DIR = "output"
ORIGINAL_DIR = "original"


def compile_frames_to_video_ffmpeg(frames_dir, output_video_path, fps):
    """
    Compile frames into a video using ffmpeg.
    -y : overwrite output
    -framerate : set the input framerate
    -i : input sequence pattern
    -c:v libx264 and -vf format=yuv420p: Output as h264 with yuv420p pixel format
    -crf 18: good quality
    """
    command = [
        'ffmpeg',
        '-y',
        '-framerate', str(fps),
        '-i', os.path.join(frames_dir, 'frame%d.jpg'),
        '-c:v', 'libx264',
        '-vf', 'format=yuv420p',
        '-crf', '18',
        output_video_path
    ]
    subprocess.run(command, check=True)


def extract_audio_from_video(video_path, audio_path):
    """
    Extract audio track from a given video and save as mp3.
    """
    with VideoFileClip(video_path) as video:
        audio = video.audio
        if audio:
            audio.write_audiofile(audio_path)


def append_audio_to_video(video_path, audio_path, output_path, audio_delay):
    """
    Append audio to the generated video.
    If audio_delay > 0, add silence at start.
    If audio_delay < 0, shift audio start forward.
    """
    with VideoFileClip(video_path) as video, AudioFileClip(audio_path) as audio:
        if audio_delay != 0:
            silence_duration = abs(audio_delay)
            silence = audio.volumex(0).subclip(0, silence_duration)
            if audio_delay > 0:
                # Add silence at the beginning
                audio = concatenate_audioclips([silence, audio])
            else:
                # Cut the audio at the beginning
                audio = audio.subclip(-audio_delay)

        video = video.set_audio(audio)
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')


def get_fps_of_video(video_path):
    """
    Return the FPS of a given video using MoviePy.
    """
    with VideoFileClip(video_path) as video:
        return video.fps


def find_video_and_get_fps(directory):
    """
    Find the first MP4 file in the directory and return its FPS.
    """
    video_file = next((f for f in os.listdir(directory) if f.endswith('.mp4')), None)
    if video_file:
        video_path = os.path.join(directory, video_file)
        fps = get_fps_of_video(video_path)
        print(f"The FPS of the video '{video_file}' is {fps}")
        return fps
    else:
        print("No MP4 video found in the directory.")
        return 24  # default fallback FPS


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Run MATLAB processing in parallel for each of 16 "threads"
    processes = []
    for i in range(16):
        proc = subprocess.Popen(["python3", SCRIPT_NAME, str(i)])
        processes.append(proc)

    # Wait for all MATLAB processes to finish
    for proc in processes:
        proc.wait()

    # Once frames are processed, compile them into a new video
    fps = find_video_and_get_fps(ORIGINAL_DIR)
    output_video_path = os.path.join(OUTPUT_DIR, "video_no_audio.mp4")
    compile_frames_to_video_ffmpeg(FRAMES_DIR, output_video_path, fps)

    # Extract and re-append the audio
    original_video_path = next((f for f in os.listdir(ORIGINAL_DIR) if f.endswith('.mp4')), None)
    if original_video_path:
        original_video_full_path = os.path.join(ORIGINAL_DIR, original_video_path)
        original_audio_path = os.path.join(OUTPUT_DIR, "original_audio.mp3")
        extract_audio_from_video(original_video_full_path, original_audio_path)

        final_output_video_path = os.path.join(OUTPUT_DIR, "final_with_audio.mp4")
        append_audio_to_video(output_video_path, original_audio_path, final_output_video_path, 0)
        print("Process completed successfully.")
    else:
        print("No original video file found in the 'original' directory.")
