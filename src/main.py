import youtube
import transcribe
import video_editor
import os

padding = float(0.15)

def main():
    channel_url = input("Enter a YouTube channel URL: ")
    videos = youtube.list_channel_videos(channel_url)
    for i in range(0, len(videos)):
        print(f"{i}. {videos[i]["title"]}")
    print(f"Found {len(videos)} videos.")

    start_video = int(input(f"Enter the index of the first video (default: {0}): ").strip() or 0)
    end_video = int(input(f"Enter the index of the last video (default: {len(videos)}): ").strip() or len(videos))
    sentence_to_find = input("Enter the sentence to find (regex is supported): ").strip()
    max_range = float(input(f"Enter the video length to download (in seconds, default: {60}): ").strip() or 60)
    resolution = int(input(f"Insert desired max resolution (in height pixels, default: {720}): ").strip() or 720)
    print(f"Ok let's go.")

    clip_paths = []

    for video in videos[start_video:end_video]:
        title, url, id = video['title'], video['url'], str(video['id']).lstrip('-')

        download_directory = "../downloads"
        clips_directory = "../clips"

        clip_path = clips_directory + "/" + id + ".mp4"
        if os.path.exists(clip_path):
            continue
        
        print(f"\nVideo {title}")

        video_path = download_directory + "/" + id + ".webm"
        if not os.path.exists(video_path):
            print(f"Downloading \"{url}\"...")
            video_path = youtube.download_video(url, video_path, resolution=resolution, range=(0, max_range))
            if not video_path:
                print("Failed to download video.")
                continue
            print(f"Video downloaded: \"{video_path}")

        print(f"Transcribing \"{video_path}\"...")
        transcription = transcribe.transcribe_audio(video_path)
        for word in transcription["words"]:
            word["start"] = word["start"] + padding
            word["end"] = word["end"] + padding
        print(f"Transcription: {transcription["text"]}")
        
        matching_phrases = transcribe.find_phrase(transcription, sentence_to_find)
        for phrase in matching_phrases:
            text, start, end = phrase["text"], phrase["start"], phrase["end"]
            print(f"Matching phrase: \"{text}\"")
            print(f"Creating clip from {start:.2f} to {end:.2f}...")
            clip_output = video_editor.extract_clip(video_path, start, end, clips_directory)
            clip_paths.append(clip_output)
            print(f"Clip created \"{clip_output}\"")

    if clip_paths:
        final_output = "../result/result.mp4"
        video_editor.combine_clips(clip_paths, final_output)
        print(f"Final video saved to \"{final_output}\"")
    else:
        print("No clips found with the specified word.")

if __name__ == "__main__":
    main()
