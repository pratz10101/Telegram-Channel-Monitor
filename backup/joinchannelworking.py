import os
import asyncio
import sqlite3
from telethon import TelegramClient, functions
from telethon.tl.functions.contacts import SearchRequest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")

# Ensure all required environment variables are set
if not all([api_id, api_hash, session_name]):
    print("Missing one or more required environment variables.")
    exit()

# Keywords to search for in channel names
keywords = ["udemy", "hackernews"]
max_joins = 10  # Maximum number of channels to join

# Initialize Telegram client
client = TelegramClient(session_name, api_id, api_hash)

# Counter for the number of channels joined
joined_count = 0

# SQLite database setup
db_name = "joined_channels.db"

def initialize_database():
    """Creates the SQLite database and joined_channels table only if they don't exist."""
    # Check if the database file exists
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Create table for joined channels
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS joined_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER,
                channel_name TEXT,
                username TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        print("Database and table created.")
    else:
        print("Database already exists. Skipping creation.")

def save_channel_to_database(channel_id, channel_name, username):
    """Inserts the joined channel's info into the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO joined_channels (channel_id, channel_name, username) VALUES (?, ?, ?)", 
                   (channel_id, channel_name, username))
    conn.commit()
    conn.close()

async def join_channel(channel):
    """Joins a Telegram channel and saves its details to the SQLite database."""
    global joined_count
    try:
        print(f"Attempting to join channel: {channel.title}")
        await client(functions.channels.JoinChannelRequest(channel))
        print(f"Joined channel: {channel.title}")

        # Save channel information (ID, name, username) to the database
        save_channel_to_database(channel.id, channel.title, channel.username or "")
        joined_count += 1
    except Exception as e:
        print(f"Could not join {channel.title}: {e}")   

async def search_and_join_channels():
    """Searches for public channels and joins them based on keywords."""
    global joined_count
    print("Starting channel search...")

    for keyword in keywords:
        if joined_count >= max_joins:
            print("Reached the maximum number of channels to join.")
            break
            
        print(f"Searching for channels with keyword: {keyword}")
        try:
            # Search for channels using the keyword
            result = await client(SearchRequest(
                q=keyword,
                limit=10  # Number of results to fetch per keyword
            ))

            for channel in result.chats:
                # Only attempt to join if it's a public channel and if we haven't hit the max limit
                if hasattr(channel, 'broadcast') and channel.broadcast and joined_count < max_joins:
                    print(f"Found channel: {channel.title}")
                    await join_channel(channel)  # Pass the actual channel object
                    # Break out if max_joins is reached
                    if joined_count >= max_joins:
                        print("Reached the max join limit.")
                        break
        except Exception as e:
            print(f"Error searching with keyword '{keyword}': {e}")

async def main():
    """Main function to start the client and join channels."""
    print("Starting the Telegram client...")
    await client.start()

    # Initialize the database (if not already created)
    initialize_database()

    await search_and_join_channels()

# Run the bot
with client:
    client.loop.run_until_complete(main())
