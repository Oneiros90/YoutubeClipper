from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy import concatenate_videoclips
import os

def extract_clip(video_path, start, end, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_file = f"{output_dir}/{base_name}.mp4"
    with VideoFileClip(video_path) as clip:
        subclip = clip.subclipped(start, end)
        subclip.write_videofile(output_file, codec="libx264", audio_codec="aac", logger=None)
    return output_file

def combine_clips(clip_paths, output_path):
    clips = [VideoFileClip(clip) for clip in clip_paths]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path, codec="libx264", logger=None)

if __name__ == "__main__":
    print("Testing video.py")
    video_path = input("Enter a video file path: ")
    start = float(input("Enter start time (seconds): "))
    end = float(input("Enter end time (seconds): "))
    output_path = "../clips"
    extract_clip(video_path, start, end, output_path)
    print(f"Clip saved to {output_path}")
