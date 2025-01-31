import os
import re
import shutil
from pytube import Playlist, YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from pydub import AudioSegment
import subprocess

def is_playlist(url):
    """Checks if the given URL is a YouTube playlist."""
    return "list=" in url

def get_video_ids(url):
    """Extracts video IDs from a playlist or single video URL."""
    if is_playlist(url):
        playlist = Playlist(url)
        return [video.split('v=')[1].split('&')[0] for video in playlist.video_urls]
    else:
        yt = YouTube(url)
        return [yt.video_id]

def format_timestamp(seconds):
    """Converts seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def get_transcript(video_id):
    """Fetches the transcript of a YouTube video if available."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([f"[{format_timestamp(entry['start'])}] {entry['text']}" for entry in transcript])
    except TranscriptsDisabled:
        print(f"No subtitles available for video {video_id}. Will use audio-to-text.")
        return None

def download_audio(video_id, output_folder):
    """Downloads audio from a YouTube video."""
    yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_path = audio_stream.download(output_folder, filename=f"{video_id}.mp4")
    return audio_path

def convert_audio_to_wav(audio_path):
    """Converts the audio file to WAV format for processing."""
    wav_path = re.sub(r'\.mp4$', '.wav', audio_path)
    audio = AudioSegment.from_file(audio_path, format="mp4")
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_audio_llama(audio_path):
    """Uses Ollama to transcribe audio using Llama 3.2."""
    command = ["ollama", "run", "llama3.2", "--file", audio_path]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def save_transcript(video_id, transcript_text, output_folder):
    """Saves the transcript to a text file with timestamps directly in the output folder."""
    transcript_file = os.path.join(output_folder, f"{video_id}.txt")
    with open(transcript_file, "w", encoding="utf-8") as file:
        file.write(transcript_text)

def main(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
    video_ids = get_video_ids(url)
    
    for video_id in video_ids:
        print(f"Processing video: {video_id}")
        
        # Save the transcript directly in the output_folder
        transcript = get_transcript(video_id)
        if transcript:
            save_transcript(video_id, transcript, output_folder)
        else:
            audio_path = download_audio(video_id, output_folder)
            wav_path = convert_audio_to_wav(audio_path)
            transcript = transcribe_audio_llama(wav_path)
            save_transcript(video_id, transcript, output_folder)
            os.remove(audio_path)  # Clean up
            os.remove(wav_path)  # Clean up
    print("Transcription completed!")

# Example Usage
if __name__ == "__main__":
    URL = "https://www.youtube.com/playlist?list=PLZoTAELRMXVMBr14UQ30AFlnlQ7eL5wjl"  # Replace with your playlist URL
    OUTPUT_FOLDER = r"/mnt/c/Users/jagat/OneDrive/Desktop/Videos/transcripts"  # Change path as needed
    main(URL, OUTPUT_FOLDER)
