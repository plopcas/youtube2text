import configparser
from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

def download_youtube_transcript(video_url):
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get the output folder path from the configuration file
    output_folder = config.get('General', 'output_folder')

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    video_id = video_url.split("v=")[1].split("&")[0]  # Extract video ID from URL

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    print("Available transcripts:")
    for transcript in transcript_list:
        print(f"  {transcript.language} ({transcript.language_code})")

    chosen_locale = input("Please enter the locale of the transcript you want (e.g., en-US): ")
    chosen_transcript = None
    for transcript in transcript_list:
        if transcript.language_code == chosen_locale:
            chosen_transcript = transcript
            break

    if chosen_transcript is None:
        print("No transcript available for the chosen locale.")
        return

    transcript_text = ' '.join([transcript_part['text'] for transcript_part in chosen_transcript.fetch()])

    # Generate the output file path
    output_file = f"{video_id}_{chosen_locale}.txt"
    output_file_path = os.path.join(output_folder, output_file)

    with open(output_file_path, 'w') as file:
        file.write(transcript_text)

    print(f"Transcript saved to: {output_file_path}")

# Example usage:
video_url = input("Please enter the YouTube video URL: ")
download_youtube_transcript(video_url)
