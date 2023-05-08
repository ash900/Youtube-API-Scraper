from googleapiclient.discovery import build
import csv

# Set your Perspective API key
API_KEY = " insert key"

# Initialize the Perspective API client
client = build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

input_csv = "updated_video_data.csv"
output_csv = "analysed_caption_data.csv"

with open(input_csv, 'r') as input_file, open(output_csv, 'w', newline='') as output_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames + ['toxicity', 'severe_toxicity', 'identity_attack', 'insult', 'threat']  # Add new fieldnames for the generated scores
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        transcript = row['transcript']

        # Analyze the caption using the Perspective API
        analyze_request = {
            'comment': {'text': transcript},
            'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'THREAT': {}}
        }
        response = client.comments().analyze(body=analyze_request).execute()

        # Extract the generated scores
        toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']
        severe_toxicity_score = response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']

        # Write the scores to the output CSV file
        row['toxicity'] = toxicity_score
        row['severe_toxicity'] = severe_toxicity_score
        writer.writerow(row)
