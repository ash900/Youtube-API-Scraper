import os
import googleapiclient.discovery
from google.oauth2 import service_account

# Set the API key.
API_KEY = "AIzaSyDIGx71TQSbp0A25p7Mss1O09fzbc754og"
CREDENTIALS_FILE = "C:\\Users\\Aashir\\Downloads\\rugged-silo-349212-08e7758768cc.json"

# Set up OAuth2 credentials.
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/youtube.force-ssl"])

# Create a YouTube service object.
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=scoped_credentials)

# Get the list of recommended videos for the seed video.
request = youtube.videos().list(
    part=["snippet,contentDetails"],
    id="y-_vAaQhyZg"
)
response = request.execute()

# Get the captions for each recommended video.
for video in response["items"]:
    # Get the captions for the video.
    captions_request = youtube.captions().download(
        id=video["id"],
        tfmt="srt"
    )
    captions_response = captions_request.execute()

    # Save the captions to a file.
    with open(video["id"] + ".srt", "w", encoding="utf-8") as f:
        f.write(captions_response)
