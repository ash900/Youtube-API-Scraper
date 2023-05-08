import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi

# Read the csv file
csv_file = " csv file "
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
        
        # Update the "transcript" field in the DataFrame
        df.loc[df["video_id"] == video_id, "transcript"] = transcript_text
        
        print(f"Captions downloaded for video ID: {video_id}")
    except Exception as e:
        print(f"Error downloading captions for video ID: {video_id}")
        print(str(e))

# Save the updated DataFrame to the csv file
df.to_csv("updated_video_data.csv", index=False)
