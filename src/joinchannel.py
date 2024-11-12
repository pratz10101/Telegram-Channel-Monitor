from telethon import TelegramClient, functions
from telethon.tl.functions.contacts import SearchRequest
from config import API_ID, API_HASH, SESSION_NAME, KEYWORDS, MAX_JOINS
from db_utils import initialize_db, insert_data

# Initialize the Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Create tables for joined channels
JOINED_CHANNEL_TABLE = '''CREATE TABLE IF NOT EXISTS joined_channels (
                            channel_id INTEGER PRIMARY KEY,
                            access_hash INTEGER,
                            channel_name TEXT
                        )'''

async def join_channel(channel):
    """Joins a Telegram channel and saves channel details to the database."""
    try:
        print(f"Attempting to join channel: {channel.title}")
        await client(functions.channels.JoinChannelRequest(channel))
        print(f"Joined channel: {channel.title}")

        # Save channel info to database
        data = [(channel.id, channel.access_hash, channel.title)]
        insert_data("data/joined_channel.db", "INSERT OR IGNORE INTO joined_channels (channel_id, access_hash, channel_name) VALUES (?, ?, ?)", data)
    except Exception as e:
        print(f"Could not join {channel.title}: {e}")

async def search_and_join_channels():
    """Searches for public channels and joins them based on keywords."""
    print("Starting channel search...")

    for keyword in KEYWORDS:
        print(f"Searching for channels with keyword: {keyword}")
        try:
            result = await client(SearchRequest(q=keyword, limit=10))

            for channel in result.chats:
                if hasattr(channel, 'broadcast') and channel.broadcast:
                    print(f"Found channel: {channel.title}")
                    await join_channel(channel)
        except Exception as e:
            print(f"Error searching with keyword '{keyword}': {e}")

async def main():
    """Main function to start the client and join channels."""
    print("Starting the Telegram client...")
    await client.start()
    await search_and_join_channels()

if __name__ == "__main__":
    # Initialize DB and tables
    initialize_db("data/joined_channel.db", JOINED_CHANNEL_TABLE)
    with client:
        client.loop.run_until_complete(main())
