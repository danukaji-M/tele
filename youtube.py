import os
import yt_dlp

# Quality format mapping
QUALITY_FORMATS = {
    'low': 'worstvideo[filesize<50M]+worstaudio[filesize<50M]/worst[filesize<50M]',
    'medium': 'bestvideo[height<=720][filesize<50M]+bestaudio[filesize<50M]/best[height<=720][filesize<50M]',
    'high': 'bestvideo[height<=1080][filesize<50M]+bestaudio[filesize<50M]/best[height<=1080][filesize<50M]'
}

def download_youtube(url, chat_id, quality='medium'):
    video_path = f"video_{chat_id}.mp4"
    audio_path = f"audio_{chat_id}.mp3"

    # yt-dlp options for video
    ydl_opts_video = {
        'outtmpl': video_path,
        'format': QUALITY_FORMATS.get(quality, QUALITY_FORMATS['medium']),
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    # yt-dlp options for audio
    ydl_opts_audio = {
        'outtmpl': audio_path,
        'format': 'bestaudio[filesize<50M]',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Higher quality for 50MB limit
        }],
        'quiet': True,
    }

    try:
        # Try downloading video
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([url])
        if os.path.exists(video_path) and os.path.getsize(video_path) / (1024 * 1024) <= 50:
            return video_path, 'video', None

        # Try downloading audio
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.download([url])
        if os.path.exists(audio_path) and os.path.getsize(audio_path) / (1024 * 1024) <= 50:
            return audio_path, 'audio', None

        return None, None, "Failed to download YouTube media or file too large."

    except Exception as e:
        return None, None, f"Error downloading YouTube media: {str(e)}"