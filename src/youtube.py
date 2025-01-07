import yt_dlp

def download_video(url, output_path, resolution=720, range=(0, 60)):
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best',
        'download_ranges': yt_dlp.utils.download_range_func(None, [range]),
        'outtmpl': output_path,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def list_channel_videos(channel_url):
    ydl_opts = {
        'extract_flat': True,  # Only list the videos, don't download them
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        if 'entries' in info:
            return info["entries"][::-1]
        return []

if __name__ == "__main__":
    channel_url = input("Enter a YouTube channel URL: ")
    videos = list_channel_videos(channel_url)
    print(f"Found {len(videos)} videos.")
    for video in videos:
        print(video["title"])
    first_video = videos[0]["url"]
    print(f"Dowloading first video: {first_video}")
    print(download_video(first_video, '../downloads'))
    
