from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from functions import clean_transcript, translate_file_en_es, make_pdf_book

video_id = input("Enter the YouTube video ID: ")

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id)
formatter = TextFormatter()

txt_formatted = formatter.format_transcript(transcript)

with open(f"{video_id}.txt", 'w', encoding='utf-8') as json_file:
    json_file.write(txt_formatted)

clean_transcript(f"{video_id}.txt", f"{video_id}_cleaned.txt")

if __name__ == "__main__":
    translate_file_en_es(f"{video_id}_cleaned.txt", f"{video_id}_es.txt")
    make_pdf_book(f"{video_id}_es.txt", f"{video_id}_es.pdf", title=f"Traducción del video {video_id}")
