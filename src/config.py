import os
import csv
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API credentials (from .env)
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")

# Define paths to databases
LINKS_COLLECTED_DB = 'data/links_collected.db'
JOINED_CHANNEL_DB = 'data/joined_channel.db'

# Number of links to collect per channel
LINKS_PER_CHANNEL = 10


# Function to read keywords from CSV
def load_keywords_from_csv(filepath='data/keywords.csv'):
    keywords = []
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                keywords.append(row['keyword'].strip())  # Read the 'keyword' column
    except Exception as e:
        print(f"Error reading keywords from CSV: {e}")
    return keywords

# Load keywords from CSV
KEYWORDS = load_keywords_from_csv()
MAX_JOINS = 10
