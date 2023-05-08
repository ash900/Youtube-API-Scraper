import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
# Gets transcripts with a desired KB limit
# Read the csv file
csv_file = "csv"
df = pd.read_csv(csv_file)

# Extract the video IDs from the "videoID" column
video_ids = df["video_id"].tolist()

# Download captions for each video
for video_id in video_ids:
    try:
        captions = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Process the captions as needed
        # You can save them to a file, analyze them, etc.
        # Example: Save captions to a text file
        transcript_text = "\n".join(caption["text"] for caption in captions)
        
        # Limit the transcript text to approximately 20KB
        max_text_length = 17 * 1024  # 20KB in bytes
        if len(transcript_text.encode("utf-8")) > max_text_length:
            transcript_text = transcript_text[:max_text_length].rsplit(' ', 1)[0]  # Truncate the text
            
        # Save the limited transcript to a text file
        #with open(f"{video_id}_captions.txt", "w", encoding="utf-8") as file:
        #    file.write(transcript_text)
        # Update the "transcript" field in the DataFrame
        df.loc[df["video_id"] == video_id, "transcript"] = transcript_text
        
        print(f"Captions downloaded for video ID: {video_id}")
    except Exception as e:
        print(f"Error downloading captions for video ID: {video_id}")
        print(str(e))

# Save the updated DataFrame to the csv file
df.to_csv("updated_video_data.csv", index=False)
