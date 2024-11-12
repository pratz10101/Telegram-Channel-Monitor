import os
import csv
import sqlite3
import asyncio
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
client = TelegramClient(session_name, api_id, api_hash)

# Define paths for files and databases
base_dir = os.path.dirname(__file__)
SUS_KEYWORDS_FILE = os.path.join(base_dir, 'C:/Users/pratz/Desktop/Project/data/sus_keys.csv')
JOINED_CHANNEL_DB = os.path.join(base_dir, 'C:/Users/pratz/Desktop/Project/data/joined_channel.db')
FLAGGED_MESSAGES_DB = os.path.join(base_dir, 'C:/Users/pratz/Desktop/Project/data/flagged_messages.db')  # New database for flagged messages

# Load suspicious keywords from CSV file
def load_suspicious_keywords():
    keywords = []
    try:
        with open(SUS_KEYWORDS_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                keywords.extend(row)
        print(f"Loaded {len(keywords)} suspicious keywords.")
    except FileNotFoundError:
        print("Warning: sus_keys.csv not found.")
    return keywords

# Initialize the flagged messages database
def initialize_flagged_messages_db():
    conn = sqlite3.connect(FLAGGED_MESSAGES_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS flagged_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        channel_id INTEGER,
                        channel_name TEXT,
                        keyword TEXT,
                        message_text TEXT
                     )''')
    conn.commit()
    conn.close()

# Function to flag suspicious messages in a channel
async def flag_suspicious_messages(channel_id, channel_name, keywords):
    """Scans messages in a channel for suspicious keywords and flags them."""
    print(f"Scanning messages in {channel_name} for suspicious content...")
    channel_entity = PeerChannel(channel_id)

    async for message in client.iter_messages(channel_entity, limit=100):  # Adjust limit as needed
        message_text = message.message or ""
        for keyword in keywords:
            if keyword.lower() in message_text.lower():
                # Log the flagged message
                conn = sqlite3.connect(FLAGGED_MESSAGES_DB)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO flagged_messages (channel_id, channel_name, keyword, message_text) VALUES (?, ?, ?, ?)",
                               (channel_id, channel_name, keyword, message_text))
                conn.commit()
                conn.close()
                print(f"Flagged message in {channel_name} with keyword '{keyword}': {message_text[:50]}...")  # Preview of flagged message
                break

# Function to scan all channels for suspicious messages
async def analyze_channels_for_suspicious_activity():
    """Scans all joined channels for suspicious activity and flags messages."""
    conn = sqlite3.connect(JOINED_CHANNEL_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id, channel_name FROM joined_channels")
    channels = cursor.fetchall()
    conn.close()

    keywords = load_suspicious_keywords()
    if not keywords:
        print("No suspicious keywords loaded. Exiting.")
        return

    for channel_id, channel_name in channels:
        await flag_suspicious_messages(channel_id, channel_name, keywords)

# Main function
async def main():
    """Main function to initialize DBs and scan for suspicious messages."""
    initialize_flagged_messages_db()  # Set up flagged messages database
    print("Starting the Telegram client...")
    await client.start()
    await analyze_channels_for_suspicious_activity()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
