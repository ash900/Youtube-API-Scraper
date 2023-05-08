import os
import google.auth
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
#from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd

# Set your API key (optional)
#API_KEY = " "

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRETS_FILE = "insert json file"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Get OAuth credentials
#credentials, _ = google.auth.load_credentials_from_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

# Create a YouTube service object
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
Credentials = flow.run_local_server(port=0)
#youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY, credentials=credentials)
youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=Credentials)


# Specify the seed video ID
seed_video_id = " insert vid id"

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
    channel = item["snippet"]["channelTitle"]
    recommended_videos.append({"video_id": video_id, "title": title , "channel": channel})

# Create a DataFrame from the recommended video data
df = pd.DataFrame(recommended_videos)

# Export the DataFrame to a CSV file
output_file = "recommended_videos.csv"
df.to_csv(output_file, index=False)

print("Data exported to", output_file)
