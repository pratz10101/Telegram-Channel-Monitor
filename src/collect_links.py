import os
import asyncio
import sqlite3
from telethon import TelegramClient
from telethon.tl.types import PeerChannel, MessageMediaWebPage
from dotenv import load_dotenv
from config import LINKS_COLLECTED_DB, JOINED_CHANNEL_DB, LINKS_PER_CHANNEL  # Correct import

# Load environment variables
load_dotenv()

# Telegram client setup
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")

client = TelegramClient(session_name, api_id, api_hash)

# Function to initialize the database for storing collected links
def initialize_links_db():
    conn = sqlite3.connect(LINKS_COLLECTED_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS collected_links (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        channel_name TEXT,
                        link TEXT
                     )''')
    conn.commit()
    conn.close()

# Function to initialize the joined_channels database
def initialize_joined_channels_db():
    conn = sqlite3.connect(JOINED_CHANNEL_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS joined_channels (
                        channel_id INTEGER PRIMARY KEY,
                        access_hash INTEGER,
                        channel_name TEXT
                     )''')
    conn.commit()
    conn.close()

# Function to collect links from a specific channel
async def collect_links_from_channel(channel_id, access_hash, channel_name):
    """Collects 10 links from a specified channel using its ID and access hash."""
    try:
        # Retrieve channel entity using ID and access hash
        channel_entity = PeerChannel(channel_id)
        print(f"Collecting links from channel: {channel_name}")

        # Fetch messages and extract links
        links = []
        async for message in client.iter_messages(channel_entity, limit=100):
            if len(links) >= LINKS_PER_CHANNEL:
                break
            if message.media and isinstance(message.media, MessageMediaWebPage):
                link = message.media.webpage.url
                if link:
                    links.append(link)

        # Save collected links to the database
        if links:
            conn = sqlite3.connect(LINKS_COLLECTED_DB)
            cursor = conn.cursor()
            for link in links[:LINKS_PER_CHANNEL]:  # Limit to 10 links per channel
                cursor.execute("INSERT INTO collected_links (channel_name, link) VALUES (?, ?)", (channel_name, link))
            conn.commit()
            conn.close()
            print(f"Collected and saved {len(links)} links from {channel_name}")
        else:
            print(f"No links found in {channel_name}")
    except Exception as e:
        print(f"Could not collect links from {channel_name}: {e}")

# Function to collect links from all joined channels
async def collect_links_from_all_channels():
    """Reads joined channels from joined_channel.db and collects links."""
    conn = sqlite3.connect(JOINED_CHANNEL_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id, access_hash, channel_name FROM joined_channels")
    channels = cursor.fetchall()
    conn.close()

    for channel_id, access_hash, channel_name in channels:
        await collect_links_from_channel(channel_id, access_hash, channel_name)

# Main function to run the client and start collecting links
async def main():
    """Main function to start the client and collect links from channels."""
    print("Starting the Telegram client...")
    await client.start()
    print("Starting to collect links from channels...")
    await collect_links_from_all_channels()

if __name__ == "__main__":
    # Initialize the databases
    initialize_links_db()  # Initialize the links collected database
    initialize_joined_channels_db()  # Initialize the joined channels database
    with client:
        client.loop.run_until_complete(main())
