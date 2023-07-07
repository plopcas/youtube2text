import os
import configparser
import csv
from youtube_transcript_api import YouTubeTranscriptApi
import re

def download_youtube_transcript(video_url):
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get the output folder path and CSV file path from the configuration file
    output_folder = config.get('General', 'output_folder')
    csv_file = config.get('General', 'csv_file')

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Use the default CSV file path if it is not provided in the configuration file
    if not csv_file:
        csv_file = os.path.join('inputs', 'input.csv')

    if os.path.exists(csv_file):
        # Read URLs and locales from the CSV file
        urls_locales = read_urls_locales_from_csv(csv_file)

        # Iterate over the URLs and download transcripts
        for url, locale in urls_locales:
            download_transcript(url, locale, output_folder)
    else:
        # Prompt for a single URL and locale
        if not video_url:
            video_url = input("Please enter the YouTube video URL: ")
        locale = input("Please enter the locale of the transcript you want (e.g., en-US): ")
        download_transcript(video_url, locale, output_folder)

def read_urls_locales_from_csv(csv_file):
    urls_locales = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 2:
                urls_locales.append((row[0], row[1]))
    return urls_locales

def download_transcript(video_url, locale, output_folder):
    try:
        video_id = extract_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[locale])
        if not transcript:
            raise Exception("No transcript available for the video")

        transcript_text = ' '.join([t['text'] for t in transcript])

        output_file = os.path.join(output_folder, f"{video_id}_{locale}.txt")

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(transcript_text)

        print(f"Transcript downloaded successfully for {video_url} ({locale})")
    except Exception as e:
        print(f"Error downloading transcript for {video_url} ({locale}): {str(e)}")

def extract_video_id(url):
    video_id = url.split("v=")[1].split("&")[0]
    return video_id

# Example usage:
download_youtube_transcript(None)
