from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    return parse_qs(urlparse(url).query)["v"][0]

def get_transcript_from_url(url):
    video_id = get_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([seg["text"] for seg in transcript])
    return video_id, text
