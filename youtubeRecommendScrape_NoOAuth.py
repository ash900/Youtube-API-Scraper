import os
import googleapiclient.discovery
import pandas as pd

# Set your API key
API_KEY = "insert key"

# Create a YouTube service object
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

# Specify the seed video ID
seed_video_id = "insert vid id"

# Get the recommended videos for the seed video
request = youtube.search().list(
    part="snippet",
    maxResults=60,
    relatedToVideoId=seed_video_id,
    type="video"
)

response = request.execute()

# Process the response to extract the recommended video IDs
recommended_videos = []
for item in response["items"]:
    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]
    recommended_videos.append({"video_id": video_id, "title": title})

# Create a DataFrame from the recommended video data
df = pd.DataFrame(recommended_videos)

# Export the DataFrame to a CSV file
output_file = "recommended_videos.xlsx"
df.to_csv(output_file, index=False)

print("Data exported to", output_file)
